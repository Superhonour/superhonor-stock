import akshare as ak


def stock_zh_a_hist_df(symbol, start_date, end_date, period="daily", adjust="hfq"):
    """
    历史行情数据-东财
    period - 指定周期 默认天
    adjust - 复权 默认后复权
    """
    return ak.stock_zh_a_hist(symbol, period, start_date, end_date, adjust)
    # print(stock_zh_a_hist_df)


def stock_zh_a_spot_em():
    """
    实时行情数据-东财
    """
    return ak.stock_zh_a_spot_em()
