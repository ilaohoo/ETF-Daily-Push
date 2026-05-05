import json
import requests
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL
import pandas as pd


def build_prompt(gainers: pd.DataFrame, losers: pd.DataFrame) -> str:
    """构建AI分析提示词，要求生成日报并给出未来看好的基金方向"""
    # 格式化涨幅榜
    gainer_text = ""
    if not gainers.empty:
        for idx, row in gainers.iterrows():
            gainer_text += f"- {row['名称']}（{row['代码']}）：{row['涨跌幅']}，成交额{row['成交额']}\n"
    else:
        gainer_text = "无"

    loser_text = ""
    if not losers.empty:
        for idx, row in losers.iterrows():
            loser_text += f"- {row['名称']}（{row['代码']}）：{row['涨跌幅']}，成交额{row['成交额']}\n"
    else:
        loser_text = "无"

    prompt = f"""你是一位专业的ETF投资分析师。请基于今日全市场ETF的行情数据，完成以下任务。

## 今日涨幅前20 ETF：
{gainer_text}

## 今日跌幅前20 ETF：
{loser_text}

请输出一份**Markdown格式**的投资日报，包括以下五个部分：

1. **市场全景扫描**：从涨幅榜和跌幅榜中提炼今日市场的主线方向（哪些板块领涨、哪些板块领跌），分析核心驱动因素。
2. **最大亮点与风险**：点评涨幅第一和跌幅第一的ETF，分析其背后原因。
3. **资金流向与板块轮动**：结合涨跌榜情况，判断当前资金偏好哪些类型ETF，以及是否出现风格切换迹象。
4. **未来看好基金方向**：基于今日数据和近期市场逻辑，给出未来**最值得关注的3-5个ETF主题或具体基金代码**，并说明看好的逻辑。
5. **风险提示**：简要列出当前市场需要注意的风险点。

要求：语言专业、简洁、客观，不要包含“根据AI模型”等表述，直接输出分析内容。开头加一句概括今日市场特征的话（加粗）。最后附上免责声明：以上内容由AI生成，仅供参考，不构成投资建议，基金历史业绩不代表未来表现。"""

    return prompt


def get_ai_analysis(gainers: pd.DataFrame, losers: pd.DataFrame) -> str:
    """调用DeepSeek API获取分析报告"""
    if not DEEPSEEK_API_KEY:
        return "错误：未配置DEEPSEEK_API_KEY，请检查环境变量或GitHub Secrets。"

    prompt = build_prompt(gainers, losers)

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个专业的ETF投资分析师，擅长从行情数据中提取有价值的投资信号并给出清晰的未来展望。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2500
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        ai_content = result["choices"][0]["message"]["content"]
        return ai_content
    except Exception as e:
        return f"⚠️ AI分析生成失败：{str(e)}。\n\n请稍后重试或检查API Key配置。"
