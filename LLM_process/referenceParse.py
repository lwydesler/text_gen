
import os
# Use Tongyi from langchain_community which integrates with DashScope/Bailian
from langchain_community.llms import Tongyi
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv # Optional: for loading .env files
import dashscope 
dashscope.save_api_key('sk-ff2f7a46bc0f412c9ae4915a2829465c')
# Optional: Load environment variables from a .env file if you have one
load_dotenv()
from typing import List, Dict, Any, Optional # Added type hints
# class SummaryGenerator:
#     def __init__(self, model_name="qwen-plus"):
#         """初始化摘要生成器

#         Args:
#             model_name (str): 要使用的 DashScope/Bailian 模型名称。
#                               常见选项: "qwen-turbo", "qwen-plus", "qwen-max",
#                               "qwen-max-longcontext" 等。
#                               请参考 DashScope 文档获取最新列表和适用场景。
#         """
#         # 从环境变量获取 API Key
#         #api_key = os.getenv("DASHSCOPE_API_KEY")
#         api_key = 'sk-ff2f7a46bc0f412c9ae4915a2829465c'
#         #api_key = API_key
#         if not api_key:
#             raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量")

#         # 初始化 Tongyi (Qwen) 模型 via DashScope
#         # 您可以在这里指定不同的模型名称
#         self.llm = Tongyi(
#             model_name=model_name,
#             dashscope_api_key=api_key
#             # 可以添加其他参数，例如 temperature, top_p 等
#             # temperature=0.7
#         )

#         # 定义摘要生成的提示模板 (保持不变)
#         self.summary_template = """
#         请为以下文本生成一个简洁的摘要，包含文档的主要内容和关键观点:

#         {text}

#         摘要:
#         """

#         self.prompt = PromptTemplate(
#             input_variables=["text"],
#             template=self.summary_template
#         )

#         # 创建 LLM 链 (保持不变)
#         self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

#     def generate_section_summary(self, section_text):
#         """为单个章节生成摘要

#         Args:
#             section_text: 章节文本内容

#         Returns:
#             str: 章节摘要 或 None (如果出错)
#         """
#         if not section_text or section_text.isspace():
#              print("警告: 章节文本为空，跳过摘要生成。")
#              return "" # 返回空字符串而不是 None，以便后续拼接

#         try:
#             # 使用 run 方法调用 LLMChain
#             summary = self.chain.run(text=section_text)
#             # 或者使用 invoke for more structured output/streaming if needed later
#             # response = self.chain.invoke({"text": section_text})
#             # summary = response['text'] # Adjust based on actual output structure if using invoke
#             return summary.strip() #去除可能的多余空格
#         except Exception as e:
#             print(f"生成章节摘要时发生错误: {str(e)}")
#             # 考虑更具体的异常处理，例如 API 错误、速率限制等
#             return None

#     def generate_document_summary(self, sections):
#         """为整个文档生成摘要

#         Args:
#             sections (dict): 文档各章节内容的字典 {章节标题: 章节内容}

#         Returns:
#             dict: 包含各章节摘要和整体摘要的字典, 或 None (如果出错)
#         """
#         if not sections:
#             print("错误: 输入的章节字典为空。")
#             return None

#         try:
#             # 为每个章节生成摘要
#             section_summaries = {}
#             all_section_texts_for_overall = [] # 用于收集原始文本或摘要以生成总摘要

#             print("开始生成章节摘要...")
#             for i, (title, content) in enumerate(sections.items()):
#                 print(f"  处理章节 {i+1}/{len(sections)}: {title}")
#                 summary = self.generate_section_summary(content)
#                 if summary is not None: # 检查是否成功生成
#                     section_summaries[title] = summary
#                     all_section_texts_for_overall.append(summary) # 使用章节摘要生成总摘要
#                     # 或者，如果章节摘要太短，可以考虑拼接原始文本的一部分或全部
#                     # all_section_texts_for_overall.append(content) # 另一种策略
#                 else:
#                      print(f"  警告: 章节 '{title}' 摘要生成失败，将跳过此章节。")


#             if not section_summaries:
#                  print("错误：所有章节摘要均生成失败。")
#                  return None

#             # 将所有成功的章节摘要组合，生成整体摘要
#             # 注意：组合摘要可能很长，检查是否超过模型上下文限制
#             print("\n开始生成整体摘要...")
#             combined_summary_text = "\n\n".join(all_section_texts_for_overall) # 使用换行符分隔

#             # 检查组合文本是否为空
#             if not combined_summary_text or combined_summary_text.isspace():
#                 print("警告：没有可用于生成整体摘要的内容。")
#                 overall_summary = "未能生成整体摘要，因为没有成功的章节摘要。"
#             else:
#                 # 调用 generate_section_summary 方法来生成整体摘要
#                 # （复用相同的逻辑和提示）
#                 overall_summary = self.generate_section_summary(combined_summary_text)
#                 if overall_summary is None:
#                      print("错误：生成整体摘要失败。")
#                      overall_summary = "生成整体摘要时出错。" # 提供一个错误信息


#             print("摘要生成完成。")
#             return {
#                 "section_summaries": section_summaries,
#                 "overall_summary": overall_summary
#             }

#         except Exception as e:
#             print(f"生成文档摘要时发生严重错误: {str(e)}")
#             return None

# class SummaryGenerator:
#     def __init__(self, model_name="qwen-plus"):
#         """初始化摘要生成器

#         Args:
#             model_name (str): 要使用的 DashScope/Bailian 模型名称。
#                               常见选项: "qwen-turbo", "qwen-plus", "qwen-max",
#                               "qwen-max-longcontext" 等。
#                               请参考 DashScope 文档获取最新列表和适用场景。
#         """
#         # 从环境变量获取 API Key (Recommended)
#         # api_key = os.getenv("DASHSCOPE_API_KEY")
#         # Using the provided key for this example
#         current_api_key = 'sk-ff2f7a46bc0f412c9ae4915a2829465c' # Use the key defined above
#         if not current_api_key:
#             raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量或在代码中提供 API Key")

#         # 初始化 Tongyi (Qwen) 模型 via DashScope
#         self.llm = Tongyi(
#             model_name=model_name,
#             dashscope_api_key=current_api_key
#             # temperature=0.7 # Optional: Add other parameters
#         )

#         # 定义摘要生成的提示模板 (保持不变)
#         self.summary_template = """
#         请为以下文本生成一个简洁的摘要，包含文档的主要内容和关键观点:

#         {text}

#         摘要:
#         """

#         self.prompt = PromptTemplate(
#             input_variables=["text"],
#             template=self.summary_template
#         )

#         # 创建 LLM 链 (保持不变)
#         self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

#     def generate_section_summary(self, section_text: str) -> Optional[str]:
#         """为单个章节生成摘要

#         Args:
#             section_text: 章节文本内容

#         Returns:
#             str: 章节摘要 或 None (如果出错)
#         """
#         if not section_text or section_text.isspace():
#              print("警告: 章节文本为空，跳过摘要生成。")
#              return "" # 返回空字符串而不是 None，以便后续拼接

#         try:
#             # 使用 run 方法调用 LLMChain (simple use case)
#             summary = self.chain.run(text=section_text)
#             # For more control or structured output, consider invoke:
#             # response = self.chain.invoke({"text": section_text})
#             # summary = response.get('text', '') # Adjust key based on actual output
#             return summary.strip() #去除可能的多余空格
#         except Exception as e:
#             print(f"生成章节摘要时发生错误: {str(e)}")
#             # Consider more specific exception handling (e.g., API errors, rate limits)
#             return None

#     def generate_document_summary(self, sections_data: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
#         """为整个文档生成摘要

#         Args:
#             sections_data (List[Dict[str, Any]]): 文档各章节数据的列表。
#               每个字典应包含 'title' (List[str]), 'paragraph' (str),
#               和可选的 'length' (int)。
#               例如:
#               [
#                 {'title': ['引言', '研究背景'], 'paragraph': '...', 'length': 58},
#                 {'title': ['方法', '数据处理'], 'paragraph': '...', 'length': 52},
#                 ...
#               ]

#         Returns:
#             dict: 包含各章节摘要和整体摘要的字典, 或 None (如果出错)
#                   格式: {'section_summaries': { '标题1 - 子标题1': '摘要1', ... }, 'overall_summary': '总摘要'}
#         """
#         if not sections_data:
#             print("错误: 输入的章节数据列表为空。")
#             return None

#         try:
#             section_summaries = {}
#             all_section_texts_for_overall = [] # 用于收集摘要以生成总摘要

#             print("开始生成章节摘要...")
#             for i, section_info in enumerate(sections_data):
#                 # --- Modification Start ---
#                 # Construct a meaningful title key from the list
#                 title_parts = section_info.get('title', [f'未知章节 {i+1}']) # Default title if missing
#                 title_key = " - ".join(title_parts) # Join title parts with " - "

#                 # Get the paragraph content
#                 content = section_info.get('paragraph', '')
#                 # --- Modification End ---

#                 print(f"  处理章节 {i+1}/{len(sections_data)}: {title_key}")

#                 if not content or content.isspace():
#                     print(f"  警告: 章节 '{title_key}' 内容为空，跳过。")
#                     continue # Skip this section if content is empty

#                 summary = self.generate_section_summary(content)

#                 if summary is not None: # Check if summary generation was successful
#                     section_summaries[title_key] = summary
#                     all_section_texts_for_overall.append(summary) # Use section summary for overall summary
#                 else:
#                      print(f"  警告: 章节 '{title_key}' 摘要生成失败，将跳过此章节。")

#             if not section_summaries:
#                  print("错误：所有章节摘要均生成失败。")
#                  return None

#             # Combine successful section summaries to generate the overall summary
#             print("\n开始生成整体摘要...")
#             combined_summary_text = "\n\n".join(all_section_texts_for_overall)

#             # Check if combined text is empty (might happen if all summaries were empty strings)
#             if not combined_summary_text or combined_summary_text.isspace():
#                 print("警告：没有可用于生成整体摘要的内容。")
#                 overall_summary = "未能生成整体摘要，因为没有成功的章节摘要或摘要内容为空。"
#             else:
#                 # Reuse generate_section_summary logic for the overall summary
#                 overall_summary = self.generate_section_summary(combined_summary_text)
#                 if overall_summary is None:
#                      print("错误：生成整体摘要失败。")
#                      overall_summary = "生成整体摘要时出错。" # Provide an error message

#             print("摘要生成完成。")
#             return {
#                 "section_summaries": section_summaries,
#                 "overall_summary": overall_summary
#             }

#         except Exception as e:
#             print(f"生成文档摘要时发生严重错误: {str(e)}")
#             return None

class SummaryGenerator:
    def __init__(self, model_name="qwen-plus", api_key=''):
        """初始化摘要生成器

        Args:
            model_name (str): 要使用的 DashScope/Bailian 模型名称。
                              常见选项: "qwen-turbo", "qwen-plus", "qwen-max",
                              "qwen-max-longcontext" 等。
                              请参考 DashScope 文档获取最新列表和适用场景。
        """
        # 从环境变量获取 API Key (Recommended)
        # api_key = os.getenv("DASHSCOPE_API_KEY")
        # Using the provided key for this example
        current_api_key = api_key  # Use the key defined above
        if not current_api_key:
            raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量或在代码中提供 API Key")

        # 初始化 Tongyi (Qwen) 模型 via DashScope
        self.llm = Tongyi(
            model_name=model_name,
            dashscope_api_key=current_api_key
            # temperature=0.7 # Optional: Add other parameters
        )

        # 定义摘要生成的提示模板 (保持不变)
        self.summary_template = """
        请为以下文本生成一个简洁的摘要，包含文档的主要内容和关键观点:

        {text}

        摘要:
        """

        self.prompt = PromptTemplate(
            input_variables=["text"],
            template=self.summary_template
        )

        # 创建 LLM 链 (保持不变)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def generate_section_summary(self, section_text: str) -> Optional[str]:
        """为单个章节生成摘要

        Args:
            section_text: 章节文本内容

        Returns:
            str: 章节摘要 或 None (如果出错)
        """
        if not section_text or section_text.isspace():
             print("警告: 章节文本为空，跳过摘要生成。")
             return ""  # 返回空字符串而不是 None，以便后续拼接

        try:
            # 使用 run 方法调用 LLMChain (simple use case)
            summary = self.chain.run(text=section_text)
            # For more control or structured output, consider invoke:
            # response = self.chain.invoke({"text": section_text})
            # summary = response.get('text', '') # Adjust key based on actual output
            return summary.strip()  #去除可能的多余空格
        except Exception as e:
            print(f"生成章节摘要时发生错误: {str(e)}")
            # Consider more specific exception handling (e.g., API errors, rate limits)
            return None

    def generate_document_summary(self, document_data: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """为整个文档生成摘要

        Args:
            document_data (List[Dict[str, Any]]): 文档各章节数据的列表。
              每个字典应包含 'title' (List[str]), 'paragraph' (List[str]),
              和可选的 'length' (int)。
              例如:
              [
                {'title': ['引言', '研究背景'], 'paragraph': ['...', '...'], 'length': 58},
                {'title': ['方法', '数据处理'], 'paragraph': ['...', '...'], 'length': 52},
                ...
              ]

        Returns:
            dict: 包含各章节摘要和整体摘要的字典, 或 None (如果出错)
                  格式: {'section_summaries': { '标题1 - 子标题1': '摘要1', ... }, 'overall_summary': '总摘要'}
        """
        if not document_data:
            print("错误: 输入的章节数据列表为空。")
            return None

        try:
            section_summaries = {}
            all_section_texts_for_overall = []  # 用于收集摘要以生成总摘要

            print("开始生成章节摘要...")
            for i, section_info in enumerate(document_data):
                # --- Modification Start ---
                # Construct a meaningful title key from the list
                title_parts = section_info.get('title', [f'未知章节 {i+1}'])  # Default title if missing
                title_key = " - ".join(title_parts)  # Join title parts with " - "

                # 将段落列表拼接为一个字符串
                content = " ".join(section_info.get('paragraph', []))  # Join all paragraphs into a single string
                # --- Modification End ---

                print(f"  处理章节 {i+1}/{len(document_data)}: {title_key}")

                if not content or content.isspace():
                    print(f"  警告: 章节 '{title_key}' 内容为空，跳过。")
                    continue  # Skip this section if content is empty

                summary = self.generate_section_summary(content)

                if summary is not None:  # Check if summary generation was successful
                    section_summaries[title_key] = summary
                    all_section_texts_for_overall.append(summary)  # Use section summary for overall summary
                else:
                    print(f"  警告: 章节 '{title_key}' 摘要生成失败，将跳过此章节。")

            if not section_summaries:
                print("错误：所有章节摘要均生成失败。")
                return None

            # Combine successful section summaries to generate the overall summary
            print("\n开始生成整体摘要...")
            combined_summary_text = "\n\n".join(all_section_texts_for_overall)

            # Check if combined text is empty (might happen if all summaries were empty strings)
            if not combined_summary_text or combined_summary_text.isspace():
                print("警告：没有可用于生成整体摘要的内容。")
                overall_summary = "未能生成整体摘要，因为没有成功的章节摘要或摘要内容为空。"
            else:
                # Reuse generate_section_summary logic for the overall summary
                overall_summary = self.generate_section_summary(combined_summary_text)
                if overall_summary is None:
                    print("错误：生成整体摘要失败。")
                    overall_summary = "生成整体摘要时出错。"  # Provide an error message

            print("摘要生成完成。")
            return {
                "section_summaries": section_summaries,
                "overall_summary": overall_summary
            }

        except Exception as e:
            print(f"生成文档摘要时发生严重错误: {str(e)}")
            return None

# --- 示例用法 ---
if __name__ == "__main__":
    # 确保设置了环境变量 DASHSCOPE_API_KEY

    # 示例章节数据
    # sample_sections = {
    #     "引言": "本文档旨在探讨人工智能在自然语言处理领域的最新进展。我们将回顾关键技术，并讨论其在摘要生成中的应用。目标是提供一个全面的概述。",
    #     "关键技术": "循环神经网络（RNN）和长短期记忆（LSTM）网络曾是序列处理的主流。然而，Transformer 架构及其自注意力机制带来了革命性变化，催生了 BERT、GPT 等大型预训练模型。这些模型在理解上下文和生成连贯文本方面表现出色。",
    #     "摘要生成应用": "基于 Transformer 的模型特别适用于文本摘要任务。它们可以捕捉长距离依赖关系，生成不仅简洁而且保留了原文核心信息的摘要。有两种主要方法：抽取式摘要（选择原文关键句子）和生成式摘要（生成新句子）。目前，生成式摘要因其灵活性而越来越受欢迎。",
    #     "挑战与未来": "尽管取得了巨大进步，但仍存在挑战，如处理超长文档、确保事实准确性以及避免生成偏见。未来的研究方向可能包括更高效的模型架构、更好的多模态融合以及更强的可解释性。"
    # }

    # # 选择一个模型，确保你的 API Key 有权限访问它
    # model_to_use = "qwen-turbo"
    # # model_to_use = "qwen-plus" # 效果通常更好，但可能稍慢/贵
    # # model_to_use = "qwen-max" # 效果可能最好，但可能更慢/贵

    # try:
    #     # 创建生成器实例
    #     generator = SummaryGenerator(model_name=model_to_use)

    #     # 生成文档摘要
    #     summary_result = generator.generate_document_summary(sample_sections)

    #     # 打印结果
    #     if summary_result:
    #         print("\n--- 章节摘要 ---")
    #         for title, summary in summary_result["section_summaries"].items():
    #             print(f"[{title}]: {summary}")

    #         print("\n--- 整体摘要 ---")
    #         print(summary_result["overall_summary"])
    #     else:
    #         print("\n未能成功生成摘要。")

    # except ValueError as ve:
    #     print(f"初始化错误: {ve}")
    # except Exception as ex:
    #     print(f"运行示例时发生意外错误: {ex}")
    # 示例输入数据
    document_data = [
        {'title': ['引言', '研究背景'], 'paragraph': ['随着科技进步，人工智能在各领域的应用日益广泛，尤其在自然语言处理方面取得了重大突破，这为许多行业带来了效率提升和创新机遇。'], 'length': 80},
        {'title': ['方法', '数据处理'], 'paragraph': ['本研究采用了多种数据清洗技术，包括去重、标准化和异常值处理。我们使用先进的算法对数据集进行预处理，以确保输入模型的训练数据具有高质量和一致性。'], 'length': 95},
        {'title': ['结果讨论'], 'paragraph': '', 'length': 0},
        {'title': ['结论', '研究展望'], 'paragraph': ['研究表明该模型效果显著。未来，人工智能将更多地与领域知识结合，通过持续学习和模型优化，推动各行业的智能化转型和深层次变革。'], 'length': 88}
    ]

    # 创建生成器实例 (可以选择不同模型)
    # generator = SummaryGenerator(model_name="qwen-turbo")
    apikey = ''
    generator = SummaryGenerator(model_name="qwen-plus", api_key=apikey)

    # 生成摘要
    summary_output = generator.generate_document_summary(document_data)

    # 打印结果
    if summary_output:
        print("\n--- 生成的摘要 ---")
        print("\n章节摘要:")
        for title, summary in summary_output['section_summaries'].items():
            print(f"  {title}: {summary}")
        print(f"\n整体摘要:\n{summary_output['overall_summary']}")
    else:
        print("\n未能成功生成文档摘要。")