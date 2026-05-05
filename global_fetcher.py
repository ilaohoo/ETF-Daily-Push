import yfinance as yf
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_global_market_data() -> dict:
    """获取海外主要指数、个股、商品数据，用于AI分析"""
    tickers = {
        'spx': '^GSPC',      # 标普500
        'ixic': '^IXIC',     # 纳斯达克
        'dji': '^DJI',       # 道琼斯
        'mu': 'MU',          # 美光科技
        'wdc': 'WDC',        # 闪迪
        'nvda': 'NVDA',      # 英伟达
        'kospi': '^KS11',    # 韩国KOSPI
        'hstec': '^HSTECH',  # 恒生科技
        'dxy': 'DX-Y.NYB',   # 美元指数
        'oil': 'CL=F',       # 原油期货
        'gold': 'GC=F'       # 黄金期货
    }
    data = {'date': datetime.now().strftime('%Y-%m-%d')}

    for name, ticker in tickers.items():
        try:
            ticker_obj = yf.Ticker(ticker)
            hist = ticker_obj.history(period="2d")
            if len(hist) >= 2:
                prev = hist['Close'].iloc[-2]
                curr = hist['Close'].iloc[-1]
                pct = (curr - prev) / prev * 100
                data[f"{name}_pct"] = f"{pct:+.2f}%"
                # 特别记录美光是否创52周新高
                if name == 'mu':
                    info = ticker_obj.info
                    high_52w = info.get('fiftyTwoWeekHigh', None)
                    if high_52w and curr >= high_52w * 0.99:
                        data['mu_high'] = '是'
                    else:
                        data['mu_high'] = '否'
            else:
                data[f"{name}_pct"] = "N/A"
        except Exception as e:
            logger.warning(f"获取 {name} 数据失败: {e}")
            data[f"{name}_pct"] = "N/A"

    data['qdii_note'] = "近期QDII基金持续净申购，部分产品限购，建议关注额度变化；可通过支付宝搜索'QDII'或跨境ETF（需A股账户）配置海外资产。"
    return data
