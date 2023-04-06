import akahare_module as am
import exponential_smoothing as es

# 定义参数
calc_date_str = '20230406'

stock_list = am.stock_rank_xzjp_ths()
stock_code_dict = []
for index, row in stock_list.iterrows():
    stock_code = row['股票代码']
    df = am.stock_zh_a_hist_df(stock_code, '20230101', calc_date_str)
    if stock_code not in stock_code_dict:
        stock_code_dict.append(stock_code)
        file_name = row['股票代码'] + '.csv'
        stock_name = row['股票简称'] + '【' + stock_code + '】'
        df.to_csv(file_name, index=False)
        forecast_value = round(es.run(file_name, row['股票简称'] + '【' + stock_code + '】'), 2)
        cur_value = am.stock_zh_a_spot_em_with_symbol(stock_code)
        print("%s预测值收盘价格为=%s,当前价格=%s,误差=%s,误差比=%s" %
              (stock_name, forecast_value, cur_value, round(forecast_value - cur_value, 2), round((forecast_value - cur_value) * 100 / cur_value, 2)))
