import akshare as ak


def stock_zh_a_hist_df(symbol, start_date, end_date, period="daily", adjust=""):
    """
    历史行情数据-东财
    period - 指定周期 默认天
    adjust - 复权 默认不复权
    """
    return ak.stock_zh_a_hist(symbol, period, start_date, end_date, adjust)
    # print(stock_zh_a_hist_df)


def stock_zh_a_spot_em():
    """
    实时行情数据-东财
    """
    return ak.stock_zh_a_spot_em()


def stock_zh_a_spot_em_with_symbol(symbol):
    """
    实时行情数据-东财
    """
    df = stock_zh_a_spot_em()
    cur_value_list = df[(df['代码'] == symbol)]['最新价'].tolist()
    return cur_value_list[0]


def stock_rank_xzjp_ths():
    """
    同花顺-数据中心-技术选股-险资举牌
    """
    return ak.stock_rank_xzjp_ths()


if __name__ == "__main__":
    df = stock_zh_a_hist_df('000900', '20230407', '20230407')
    print(df)
