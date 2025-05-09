from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import Tongyi# 记得根据实际导入Tongyi

# class ParagraphGenerator:
#     def __init__(self, model_name):

#         current_api_key = 'sk-ff2f7a46bc0f412c9ae4915a2829465c'  # 你的DashScope API Key
#         if not current_api_key:
#             raise ValueError("请设置 API Key")

#         # 初始化 LLM
#         self.llm = Tongyi(
#             model_name=model_name,
#             dashscope_api_key=current_api_key
#         )

#         self.prompt_template = PromptTemplate(
#             input_variables=["chapter_title", "reference_title", "reference_summary", "reference_paragraph", "reference_length"],
#             template="""
# 你是一位专业的写作助手，请你根据下列段落内容和摘要，生成与章节标题匹配的新段落内容。要求如下：
# 1. 保持内容围绕章节标题展开；
# 2. 使用原段落的核心信息，但可以改写、重组或扩展；
# 3. 控制输出字数与原段落字数相近（误差不超过 ±20%）；
# 4. 保持表达通顺、学术风格一致。

# 【章节标题】：{chapter_title}
# 【原段落标题】：{reference_title}
# 【原段落摘要】：{reference_summary}
# 【原段落正文】：{reference_paragraph}
# 【原段落字数】：{reference_length}

# 请生成新的段落内容：
# """
#         )
#         self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

#     def generate_paragraph(self, chapter_title, reference):
#         try:
#             return self.chain.run({
#                 "chapter_title": chapter_title,
#                 "reference_title": reference["title"],
#                 "reference_summary": reference["summary"],
#                 "reference_paragraph": reference["paragraph"],
#                 "reference_length": reference["length"]
#             }).strip()
#         except Exception as e:
#             return f"生成失败: {str(e)}"

#     def generate_all(self, data):
#         for chapter in data:
#             chapter_title = chapter["title"]
#             for ref in chapter["references"]:
#                 ref["generated_paragraph"] = self.generate_paragraph(chapter_title, ref)
#         return data

# import tiktoken
# import openai

# class ParagraphGenerator:
#     def __init__(self, model="gpt-3.5-turbo", max_tokens=3000):
#         self.model = model
#         self.max_tokens = max_tokens
#         self.encoding = tiktoken.encoding_for_model(model)

#     def count_tokens(self, text):
#         if isinstance(text, list):
#             text = " ".join(text)
#         return len(self.encoding.encode(text))

#     def generate_combined_paragraph(self, chapter: dict):
#         """
#         自动拼接并生成当前章节内容（按 token 限制切分）
#         """
#         title = chapter["title"]
#         references = chapter["references"]
#         combined_paragraphs = []
#         temp_refs = []
#         token_count = self.count_tokens(str(title))

#         for ref in references:
#             content = ref["paragraph"]
#             if isinstance(content, list):
#                 content = "\n".join(content)
#             ref_tokens = self.count_tokens(content)

#             # 如果加上当前段落会超出 token 限制，则处理已有段落
#             if token_count + ref_tokens > self.max_tokens:
#                 if temp_refs:
#                     result = self._call_openai(temp_refs, title)
#                     combined_paragraphs.append(result)
#                     temp_refs = []
#                     token_count = self.count_tokens(str(title))
#             temp_refs.append(content)
#             token_count += ref_tokens

#         # 最后一个分段未处理的也补上
#         if temp_refs:
#             result = self._call_openai(temp_refs, title)
#             combined_paragraphs.append(result)

#         return "\n\n".join(combined_paragraphs)

#     def generate_all_chapters(self, chapters: list):
#         """
#         批量处理所有章节并返回生成结果
#         """
#         results = []
#         for i, chapter in enumerate(chapters):
#             print(f"📘 正在处理第 {i+1} 章：{chapter['title']}")
#             try:
#                 combined = self.generate_combined_paragraph(chapter)
#                 results.append({
#                     "title": chapter["title"],
#                     "generated_paragraph": combined
#                 })
#             except Exception as e:
#                 print(f"❌ 错误：章节 {chapter['title']} 处理失败，原因：{e}")
#                 results.append({
#                     "title": chapter["title"],
#                     "generated_paragraph": f"[错误] 无法生成该章节内容：{e}"
#                 })
#         return results

#     def _call_openai(self, paragraphs: list, title: list):
#         """
#         内部方法：调用 OpenAI 接口生成摘要内容
#         """
#         prompt = (
#             f"你是一名学术写作助手，请根据以下段落内容，围绕标题 {'-'.join(title)}，"
#             f"生成一段总结性文本，风格正式、结构清晰、内容通顺，控制篇幅在参考内容的长度范围内。\n\n"
#             f"参考内容：\n{''.join(paragraphs)}"
#         )

#         messages = [
#             {"role": "system", "content": "你是一个学术内容撰写助手"},
#             {"role": "user", "content": prompt}
#         ]

#         response = openai.ChatCompletion.create(
#             model=self.model,
#             messages=messages,
#             temperature=0.4
#         )

#         return response["choices"][0]["message"]["content"].strip()

import os
from langchain_community.llms import Tongyi
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
# import tiktoken # No longer strictly needed for Tongyi unless you have a specific use case

# 假设你的 DashScope API Key 存储在环境变量中或直接提供
# DASH SCOPE_API_KEY = "sk-ff2f7a46bc0f412c9ae4915a2829465c" # 最好从环境变量读取

class ParagraphGenerator:
    def __init__(self, model_name="qwen-turbo", dashscope_api_key='', num_limit=2500): # 默认模型设为qwen-turbo或你选择的
        """
        初始化 ParagraphGenerator。
        :param model_name: Tongyi 模型的名称，例如 "qwen-turbo", "qwen-plus", "qwen-max"。
        :param dashscope_api_key: DashScope API Key. 如果为 None, 会尝试从环境变量 'DASHSCOPE_API_KEY' 读取。
        """
        self.model_name = model_name
        self.num_limit = num_limit
        
        if dashscope_api_key:
            current_api_key = dashscope_api_key
        else:
            current_api_key = os.environ.get("DASHSCOPE_API_KEY")
            # current_api_key = '4915a2829465c' # 或者直接硬编码，但不推荐生产环境

        if not current_api_key:
            raise ValueError("请设置 DashScope API Key 或通过参数传入。")

        # 初始化 LLM
        self.llm = Tongyi(
            model_name=self.model_name,
            dashscope_api_key=current_api_key
            # temperature=0.4 # 可以在这里设置，或者在调用时设置
        )

        # 注意：这个PromptTemplate是为处理单个参考段落设计的
        self.prompt_template = PromptTemplate(
            input_variables=["chapter_title", "reference_title", "reference_paragraph", "reference_length"],
            template="""
你是一位专业的写作助手，请你根据下列段落内容和摘要，生成与章节标题匹配的新段落内容。要求如下：
1. 保持内容围绕章节标题展开；
2. 使用原段落的核心信息，但可以改写、重组或扩展；
3. 控制输出字数与原段落字数相近（误差不超过 ±20%）；
4. 保持表达通顺、学术风格一致。

【章节标题】：{chapter_title}
【原段落标题】：{reference_title}
【原段落正文】：{reference_paragraph}
【原段落字数】：{reference_length}

请生成新的段落内容：
"""
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def get_character_count(self, text):
        """
        计算文本的字符数。
        """
        if isinstance(text, list):
            text = "\n".join(text) # 如果是列表，先合并
        return len(text)

    def generate_paragraph_for_reference(self, chapter_title: str, reference: dict):
        """
        为单个参考文献生成新的段落内容。
        假设 reference 字典包含 'title', 'summary', 'paragraph' 键。
        """
        reference_title = reference.get("title", "N/A") # 如果没有标题，提供默认值
        reference_summary = reference.get("summary", "N/A") # 如果没有摘要，提供默认值
        reference_paragraph = reference.get("paragraph", "")
        
        if isinstance(reference_paragraph, list):
            reference_paragraph = "\n".join(reference_paragraph)

        reference_length = self.get_character_count(reference_paragraph)

        if not reference_paragraph.strip():
            # print(f"    Skipping empty reference paragraph for reference title: {reference_title}")
            return "" # 如果原段落为空，则不生成

        inputs = {
            "chapter_title": chapter_title,
            "reference_title": reference_title,
            "reference_summary": reference_summary,
            "reference_paragraph": reference_paragraph,
            "reference_length": reference_length
        }
        
        # print(f"    Invoking LLM for reference: {reference_title} (length: {reference_length})")
        # response = self.chain.invoke(inputs, config={"temperature": 0.4}) # Langchain 0.1.0+
        response = self.chain.run(**inputs, temperature=0.4) # 旧版 langchain
        
        # response = self.chain.invoke(inputs, temperature=0.4) # 确保你的Langchain版本支持invoke和config
        # generated_text = response.get('text', '') if isinstance(response, dict) else str(response)
        
        return str(response).strip()


    def generate_chapter_content(self, chapter: dict):
        """
        为当前章节的所有参考文献生成新的段落内容，并拼接它们。
        与原版不同，这里是为每个reference调用一次LLM。
        """
        chapter_main_title = chapter["title"]
        references = chapter.get("references", []) # 使用 .get 以防 "references" 不存在
        
        generated_paragraphs_for_chapter = []

        if not references:
            print(f"    No references found for chapter: {chapter_main_title}")
            return "[信息] 章节没有参考文献内容可供生成。"

        print(f"  Processing {len(references)} references for chapter '{chapter_main_title}'...")
        for i, ref in enumerate(references):
            # print(f"    Processing reference {i+1}/{len(references)}...")
            # 假设每个 ref 字典有 "title", "summary", "paragraph"
            # 如果你的 'ref' 结构不同 (例如 'ref["paragraph"]' 才是实际内容), 你需要调整
            # 这里的 'ref' 结构需要符合 generate_paragraph_for_reference 的期望
            # 例如，如果 'ref' 已经是 {"title": "ref title", "paragraph": "content", "summary": "sum"}
            # 那么直接传递 ref 即可
            
            # 我们需要确保 ref 对象包含 "title", "summary", "paragraph" 键
            # 原始代码中 ref["paragraph"] 是内容, 没有明确的 ref["title"] 和 ref["summary"]
            # 我们需要假设或构建它们
            current_ref_data = {
                "title": ref.get("reference_title", f"Reference {i+1}"), # 尝试获取，否则用占位符
                "summary": ref.get("reference_summary", "Not available"), # 尝试获取，否则用占位符
                "paragraph": ref.get("paragraph", "") # 这是原始代码中的内容
            }
            #print('current_ref_data', current_ref_data)

            try:
                new_paragraph = self.generate_paragraph_for_reference(chapter_main_title, current_ref_data)
                if new_paragraph: # 只有在成功生成且内容非空时才添加
                    print('new_paragraph', new_paragraph)
                    generated_paragraphs_for_chapter.append(new_paragraph)
            except Exception as e:
                error_msg = f"[错误] 处理章节 '{chapter_main_title}' 中的参考文献 '{current_ref_data['title']}' 失败: {e}"
                print(f"    ❌ {error_msg}")
                generated_paragraphs_for_chapter.append(error_msg)
        
        return "\n\n".join(generated_paragraphs_for_chapter)

    def generate_all_chapters(self, chapters: list):
        """
        批量处理所有章节并返回生成结果。
        """
        results = []
        for i, chapter_data in enumerate(chapters):
            print(f"📘 正在处理第 {i+1} 章：{chapter_data['title']}")
            try:
                # generate_combined_paragraph 已被 generate_chapter_content 替代
                generated_content = self.generate_chapter_content(chapter_data)
                results.append({
                    "title": chapter_data["title"],
                    "generated_content": generated_content # 键名修改以反映内容
                })
            except Exception as e:
                print(f"❌ 错误：章节 {chapter_data['title']} 处理失败，原因：{e}")
                results.append({
                    "title": chapter_data["title"],
                    "generated_content": f"[错误] 无法生成该章节内容：{e}"
                })
        return results

if __name__ == '__main__':
    data = [{'title': ['一、预算编制说明', '1、项目概况'], 'length': 2458, 'references': [{'title': ['第一章  绪言'],
                                                                          'paragraph': '“内蒙古四子王旗小南山一带铜镍多金属矿区块优选调查评价”系内蒙古自治区2025年第一批地质勘查基金项目，项目编号：2025-JC09，任务书编号：[2025]基础-09。招标人内蒙古自治区测绘地理信息中心以公开招标方式优选勘查单位，委托内蒙古自治区公共资源交易中心在内蒙古自治区公共资源交易平台(内蒙古自治区自然资源网上交易系统)上实施招投标活动；招标代理机构是内蒙古亿和全过程工程项目管理有限公司，招标编号：CHDL-2025-2-89。我单位就该项目进行了认真资料收集、综合整理和综合研究、实地踏勘，按照招标文件相关技术要求编写了标书。',
                                                                          'length': 270,
                                                                          'summary': '摘要：  \n内蒙古四子王旗小南山一带铜镍多金属矿区块优选调查评价项目（编号：2025-JC09）是内蒙古自治区2025年第一批地质勘查基金项目。该项目由内蒙古自治区测绘地理信息中心通过公开招标方式选择勘查单位，委托内蒙古自治区公共资源交易中心在自治区公共资源交易平台实施招投标活动，招标代理机构为内蒙古亿和全过程工程项目管理有限公司（招标编号：CHDL-2025-2-89）。项目旨在对目标区域进行地质勘查与资源评价。我单位通过资料收集、综合研究及实地踏勘，按照招标文件要求完成了标书编制。',
                                                                          'id': 0},
                                                                         {'title': ['第一章  绪言', '第一节  基本情况', '1、项目概况'],
                                                                          'paragraph': [
                                                                           '项目名称：内蒙古四子王旗小南山一带铜镍多金属矿区块优选调查评价；',
                                                                           '项目编号：2025-JC09；', '工作起止年限：2025年1月～2029年1月；',
                                                                           '工作区范围(2000国家大地坐标系)：',
                                                                           '①111°08′19″，41°43′49″；',
                                                                           '②111°08′19″，41°57′01″；',
                                                                           '③111°37′47″，41°57′01″；',
                                                                           '④111°37′47″，41°46′22″；',
                                                                           '⑤111°29′57″，41°43′49″；',
                                                                           '涉及1∶5万国际标准图幅6幅：小白林地幅（K49E013013）、白林地幅（K49E014013）、打忽拉幅（K49E013014）、大井坡幅（K49E014014）、后点力素呼洞幅（K49E013015）、西海卜子幅（K49E014015）。',
                                                                           '面积971km2。'], 'length': 330,
                                                                          'summary': '摘要：  \n项目名称为“内蒙古四子王旗小南山一带铜镍多金属矿区块优选调查评价”，编号2025-JC09，计划于2025年1月至2029年1月实施。工作区位于内蒙古四子王旗小南山地区，覆盖面积971平方公里，地理范围由五个坐标点界定，并涉及6幅1∶5万国际标准图幅。该项目旨在对区域内铜镍多金属矿资源进行优选调查与评价，以明确矿产资源潜力和分布特征。',
                                                                          'id': 1},
                                                                         {'title': ['第一章  绪言', '第一节  基本情况', '5、预期成果'],
                                                                          'paragraph': [
                                                                           '5.1、提交《内蒙古四子王旗小南山一带铜镍多金属矿区块优选调查评价报告》及相应的附图、附表、附件、电子数据光盘。',
                                                                           '5.2、提交可供进一步工作的勘查区块2～3处。'], 'length': 79,
                                                                          'summary': '摘要：  \n报告要求提交《内蒙古四子王旗小南山一带铜镍多金属矿区块优选调查评价报告》，包括附图、附表、附件及电子数据光盘，并提出2～3处可供进一步勘查的矿产区块。主要内容涉及对铜镍多金属矿的调查评价及后续勘查工作的区块优选。',
                                                                          'id': 5}, {'title': ['第一章  绪言', '第三节  野外踏勘'],
                                                                                     'paragraph': [
                                                                                      '小南山一带近年来在铜镍矿找寻方面取得了丰硕成果。投标单位积极响应“国家新一轮找矿突破战略行动”、“内蒙古自治区战略性矿产找矿行动十四五实施方案”精神，为实现关键战略性矿产铜镍矿的增储上产，对四子王旗一带1∶50万重力，1∶20万化探，1∶5万地磁、航磁、化探及相关典型铜镍矿床资料进行了综合研究，认为该区虽在铜镍找矿方面取得了较大突破，但关于矿床成因及找矿标志的归纳总结工作做的较少，进一步找矿潜力大。',
                                                                                      '为事半功倍，更有针对性地开展各项找矿工作，投标单位于2025年1月组织有关技术人员对工作区进行了系统实地踏勘。'],
                                                                                     'length': 256,
                                                                                     'summary': '小南山地区在铜镍矿找矿方面取得显著成果，但关于矿床成因和找矿标志的研究仍显不足，进一步找矿潜力较大。为落实国家及内蒙古自治区的找矿战略行动，投标单位基于现有地质资料开展综合研究，并计划于2025年1月组织技术人员进行实地踏勘，以更高效、有针对性地推进铜镍矿找矿工作，助力关键战略性矿产的增储上产。',
                                                                                     'id': 10},
                                                                        {'title': ['第一章  绪言', '第四节  矿权设置'],
                                                                                      'paragraph': [
                                                                                       '根据最新矿权查询，涉及调查区及周边范围目前设有18个探矿权（包含12个基金项目），8个采矿权，详见图1-19、表1-2、表1-3。'],
                                                                                      'length': 65,
                                                                                      'summary': '摘要: 最新矿权查询显示，调查区及周边范围内设有18个探矿权（其中12个为基金项目）和8个采矿权，具体信息参见图1-19、表1-2和表1-3。',
                                                                                      'id': 14}, ]}]
    generator = ParagraphGenerator(dashscope_api_key='9ae4915a2829465c')
    result = generator.generate_all_chapters(data)
    print(result)
