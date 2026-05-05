import os
from dotenv import load_dotenv

load_dotenv()

# 修改此处：变量名改为 PUSHPLUS_JIJIN
PUSHPLUS_JIJIN = os.getenv("PUSHPLUS_JIJIN", "")

# DeepSeek 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
