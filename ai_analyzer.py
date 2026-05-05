import pandas as pd
import requests
from typing import Optional, Dict, Any
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL


def build_prompt(
    gainers: pd.DataFrame,
    losers: pd.DataFrame,
    global_data: Optional[Dict[str, Any]] = None
) -> str:
    # 格式化国内涨跌榜
    gainer_text = ""
    for _, row in gainers.iterrows():
        gainer_text += f"- {row['名称']}（{row['代码']}）：{row['涨跌幅']}，成交额{row['成交额']}\n"
    loser_text = ""
    for _, row in losers.iterrows():
        loser_text += f"- {row['名称']}（{row['代码']}）：{row['涨跌幅']}，成交额{row['成交额']}\n"

    global_section = ""
    if global_data:
        global_section = f"""
## 海外市场概览（{global_data.get('date', '最新交易日')}）
- **美股三大指数**：道琼斯 {global_data.get('dji_pct', 'N/A')}，标普500 {global_data.get('spx_pct', 'N/A')}，纳斯达克 {global_data.get('ixic_pct', 'N/A')}
- **关键个股**：美光科技 {global_data.get('mu_pct', 'N/A')}（创新高：{global_data.get('mu_high', 'N/A')}），闪迪 {global_data.get('wdc_pct', 'N/A')}，英伟达 {global_data.get('nvda_pct', 'N/A')}
- **亚太市场**：韩国KOSPI {global_data.get('kospi_pct', 'N/A')}，恒生科技 {global_data.get('hstec_pct', 'N/A')}
- **汇率与商品**：美元指数 {global_data.get('dxy_pct', 'N/A')}，原油 {global_data.get('oil_pct', 'N/A')}，黄金 {global_data.get('gold_pct', 'N/A')}
- **QDII动态**：{global_data.get('qdii_note', '')}
"""

    prompt = f"""你是一位专业的ETF投资分析师，覆盖A股、港股及海外市场。请基于以下数据，生成一份专业的投资日报。

## 今日A股ETF涨幅前20：
{gainer_text}

## 今日A股ETF跌幅前20：
{loser_text}
{global_section}
请输出**Markdown格式**的分析报告，包含以下六个部分：

### 1. 市场全景扫描
- 从A股涨跌榜总结主线（领涨/领跌板块），分析核心驱动因素。
- 结合海外市场走势，说明海外风险偏好对A股科技、资源等板块的传导。

### 2. 最大亮点与风险
- 点评A股涨幅第一和跌幅第一的ETF。
- 若海外标志性个股（如美光、英伟达）异动，点明其对国内相关产业链的映射。

### 3. 资金流向与板块轮动
- 基于A股涨跌榜和成交额，判断资金偏好（宽基/行业/主题）。
- 结合海外资金动向（如半导体强弱、亚太联动），预判短期风格切换。

### 4. 未来看好的基金方向（含海外）
- **国内部分**：推荐3-5个A股ETF主题或具体代码，说明理由。
- **海外部分**：推荐可通过**支付宝QDII**或**跨境ETF（A股账户）**配置的海外方向（例如：纳斯达克100ETF、半导体行业ETF、海外创新药ETF等），并说明渠道特点（QDII适合场外定投，跨境ETF支持T+0）。

### 5. 操作策略建议
- 按风险偏好给出三类配置：积极进取型（科技/半导体）、均衡型（科技+资源+红利）、保守型（短融债/红利低波）。
- 对于海外方向，建议跨境资产占比不超过总仓位的20%-30%。

### 6. 风险提示
- 列出当前国内外主要风险（地缘政治、汇率波动、QDII额度限制、ETF溢价等）。

要求：语言专业、简洁，开头加粗概括今日市场特征（含海外影响）。末尾加免责声明：以上内容由AI生成，仅供参考，不构成投资建议。基金历史业绩不代表未来表现。"""
    return prompt


def get_ai_analysis(
    gainers: pd.DataFrame,
    losers: pd.DataFrame,
    global_data: Optional[Dict[str, Any]] = None
) -> str:
    if not DEEPSEEK_API_KEY:
        return "错误：未配置DEEPSEEK_API_KEY，请检查环境变量。"

    prompt = build_prompt(gainers, losers, global_data)
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是专业的ETF投资分析师，擅长国内外行情分析并给出配置建议。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 3000
    }
    try:
        resp = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ AI分析失败：{str(e)}"
