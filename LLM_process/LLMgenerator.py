from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

# 模板定义
template = """
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

prompt = PromptTemplate(
    input_variables=["chapter_title", "reference_title", "reference_summary", "reference_paragraph", "reference_length"],
    template=template
)

llm = ChatOpenAI(temperature=0.7, model="gpt-4")  # 你也可以换成 gpt-3.5
chain = LLMChain(llm=llm, prompt=prompt)