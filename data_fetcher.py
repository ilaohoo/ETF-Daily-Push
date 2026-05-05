import akshare as ak
import pandas as pd
import logging
from tenacity import retry, stop_after_attempt, wait_fixed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def fetch_all_etf_spot() -> pd.DataFrame:
    """获取全市场所有ETF实时行情（东方财富）"""
    try:
        df = ak.fund_etf_spot_em()
        logger.info(f"成功获取ETF行情数据，共 {len(df)} 条记录")
        return df
    except Exception as e:
        logger.error(f"获取ETF行情数据失败: {e}")
        raise


def get_top_gainers_losers(df: pd.DataFrame, n: int = 20):
    """返回涨幅前n和跌幅前n的ETF（格式：代码、名称、最新价、涨跌幅、成交额）"""
    df = df.copy()
    df['涨跌幅'] = pd.to_numeric(df['涨跌幅'], errors='coerce')
    df = df.dropna(subset=['涨跌幅'])

    df_sorted = df.sort_values('涨跌幅', ascending=False)
    gainers = df_sorted.head(n)
    losers = df_sorted.tail(n).sort_values('涨跌幅', ascending=True)

    cols = ['代码', '名称', '最新价', '涨跌幅', '成交额']
    gainers = gainers[cols]
    losers = losers[cols]

    for d in (gainers, losers):
        d['涨跌幅'] = d['涨跌幅'].apply(lambda x: f"{x:+.2f}%")
        d['成交额'] = d['成交额'].apply(lambda x: f"{x/1e8:.2f}亿")

    return gainers, losers
