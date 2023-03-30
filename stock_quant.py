import akahare_module as am
import datetime

# 定义参数
# 关注
share_list = [{
    'name': '恺英网络',
    'code': '002517',
    'parent_cyc_days': 60,
    'child_cyc_days': 10,
    'buy_ratio_min': 1.1,
    'buy_ratio_max': 0.9,
    'sell_ratio_min': 0.9,
    'sell_ratio_max': 1.1,
    'income_ratio': 1.2
}]


def run():
    actual_data = am.stock_zh_a_spot_em()
    # print(actual_data)
    for i, share in enumerate(share_list):
        cur_date_index = actual_data[(actual_data['代码'] == share['code'])].index.tolist()
        data = actual_data.iloc[cur_date_index]
        # data.set_index('最新价', inplace=True)
        print(data['最新价'])
        singleProcess(share, actual_data.iloc[cur_date_index])


def singleProcess(share, cur_date):
    # 设定日期
    calc_date_str = '20230328'
    calc_date = datetime.datetime.strptime(calc_date_str, "%Y%m%d")
    # 大周期天数
    parent_cyc_days = 60
    parent_date_first = calc_date - datetime.timedelta(days=parent_cyc_days)
    parent_date_first_str = parent_date_first.strftime("%Y%m%d")
    # 获取历史数据
    parent_df = am.stock_zh_a_hist_df('002517', parent_date_first_str, calc_date_str)
    # print(parent_df)
    # 小周期天数
    child_cyc_days = share['child_cyc_days']
    child_date_first = calc_date - datetime.timedelta(days=child_cyc_days)
    child_date_first_str = child_date_first.strftime("%Y%m%d")
    child_df = am.stock_zh_a_hist_df('002517', child_date_first_str, calc_date_str)
    # print(child_df)
    # 买入下限比 -- * 最低价位 与风险成正比
    buy_ratio_min = share['buy_ratio_min']
    # 买入上限比 -- * 最高价位 与风险成正比
    buy_ratio_max = share['buy_ratio_max']
    # 卖出下限比 -- * 最低价位 即止损价 与风险成反比
    sell_ratio_min = share['sell_ratio_min']
    # 卖出上限比 -- * 最高价位 即止盈价 与风险成正比
    sell_ratio_max = share['sell_ratio_max']

    # TODO 大周期最大价位
    parent_cyc_value_max = 20
    share['parent_cyc_value_max'] = parent_cyc_value_max
    # TODO 大周期最小价位
    parent_cyc_value_min = 5
    share['parent_cyc_value_min'] = parent_cyc_value_min
    # TODO 小周期最大价位
    child_cyc_value_max = 20
    share['child_cyc_value_max'] = child_cyc_value_max
    # TODO 小周期最小价位
    child_cyc_value_min = 5
    share['child_cyc_value_min'] = child_cyc_value_min
    # TODO 大周期是否处在下行阶段
    parent_cyc_fall = True
    share['parent_cyc_fall'] = parent_cyc_fall

    # TODO 当前价格
    cur_value = 10
    share['cur_value'] = cur_value

    # 计算
    # 下行阶段寻找卖出止损价
    sell_value_min = sell_ratio_min * parent_cyc_value_min
    share['sell_value_min'] = sell_value_min
    # 上行阶段寻找买入下限价位
    buy_value_min = buy_ratio_min * parent_cyc_value_min
    share['buy_value_min'] = buy_value_min
    # 上行阶段寻找买入上限价位
    buy_value_max = buy_ratio_max * parent_cyc_value_max
    share['buy_value_max'] = buy_value_max
    # 上行阶段寻找卖出止盈价
    sell_value_max = sell_ratio_max * parent_cyc_value_max
    share['sell_value_max'] = sell_value_max

    trade(share)


def trade(share):
    # TODO 是否持仓
    hold_share_flag = False
    # TODO 计算费用
    fee = 100
    # 交易
    if hold_share_flag:
        if share['cur_value'] > share['sell_value_max'] or share['cur_value'] < share['sell_value_min']:
            print("执行卖出")
    elif ~share['parent_cyc_fall']:
        if share['cur_value'] > share['buy_value_min'] and share['cur_value'] * share['income_ratio'] < (share['buy_value_max'] - fee):
            print("执行买入")


if __name__ == "__main__":
    run()
