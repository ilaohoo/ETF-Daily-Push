from datetime import datetime
from data_fetcher import fetch_all_etf_spot, get_top_gainers_losers
from ai_analyzer import get_ai_analysis
from push_sender import send_to_pushplus


def main():
    print("=== ETF日报 AI 推送系统启动 ===")
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 1. 获取全市场ETF行情数据
    print("正在获取全市场ETF行情...")
    try:
        df = fetch_all_etf_spot()
        print(f"成功获取 {len(df)} 只ETF数据")
    except Exception as e:
        print(f"数据获取失败: {e}")
        return

    # 2. 提取涨幅前20和跌幅前20
    gainers, losers = get_top_gainers_losers(df, n=20)
    print(f"涨幅榜前20: {len(gainers)} 只")
    print(f"跌幅榜前20: {len(losers)} 只")

    # 3. 调用AI生成分析日报
    print("正在调用DeepSeek API生成AI分析...")
    ai_report = get_ai_analysis(gainers, losers)

    # 4. 组装推送标题和内容
    today_str = datetime.now().strftime("%Y-%m-%d")
    title = f"📊 ETF投资日报 {today_str}"
    # AI报告本身就是Markdown，直接作为content
    full_content = ai_report

    # 可选：在AI报告末尾追加一句免责声明（AI生成时可能已包含，但可再强调）
    full_content += "\n\n> ⚠️ **免责声明**：本报告由AI基于公开数据生成，仅供参考，不构成投资建议。基金历史业绩不代表未来表现，投资需谨慎。"

    # 5. 推送到微信
    print("正在通过PushPlus推送...")
    success = send_to_pushplus(title, full_content, template="markdown")
    if success:
        print("推送完成")
    else:
        print("推送失败，请检查网络或token")

    print("=== 程序结束 ===")


if __name__ == "__main__":
    main()
