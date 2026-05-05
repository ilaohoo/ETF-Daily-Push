import akshare as ak
import pandas as pd
import logging
from tenacity import retry, stop_after_attempt, wait_fixed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def fetch_all_etf_spot() -> pd.DataFrame:
    """
    获取全市场所有ETF的实时行情数据（包含代码、名称、涨跌幅、成交额等）
    数据来源：东方财富 ak.fund_etf_spot_em()
    """
    try:
        df = ak.fund_etf_spot_em()
        logger.info(f"成功获取ETF行情数据，共 {len(df)} 条记录")
        return df
    except Exception as e:
        logger.error(f"获取ETF行情数据失败: {e}")
        raise


def get_top_gainers_losers(df: pd.DataFrame, n: int = 20):
    """
    从行情数据中提取涨幅前n和跌幅前n的ETF
    返回：(gainers_df, losers_df)
    """
    # 确保涨跌幅列为数值类型，去除可能为空的记录
    df = df.copy()
    df['涨跌幅'] = pd.to_numeric(df['涨跌幅'], errors='coerce')
    df = df.dropna(subset=['涨跌幅'])

    # 按涨跌幅排序
    df_sorted = df.sort_values('涨跌幅', ascending=False)
    gainers = df_sorted.head(n)
    losers = df_sorted.tail(n).sort_values('涨跌幅', ascending=True)  # 跌幅最大在前

    # 选择关键列：代码、名称、最新价、涨跌幅、成交额
    cols = ['代码', '名称', '最新价', '涨跌幅', '成交额']
    gainers = gainers[cols]
    losers = losers[cols]

    # 格式化涨跌幅为百分比字符串，成交额转为亿元
    for df_item in (gainers, losers):
        df_item['涨跌幅'] = df_item['涨跌幅'].apply(lambda x: f"{x:+.2f}%")
        df_item['成交额'] = df_item['成交额'].apply(lambda x: f"{x/1e8:.2f}亿")

    return gainers, losers
