import requests
import json
from config import PUSHPLUS_TOKEN


def send_to_pushplus(title: str, content: str, template: str = "markdown") -> bool:
    """
    通过PushPlus推送消息到微信
    :param title: 消息标题
    :param content: 消息内容（支持Markdown）
    :param template: 模板类型，推荐'markdown'
    """
    if not PUSHPLUS_TOKEN:
        print("❌ PushPlus token 未配置，请检查环境变量或GitHub Secrets")
        return False

    url = "https://www.pushplus.plus/send"
    payload = {
        "token": PUSHPLUS_TOKEN,
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
