import requests
import json
from config import PUSHPLUS_JIJIN


def send_to_pushplus(title: str, content: str, template: str = "markdown") -> bool:
    if not PUSHPLUS_JIJIN:
        print("❌ PushPlus token 未配置")
        return False
    url = "https://www.pushplus.plus/send"
    payload = {
        "token": PUSHPLUS_JIJIN,
        "title": title,
        "content": content,
        "channel": "wechat",
        "template": template
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        result = r.json()
        if result.get("code") == 200:
            print("✅ PushPlus 推送成功")
            return True
        else:
            print(f"❌ 推送失败: {result}")
            return False
    except Exception as e:
        print(f"❌ 推送异常: {e}")
        return False
