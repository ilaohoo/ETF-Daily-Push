import requests
import json
from config import PUSHPLUS_JIJIN   # 修改导入名称


def send_to_pushplus(title: str, content: str, template: str = "markdown") -> bool:
    if not PUSHPLUS_JIJIN:
        print("❌ PushPlus token 未配置，请检查环境变量或GitHub Secrets")
        return False

    url = "https://www.pushplus.plus/send"
    payload = {
        "token": PUSHPLUS_JIJIN,      # 使用新变量名
        "title": title,
        "content": content,
        "channel": "wechat",
        "template": template
    }
    headers = {"Content-Type": "application/json"}

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        result = resp.json()
        if result.get("code") == 200:
            print("✅ PushPlus 推送成功")
            return True
        else:
            print(f"❌ PushPlus 推送失败: {result}")
            return False
    except Exception as e:
        print(f"❌ 推送异常: {e}")
        return False
