"""
摘要生成器
使用 LLM 生成文档摘要
"""
from langchain_community.chat_models import ChatTongyi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import API_KEY, MODEL_NAME, MAX_CHUNK_SIZE, SUMMARY_MAX_LENGTH


class SummaryGenerator:
    """摘要生成器"""

    def __init__(self):
        self.llm = self._init_llm()
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=MAX_CHUNK_SIZE,
            chunk_overlap=200,
            separators=["\n\n", "\n", "。", "！", "？", "；", " ", ""]
        )

    def _init_llm(self):
        """初始化 LLM"""
        if not API_KEY:
            raise ValueError("请设置 API_KEY")

        # 使用阿里云百炼模型
        return ChatTongyi(
            model=MODEL_NAME,
            dashscope_api_key=API_KEY,
            temperature=0.3,
            max_tokens=SUMMARY_MAX_LENGTH
        )

    def generate_summary(self, text: str) -> str:
        """生成文档摘要"""
        # 文档分块
        chunks = self.splitter.split_text(text)

        # 直接使用 LLM 生成摘要
        if len(chunks) == 1:
            # 单块直接摘要
            summary = self._direct_summary(chunks[0])
        else:
            # 多块合并后摘要
            combined = "\n\n".join(chunks[:3])  # 取前3块
            summary = self._direct_summary(combined)

        return summary

    def _direct_summary(self, text: str) -> str:
        """直接生成摘要"""
        prompt = f"""请对以下文档内容进行精简摘要，提取关键信息：

{text}

摘要要求：
1. 突出核心观点和关键信息
2. 语言简洁，不超过300字
3. 保持逻辑清晰

摘要："""

        response = self.llm.invoke(prompt)
        return response.content

    def extract_key_points(self, text: str) -> list:
        """提取关键要点"""
        prompt = f"""请从以下文档中提取3-5个关键要点：

{text}

关键要点（用简洁的语言列出）："""

        response = self.llm.invoke(prompt)
        return response.content