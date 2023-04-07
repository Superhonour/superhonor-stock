import akahare_module as am
import exponential_smoothing as es
import sql_helper as sh
import datetime

t_stock_hist_columns = {
    '日期': 'trade_date',
    '开盘': 'open_amount',
    '收盘': 'close_amount',
    '最高': 'max_amount',
    '最低': 'min_amount',
    '成交量': 'trade_volume',
    '成交额': 'trade_amount',
    '振幅': 'amplitude_range',
    '涨跌幅': 'fluctuation_range',
    '涨跌额': 'fluctuation_amount',
    '换手率': 'turnover_rate'
}


def update_hist(stock_code, trade_date):
    data = sh.fetch_one(
        "select * from t_stock_hist where stock_code = %s and trade_date = %s",
        (stock_code, trade_date))
    if data is None:
        df = am.stock_zh_a_hist_df(stock_code, trade_date, trade_date)
        df.rename(columns=t_stock_hist_columns, inplace=True)
        df.loc[:, 'stock_code'] = stock_code
        sh.mysqlconn().to_sql('t_stock_hist', df)


def forecast():
    # 定义参数
    forecast_date = '20230407'
    calc_date = datetime.datetime.strptime(
        forecast_date, "%Y%m%d") - datetime.timedelta(days=1)
    calc_date_str = calc_date.strftime("%Y%m%d")

    stock_list = am.stock_rank_xzjp_ths()
    stock_code_dict = []
    for index, row in stock_list.iterrows():
        stock_code = row['股票代码']
        if stock_code not in stock_code_dict:
            stock_code_dict.append(stock_code)
            update_hist(stock_code, calc_date_str)
            file_name = row['股票代码'] + '.csv'
            # df = am.stock_zh_a_hist_df(stock_code, '20230101', calc_date_str)
            # df.to_csv(file_name, index=False)
            stock_name = row['股票简称'] + '【' + stock_code + '】'
            forecast_value = round(es.run(file_name, stock_name), 2)
            cur_value = am.stock_zh_a_spot_em_with_symbol(stock_code)
            # sh.insert(
            #     "insert into t_stock_forecast (stock_code, forecast_date, forecast_amount) values (%s, %s, %s)",
            #     (stock_code, forecast_date, forecast_value))
            print("%s预测值收盘价格为=%s,当前价格=%s,误差=%s,误差比=%s" %
                  (stock_name, forecast_value, cur_value,
                   round(forecast_value - cur_value, 2),
                   round((forecast_value - cur_value) * 100 / cur_value, 2)))


if __name__ == "__main__":
    forecast()
