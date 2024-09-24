## 数据
添加函数 xtdata.get_trading_contract_list()
获取当前主力合约可交易标的列表

## 功能
token模式，可以设置初始化的市场列表
xtdatacenter.set_init_markets()

函数xtdata.get_period_list() 结果结构调整

添加获取合约交易时间相关函数
xtdata.get_trading_period()
xtdata.get_all_trading_periods()
xtdata.get_all_kline_trading_periods()

添加函数 xtdata.subscribe_quote2()
比xtdat.subscribe_quote()增加了除权参数