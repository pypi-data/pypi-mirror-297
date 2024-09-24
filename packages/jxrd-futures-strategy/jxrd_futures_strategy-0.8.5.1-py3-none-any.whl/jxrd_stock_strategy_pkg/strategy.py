import threading
from datetime import datetime, time
from jxrd_stock_strategy_pkg import params
from jxrd_stock_strategy_pkg import colors


class NoDayLineStrategy:

    def __init__(self, context_instance=None, params=None, call_back_dic={}):
        if context_instance is not None and params is not None:
            self.call_back_dic = call_back_dic
            self.context_instance = context_instance
            self.params = params
            self.open_date = 0  # 记录当前交易日
            self.open_first_bar_time = 0
            self.profitAbove = 0  # 记录上方盈利
            self.profitBelow = 0  # 记录下方盈利
            self.a_list = []  # 开单记录
            self.statistics = {}  # 统计
            self.back_test_params_map = {}
            self.directions = set()
            self.cid = params['exchange'] + '|' + params['tag'] + '|' + params['name'] + '|' + params['no']
            self.index_id = params['exchange'] + '|' + params['tag'] + '|' + params['name'] + '|INDEX'
            self.version = '20240702'
            self.log_info = call_back_dic.get("LogInfo")
            self.log_info(self.version, "", self.cid, 'MIN', self.params['min'], 'MAX',
                          self.params['max'], '价格', self.params["price"], '数量', self.params.get('quantity', 1))
            self.lock = threading.RLock()

    def get_cid(self):
        return self.cid

    def get_index_id(self):
        return self.index_id

    def subscribe(self):
        subscribe_event = self.call_back_dic.get("subscribe_event")
        subscribe_event(self) if subscribe_event is not None else None

    def __get_open_price__(self, trading_day=None):
        open_price_event = self.call_back_dic.get("open_price_event")
        return open_price_event(self, trading_day) if open_price_event is not None else 0

    def __get_price_tick__(self):
        price_tick_event = self.call_back_dic.get('price_tick')
        return price_tick_event(self) if price_tick_event is not None else 1

    def get_statistics(self):
        return self.statistics

    def place_order(self, direction, test_params, data_time):
        # qty = round(g_params['price'] / (profit * ContractUnit(cId)))
        # if qty == 0:
        #     qty = 1
        qty = self.params.get('quantity', 1)
        open_position = test_params.get_open_position()
        open_price = test_params.get_open_price()
        profit = test_params.get_profit()
        trade_date = test_params.get_trade_day()

        if direction == 'buy':
            order = {'time': data_time, 'd': trade_date, 'o': open_price, 'qty': qty,
                     'direction': direction,
                     'tp': open_price + profit,
                     'sl': open_price - profit}
            self.call_back_dic.get('Buy')(qty, open_position, "", needCover=False)
        else:
            order = {'time': data_time, 'd': trade_date, 'o': open_price, 'qty': qty,
                     'direction': direction,
                     'tp': open_price - profit,
                     'sl': open_price + profit}
            self.call_back_dic.get('SellShort')(qty, open_position, "", needCover=False)

        self.a_list.append(order)
        self.log_info(f"{direction} 方向开仓 {order} 开仓位置:{open_position}")

    def can_buy_order(self, record_item, test_params):

        if record_item.get('strategy_status') == 'C':
            return record_item.get('q_last') <= test_params.get_open_position()
        if record_item.get('strategy_status') == 'H':
            return record_item['low'] <= test_params.get_open_position()
        return False

    def can_sell_order(self, record_item, test_params):

        if record_item.get('strategy_status') == 'C':
            return record_item.get('q_last') >= test_params.get_open_position()
        if record_item.get('strategy_status') == 'H':
            return record_item['high'] >= test_params.get_open_position()
        return False

    def buy_cross_open_price(self, open_price, record_item):
        if record_item.get('strategy_status') == 'C':
            return record_item.get('q_last') == open_price and self.profitBelow > 0
        return record_item['low'] <= open_price <= record_item['high'] and self.profitBelow > 0

    def sell_cross_open_price(self, open_price, record_item):
        if record_item.get('strategy_status') == 'C':
            return record_item.get('q_last') == open_price and self.profitAbove > 0
        return record_item['low'] <= open_price <= record_item['high'] and self.profitAbove > 0

    def record_first_record(self, record_item, open_price=0):

        trade_day = record_item['tradingday']

        if self.buy_cross_open_price(open_price, record_item):
            # and 'buy' not in self.directions:
            test_params = self.back_test_params_map.get('buy' + trade_day)
            if test_params is None:
                test_params = params.BackTestParams()
                self.back_test_params_map['buy' + trade_day] = test_params
                test_params.set_trade_day(trade_day)
                test_params.set_open_price(open_price)
                test_params.set_profit(self.profitBelow)
                test_params.calculate_open_position(open_price - self.profitBelow * (
                        self.params.get('profit_percent', 0) / 100), self.__get_price_tick__(),
                                                    self.params.get("profit_percent_decimal_direct", 'none'))
                test_params.set_stop_profit_position(open_price + self.profitBelow)
                log_str = f" --- 记录穿过开盘价 Buy 方向 开盘日:{trade_day} 开盘价：{open_price} 最高利润:{test_params.get_profit()} " \
                          f" 买开:{test_params.get_open_position()}  止盈:{test_params.get_stop_profit_position()} " \
                          f" 当前分钟线最高: {record_item['high']} 最低:{record_item['low']} 时间:{record_item['datetime']}"
                self.log_info(log_str)
            # and 'sell' not in self.directions:
        if self.sell_cross_open_price(open_price, record_item):
            test_params = self.back_test_params_map.get('sell' + trade_day)
            if test_params is None:
                test_params = params.BackTestParams()
                self.back_test_params_map['sell' + trade_day] = test_params

                test_params.set_trade_day(trade_day)
                test_params.set_open_price(open_price)
                test_params.set_profit(self.profitAbove)
                # ( open_price= 1000; profit_percent=40%; profitAbove=500 开仓位置=1200 止盈位置=500)
                test_params.calculate_open_position(open_price + self.profitAbove * (
                        self.params.get('profit_percent', 0) / 100), self.__get_price_tick__(),
                                                    self.params.get("profit_percent_decimal_direct", 'none'))
                test_params.set_stop_profit_position(open_price - self.profitAbove)
                log_str = f" --- 记录穿过开盘价 Sell 方向 开盘日:{trade_day} 开盘价：{open_price} 最高利润:{test_params.get_profit()} " \
                          f" 卖开:{test_params.get_open_position()}  止盈:{test_params.get_stop_profit_position()} " \
                          f" 当前分钟线最高: {record_item['high']} 最低:{record_item['low']} 时间:{record_item['datetime']}"

                self.log_info(log_str)

    def calculate(self, price=0.0, min_value=0.0):
        scale = float(self.params.get("scale", 0.0))
        result = scale * min_value * price
        return result if result > 0 else min_value

    # 策略触发事件每次触发时都会执行该函数
    def handle_data(self, record_item):
        with self.lock:
            if self.not_trading_time(record_item):
                self.log_info(f"无效Tick数据 {record_item}")
                return

            # 更新开盘价
            open_price = self.__get_open_price__(record_item['tradingday'])
            if record_item['tradingday'] != self.open_date:
                self.open_date = record_item['tradingday']
                self.open_first_bar_time = record_item.get('datetime')
                self.profitAbove = 0
                self.profitBelow = 0
                self.log_info('交易日:', self.open_date, '开盘时间:', self.open_first_bar_time, "开盘价:", open_price)

            if record_item.get('strategy_status') == 'H':
                self.record_first_record(record_item, open_price)
            elif record_item['datetime'] != self.open_first_bar_time:
                self.record_first_record(record_item, open_price)

            if self.profitBelow > self.params['max']:
                self.profitBelow = 0
            if self.profitAbove > self.params['max']:
                self.profitAbove = 0

            back_test_params_map_copy = self.back_test_params_map.copy()
            for prefix_trade_day, test_params in back_test_params_map_copy.items():
                if prefix_trade_day.startswith('buy') and prefix_trade_day not in self.directions:

                    is_buy_stop_profit_position = record_item['high'] >= test_params.get_stop_profit_position() \
                        if record_item.get(
                        'strategy_status') == 'H' else record_item['q_last'] >= test_params.get_stop_profit_position()

                    if is_buy_stop_profit_position:
                        try:
                            self.back_test_params_map.pop(prefix_trade_day)
                            log_str = f"buy 方向到达止盈点位 {prefix_trade_day} 清理历史记录"
                            self.log_info(log_str)
                        except KeyError:
                            self.log_info(f" buy 止盈点位 {prefix_trade_day} 不在字典中")
                        if 'buy' + record_item['tradingday'] == prefix_trade_day:
                            self.profitBelow = 0

                    elif self.can_buy_order(record_item, test_params):
                        if record_item.get("strategy_status") == 'H':
                            self.place_buy_order(prefix_trade_day, record_item, test_params)
                        elif 'buy' + record_item['tradingday'] != prefix_trade_day or (
                                record_item['datetime'] != self.open_first_bar_time):
                            self.place_buy_order(prefix_trade_day, record_item, test_params)

                if prefix_trade_day.startswith('sell') and prefix_trade_day not in self.directions:

                    is_sell_stop_profit_position = record_item['low'] <= test_params.get_stop_profit_position() \
                        if record_item.get(
                        'strategy_status') == 'H' else record_item['q_last'] <= test_params.get_stop_profit_position()

                    if is_sell_stop_profit_position:
                        try:
                            self.back_test_params_map.pop(prefix_trade_day)
                            log_str = f"sell 方向到达止盈点位 {prefix_trade_day} 清理历史记录"
                            self.log_info(log_str)
                        except KeyError:
                            self.log_info(f" sell 止盈点位 {prefix_trade_day} 不在字典中")
                        if 'sell' + record_item['tradingday'] == prefix_trade_day:
                            self.profitAbove = 0

                    elif self.can_sell_order(record_item, test_params):
                        if record_item.get("strategy_status") == 'H':
                            self.place_sell_order(prefix_trade_day, record_item, test_params)
                        elif 'sell' + record_item['tradingday'] != prefix_trade_day or (
                                record_item['datetime'] != self.open_first_bar_time):
                            self.place_sell_order(prefix_trade_day, record_item, test_params)

            # 判断盈利是否大于限定值
            if record_item['high'] - open_price > self.calculate(open_price, self.params.get("min")) \
                    and 'sell' + record_item['tradingday'] not in self.directions:
                # 更新为最大盈利值
                self.profitAbove = max(self.profitAbove, record_item['high'] - open_price)

            # 判断盈利是否大于限定值
            if open_price - record_item['low'] > self.calculate(open_price, self.params.get("min")) \
                    and 'buy' + record_item['tradingday'] not in self.directions:
                # 更新为最大盈利值
                self.profitBelow = max(self.profitBelow, open_price - record_item['low'])

            # 判断平仓
            new_a_list = []
            for order in self.a_list:
                direction = order.get('direction')
                if direction == 'buy' and self.can_buy_many_profit(order, record_item):
                    # Sell(order.get('qty'), order.get('tp'), cId, '', 'A')  #盈利次数加1
                    self.call_back_dic.get('Sell')(order.get('qty'), order.get('tp'), self.get_cid(), '', 'A')

                    self.log_info(f"触发时间:{record_item['datetime']} 平多仓止盈{order}")
                    self.statistics["平多仓止盈次数"] = self.statistics.get("平多仓止盈次数", 0) + 1
                    self.statistics["止盈次数"] = self.statistics.get("止盈次数", 0) + 1

                    prefix_trade_day = 'buy' + order.get('d')
                    if order.get('d') == record_item['tradingday']:
                        self.directions.discard(prefix_trade_day)
                    try:
                        self.back_test_params_map.pop(prefix_trade_day)
                        self.log_info(f"平多仓止盈 {prefix_trade_day} 清理历史记录")
                        self.log_info(f"触发Tick {record_item}")
                    except KeyError:
                        self.log_info(f"平多仓止盈 {prefix_trade_day} 不在字典中")

                elif direction == 'sell' and self.can_sell_empty_loss(order, record_item):
                    # BuyToCover(order.get('qty'), order.get('sl'), cId, '', 'A')  # 亏损次数加1
                    buy_to_cover_event = self.call_back_dic.get('BuyToCover')
                    if record_item.get("strategy_status") == 'H':
                        buy_to_cover_event(order.get('qty'), order.get('sl'), self.get_cid(), '', 'A')
                    else:
                        q_upper_limit = record_item.get("q_upper_limit", 0)
                        order_price = order.get('sl') if q_upper_limit == 0 else q_upper_limit
                        buy_to_cover_event(order.get('qty'), order_price, self.get_cid(), '', 'A')

                    self.log_info(f"触发时间:{record_item['datetime']} 平空仓止损{order}")
                    self.statistics["平空仓止损次数"] = self.statistics.get("平空仓止损次数", 0) + 1
                    self.statistics["止损次数"] = self.statistics.get("止损次数", 0) + 1

                    prefix_trade_day = 'sell' + order.get('d')
                    if order.get('d') == record_item['tradingday']:
                        self.directions.discard(prefix_trade_day)
                    try:
                        self.back_test_params_map.pop(prefix_trade_day)
                        self.log_info(f"平空仓止损 {prefix_trade_day} 清理历史记录")
                        self.log_info(f"触发Tick {record_item}")
                    except KeyError:
                        self.log_info(f"平空仓止损 {prefix_trade_day} 不在字典中")

                elif direction == 'sell' and self.can_sell_empty_profit(order, record_item):
                    # BuyToCover(order.get('qty'), order.get('tp'), cId, '', 'A') # 盈利次数加1
                    self.call_back_dic.get('BuyToCover')(order.get('qty'), order.get('tp'), self.get_cid(), '', 'A')

                    self.log_info(f"触发时间:{record_item['datetime']} 平空仓止盈{order}")
                    self.statistics["平空仓止盈次数"] = self.statistics.get("平空仓止盈次数", 0) + 1
                    self.statistics["止盈次数"] = self.statistics.get("止盈次数", 0) + 1

                    prefix_trade_day = 'sell' + order.get('d')
                    if order.get('d') == record_item['tradingday']:
                        self.directions.discard(prefix_trade_day)
                    try:
                        self.back_test_params_map.pop(prefix_trade_day)
                        self.log_info(f"平空仓止盈 {prefix_trade_day} 清理历史记录")
                        self.log_info(f"触发Tick {record_item}")
                    except KeyError:
                        self.log_info(f"平空仓止盈 {prefix_trade_day} 不在字典中")

                elif direction == 'buy' and self.can_buy_many_loss(order, record_item):
                    # Sell(order.get('qty'), order.get('sl'), cId, '', 'A') # 亏损次数加1
                    sell_event = self.call_back_dic.get('Sell')
                    if record_item.get("strategy_status") == 'H':
                        sell_event(order.get('qty'), order.get('sl'), self.get_cid(), '', 'A')
                    else:
                        q_low_limit = record_item.get("q_low_limit", 0)
                        order_price = order.get('sl') if q_low_limit == 0 else q_low_limit
                        sell_event(order.get('qty'), order_price, self.get_cid(), '', 'A')

                    self.log_info(f"触发时间:{record_item['datetime']} 平多仓止损{order}")
                    self.statistics["平多仓止损次数"] = self.statistics.get("平多仓止损次数", 0) + 1
                    self.statistics["止损次数"] = self.statistics.get("止损次数", 0) + 1

                    prefix_trade_day = 'buy' + order.get('d')
                    if order.get('d') == record_item['tradingday']:
                        self.directions.discard(prefix_trade_day)
                    try:
                        self.back_test_params_map.pop(prefix_trade_day)
                        self.log_info(f"平多仓止损 {prefix_trade_day} 清理历史记录")
                        self.log_info(f"触发Tick {record_item}")
                    except KeyError:
                        self.log_info(f"平多仓止损 {prefix_trade_day} 不在字典中")

                else:
                    new_a_list.append(order)

            self.a_list = new_a_list
            self.plot_numeric(open_price, record_item['tradingday'])

    def place_sell_order(self, prefix_trade_day, record_item, test_params):
        self.place_order('sell', test_params, record_item['datetime'])
        self.directions.add(prefix_trade_day)
        if 'sell' + record_item['tradingday'] == prefix_trade_day:
            self.profitAbove = 0

    def place_buy_order(self, prefix_trade_day, record_item, test_params):
        self.place_order('buy', test_params, record_item['datetime'])
        self.directions.add(prefix_trade_day)
        if 'buy' + record_item['tradingday'] == prefix_trade_day:
            self.profitBelow = 0

    def not_trading_time(self, record_item):

        if record_item.get('strategy_status') == 'H':
            return False

        now = datetime.now()
        current_time = now.time()
        morning_start = time(3, 0, 0)
        morning_end = time(9, 0, 0)
        afternoon_start = time(15, 0, 0)
        afternoon_end = time(21, 0, 0)
        if (morning_start < current_time < morning_end) or (afternoon_start < current_time < afternoon_end):
            self.log_info(f"当前非交易时间 触发Tick")
            return True

        return 0.03 < record_item.get('datetime') < 0.0900 or 0.15 < record_item.get('datetime') < 0.2100

    def can_buy_many_profit(self, order, record_item):
        if record_item.get('strategy_status') == 'C':
            return record_item.get('q_last') >= order.get('tp')
        else:
            return record_item['high'] >= order.get('tp')

    def can_sell_empty_loss(self, order, record_item):

        if record_item.get('strategy_status') == 'C':
            return record_item.get('q_last') >= order.get('sl')
        else:
            return record_item['high'] >= order.get('sl')

    def can_sell_empty_profit(self, order, record_item):

        if record_item.get('strategy_status') == 'C':
            return record_item.get('q_last') > 0 and record_item.get(
                'q_last') <= order.get('tp')
        else:
            return record_item['low'] <= order.get('tp')

    def can_buy_many_loss(self, order, record_item):

        if record_item.get('strategy_status') == 'C':
            return record_item.get('q_last') > 0 and record_item.get(
                'q_last') <= order.get('sl')
        else:
            return record_item['low'] <= order.get('sl')

    def plot_numeric(self, open_price, trading_day=None):
        draw = self.call_back_dic.get("plot_numeric")
        draw('开盘价', open_price, colors.rgb_yellow())
        draw('最优值高点', open_price + self.params['min'], colors.rgb_red())
        draw('最优值低点', open_price - self.params['min'], colors.rgb_red())


class DayLineStrategy(NoDayLineStrategy):

    def __init__(self, context_instance=None, params=None, call_back_dic={}):
        if context_instance is not None and params is not None:
            super().__init__(context_instance, params, call_back_dic)
        else:
            super().__init__()

    def __get_m_open_price__(self, trading_day=None):
        m_open_price_event = self.call_back_dic.get("m_open_price_event")
        return m_open_price_event(self, trading_day) if m_open_price_event is not None else 0

    def __get_ma_days__(self):
        ma_days_event = self.call_back_dic.get("ma_days_event")
        return ma_days_event(self) if ma_days_event is not None else 0

    def buy_cross_open_price(self, open_price, record_item):

        if super(DayLineStrategy, self).buy_cross_open_price(open_price, record_item):
            return self.__get_m_open_price__(record_item['tradingday']) >= self.__get_ma_days__()
        return False

    def sell_cross_open_price(self, open_price, record_item):
        if super(DayLineStrategy, self).sell_cross_open_price(open_price, record_item):
            return self.__get_m_open_price__(record_item['tradingday']) < self.__get_ma_days__()
        return False

    def plot_numeric(self, open_price, trading_day=None):
        super(DayLineStrategy, self).plot_numeric(open_price, trading_day)
        draw = self.call_back_dic.get("plot_numeric")
        draw(f'ma{self.params.get("days", 0)}', self.__get_ma_days__(), colors.rgb_brown())
        draw('指数开盘价', self.__get_m_open_price__(trading_day), colors.rgb_green())


if __name__ == '__main__':
    print(f"开始运行")
