from datetime import datetime
from data_fetcher import fetch_all_etf_spot, get_top_gainers_losers
from global_fetcher import fetch_global_market_data
from ai_analyzer import get_ai_analysis
from push_sender import send_to_pushplus
from config import ETF_TOP_N


def main():
    print("=== ETF日报 AI 推送系统启动 ===")
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 1. 获取A股全市场ETF数据
    print("正在获取A股ETF行情...")
    try:
        df = fetch_all_etf_spot()
        print(f"成功获取 {len(df)} 只ETF")
    except Exception as e:
        print(f"数据获取失败: {e}")
        return

    # 2. 提取涨跌幅榜
    gainers, losers = get_top_gainers_losers(df, n=ETF_TOP_N)
    print(f"涨幅榜: {len(gainers)}只, 跌幅榜: {len(losers)}只")

    # 3. 获取海外市场数据
    print("正在获取海外市场数据...")
    global_data = fetch_global_market_data()

    # 4. AI分析
    print("正在调用DeepSeek API...")
    ai_report = get_ai_analysis(gainers, losers, global_data)

    # 5. 推送
    title = f"📊 ETF投资日报 {datetime.now().strftime('%Y-%m-%d')}"
    success = send_to_pushplus(title, ai_report, template="markdown")
    if success:
        print("推送完成")
    else:
        print("推送失败")

    print("=== 程序结束 ===")


if __name__ == "__main__":
    main()
