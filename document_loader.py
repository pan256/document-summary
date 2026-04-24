"""
文档加载器
支持 PDF、Word、TXT 等格式
"""
import os
from typing import List
from PyPDF2 import PdfReader
from docx import Document


class DocumentLoader:
    """文档加载器，支持多种格式"""

    @staticmethod
    def load_pdf(file_path: str) -> str:
        """加载 PDF 文件"""
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()

    @staticmethod
    def load_word(file_path: str) -> str:
        """加载 Word 文件"""
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()

    @staticmethod
    def load_txt(file_path: str) -> str:
        """加载 TXT 文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()

    @staticmethod
    def load(file_path: str) -> str:
        """根据文件类型自动加载"""
        ext = os.path.splitext(file_path)[1].lower()

        if ext == '.pdf':
            return DocumentLoader.load_pdf(file_path)
        elif ext in ['.docx', '.doc']:
            return DocumentLoader.load_word(file_path)
        elif ext == '.txt':
            return DocumentLoader.load_txt(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {ext}")

    @staticmethod
    def get_supported_extensions() -> List[str]:
        """获取支持的文件格式"""
        return ['.pdf', '.docx', '.doc', '.txt']