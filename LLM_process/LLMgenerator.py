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
    def __init__(self, model_name="qwen-turbo", dashscope_api_key='sk-ff2f7a46bc0f412c9ae4915a2829465c'): # 默认模型设为qwen-turbo或你选择的
        """
        初始化 ParagraphGenerator。
        :param model_name: Tongyi 模型的名称，例如 "qwen-turbo", "qwen-plus", "qwen-max"。
        :param dashscope_api_key: DashScope API Key. 如果为 None, 会尝试从环境变量 'DASHSCOPE_API_KEY' 读取。
        """
        self.model_name = model_name
        
        if dashscope_api_key:
            current_api_key = dashscope_api_key
        else:
            current_api_key = os.environ.get("DASHSCOPE_API_KEY")
            # current_api_key = 'sk-ff2f7a46bc0f412c9ae4915a2829465c' # 或者直接硬编码，但不推荐生产环境

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
            input_variables=["chapter_title", "reference_title", "reference_summary", "reference_paragraph", "reference_length"],
            template="""
你是一位专业的写作助手，请你根据下列段落内容和摘要，生成与章节标题匹配的新段落内容。要求如下：
1. 保持内容围绕章节标题展开；
2. 使用原段落的核心信息，但可以改写、重组或扩展；
3. 控制输出字数与原段落字数相近（误差不超过 ±20%）；
4. 保持表达通顺、学术风格一致。

【章节标题】：{chapter_title}
【原段落标题】：{reference_title}
【原段落摘要】：{reference_summary}
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
        response = self.chain.run(inputs, temperature=0.4) # 旧版 langchain
        
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

            try:
                new_paragraph = self.generate_paragraph_for_reference(chapter_main_title, current_ref_data)
                if new_paragraph: # 只有在成功生成且内容非空时才添加
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
