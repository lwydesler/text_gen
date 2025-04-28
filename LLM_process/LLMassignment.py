import math
import re
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import Tongyi# 记得根据实际导入Tongyi

class ArticleAssignerExtreme:
    def __init__(self, model_name, batch_size=50):
        """
        :param model_name: 通义千问模型名称
        :param batch_size: 每批处理的段落数
        """
        current_api_key = 'sk-ff2f7a46bc0f412c9ae4915a2829465c'  # 你的DashScope API Key
        if not current_api_key:
            raise ValueError("请设置 API Key")

        # 初始化 LLM
        self.llm = Tongyi(
            model_name=model_name,
            dashscope_api_key=current_api_key
        )
        self.batch_size = batch_size

        # 创建空Prompt的链，后续每次动态指定Prompt
        self.llm_model = LLMChain(llm=self.llm, prompt=PromptTemplate(
            input_variables=["text"],
            template="{text}"
        ))

        # 定义归属任务模板
        self.assignment_template = """
你是一个文档结构智能分析专家，任务是根据段落摘要，判断每个段落最适合归属到哪些章节标题下。

要求：
- 可以归属到一个或多个章节。
- 如果归属多个章节，列出所有相关章节编号。
- 严格按照格式输出，不要添加任何解释或注释。


章节列表：
{chapter_list}

段落摘要列表：
{paragraph_list}

请按照如下格式输出归属关系：
[{{段落1: 1, 3}},
{{段落2: 2}},
{{段落3: 1, 2}}...]
...

开始归类：
"""
        self.prompt_template = PromptTemplate(
            input_variables=["chapter_list", "paragraph_list"],
            template=self.assignment_template
        )

    def _build_prompt(self, base_articles, reference_articles_batch, batch_start_idx):
        """
        构建Prompt
        """
        chapters = [f"{idx + 1}. {'-'.join(item['title'])}" for idx, item in enumerate(base_articles)]
        paragraphs = [f"{batch_start_idx + idx + 1}. {item['summary']}" for idx, item in enumerate(reference_articles_batch)]
        return self.prompt_template.format_prompt(
            chapter_list='\n'.join(chapters),
            paragraph_list='\n'.join(paragraphs)
        ).to_string()

    
    def _parse_response(self, response_text):
        """
        解析模型输出（适配 ['[{段落1: 1},', '{段落2: 2}]'] 这种格式）
        """
        mapping = {}

        # 先把列表里的唯一元素取出来
        if isinstance(response_text, list):
            response_text = response_text[0]

        # 去掉两边的中括号和空格
        response_text = response_text.strip()[1:-1]

        # 按逗号分开每一小段
        items = response_text.split(',')
        
        pattern = r"段落\s*(\d+)\s*:\s*(\d+)"

        for item in items:
            item = item.strip().strip('{}')  # 去掉每项里的花括号
            match = re.match(pattern, item)
            if match:
                para_idx = int(match.group(1)) - 1
                chapter_idx = int(match.group(2)) - 1
                mapping[para_idx] = [chapter_idx]  # 注意：用列表包起来
        return mapping

    def assign(self, base_articles, reference_articles):
        """
        主执行函数
        """
        for item in base_articles:
            item['references'] = []

        total_refs = len(reference_articles)
        num_batches = math.ceil(total_refs / self.batch_size)

        for batch_idx in range(num_batches):
            batch_start = batch_idx * self.batch_size
            batch_end = min((batch_idx + 1) * self.batch_size, total_refs)
            reference_batch = reference_articles[batch_start:batch_end]

            prompt = self._build_prompt(base_articles, reference_batch, batch_start)
            print('prompt:', prompt)

            # invoke 时，传入的是 {"text": prompt}
            response = self.llm_model.invoke({"text": prompt})
            print(f"--- 第 {batch_idx} 批次的 LLM 原始输出 ---") # 添加这行
            print('response:', response)                                  # 添加这行
            print("--- LLM 输出结束 ---")                      # 添加这行
            if not response:
                print(f"警告：第 {batch_idx} 批次的 LLM 输出为空") # 可选：添加警告
                continue

            model_output = response.get('text') if isinstance(response, dict) else response
            if not model_output:
                continue  # 防止空输出

            mapping = self._parse_response(model_output)

            for ref_global_idx, chapter_idxs in mapping.items():
                if 0 <= ref_global_idx < len(reference_articles):
                    ref_item = {
                        'id': reference_articles[ref_global_idx]['id'],
                        #'summary': reference_articles[ref_global_idx]['summary'],
                        #'length': reference_articles[ref_global_idx]['length']
                    }
                    # ref_item = reference_articles[ref_global_idx]['id']
                    for chapter_idx in chapter_idxs:
                        if 0 <= chapter_idx < len(base_articles):
                            base_articles[chapter_idx]['references'].append(ref_item)

        return base_articles
if __name__ == '__main__':

    # 初始化分配器
    assigner = ArticleAssignerExtreme(model_name="qwen-plus", batch_size=50)

    base_articles = [
        {'title': ['引言', '研究背景'], 'length': 58},
        {'title': ['方法', '数据处理'], 'length': 52},
    ]

    reference_articles = [
        {'summary': '本文介绍了研究背景和意义...', 'id': 1, 'length': 58},
        {'summary': '本节描述了数据采集和处理方法...', 'id': 2, 'length': 52},
    ]

    # 进行章节分配
    new_articles = assigner.assign(base_articles, reference_articles)

    print(new_articles)