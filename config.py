import os
from dotenv import load_dotenv

load_dotenv()

# PushPlus 配置
PUSHPLUS_JIJIN = os.getenv("PUSHPLUS_JIJIN", "")

# DeepSeek 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# 其他可选配置
ETF_TOP_N = 20  # 涨幅/跌幅榜数量
