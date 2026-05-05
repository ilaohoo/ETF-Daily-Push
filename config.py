import os
from dotenv import load_dotenv

# 加载 .env 文件（本地开发使用，GitHub Actions 中该文件不存在但无害）
load_dotenv()

# PushPlus 配置
PUSHPLUS_TOKEN = os.getenv("PUSHPLUS_TOKEN", "")

# DeepSeek 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
