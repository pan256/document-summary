"""
配置文件
"""
import os

# 在代码中设置 API Key
os.environ["DASHSCOPE_API_KEY"] = "sk-ed957a9e7366449dafba848c702eb166"  # 替换为你的实际API Key

# API配置
API_KEY = os.getenv("DASHSCOPE_API_KEY", "")

# 模型配置
MODEL_NAME = "qwen-plus"  # 阿里云模型

# 摘要配置
MAX_CHUNK_SIZE = 2000  # 文档分块大小
SUMMARY_MAX_LENGTH = 500  # 摘要最大长度