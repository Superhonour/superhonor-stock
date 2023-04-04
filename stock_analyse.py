import akahare_module as am
import exponential_smoothing as es

# 定义参数
calc_date_str = '20230404'

stock_list = am.stock_rank_xzjp_ths()
stock_code_dict = []
for index, row in stock_list.iterrows():
    df = am.stock_zh_a_hist_df(row['股票代码'], '20230101', calc_date_str)
    stock_code = row['股票代码']
    if stock_code not in stock_code_dict:
        stock_code_dict.append(stock_code)
        file_name = row['股票代码'] + '.csv'
        # df.to_csv(file_name, index=False)
        es.run(file_name, row['股票简称'] + '【' + stock_code + '】')
