import akshare as ak
import pandas as pd

stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="002517", period="daily", start_date="20170301", end_date='20230331', adjust="")
print(stock_zh_a_hist_df)

df = pd.DataFrame(stock_zh_a_hist_df)
# index = False表示不写入索引
df.to_csv('stock_zh_a_hist_df.csv', index=False)
