from ffquant.indicators.BaseIndicator import BaseIndicator
from datetime import datetime, timedelta
import pytz

__ALL__ = ['TradeAction']

class TradeAction(BaseIndicator):
    (BUY, NA, SELL) = (1, 0, -1)

    lines = ('ta',)

    def __init__(self):
        self.addminperiod(1)
        self.cache = {}

    def handle_api_resp(self, item):
        # BE CAREFULL!!!! closeTime stands for the beginning of the bar here
        result_time_str = datetime.fromtimestamp(item['closeTime']/ 1000).strftime('%Y-%m-%d %H:%M:%S')
        if item['tradeAction'] == 'BUY':
            self.cache[result_time_str] = self.BUY
        elif item['tradeAction'] == 'SELL':
            self.cache[result_time_str] = self.SELL

        if self.p.debug:
            print(f"{self.__class__.__name__}, result_time_str: {result_time_str}, trade_action: {item['tradeAction']}")

    def backpeek_for_result(self):
        current_bar_time = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        current_bar_time_str = current_bar_time.strftime('%Y-%m-%d %H:%M:%S')

        self.lines.ta[0] = self.cache.get(current_bar_time_str, self.NA)
        for i in range(0, self.p.backpeek_size):
            v = self.cache.get((current_bar_time - timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M:%S'), self.NA)
            if v != self.NA:
                if self.p.debug:
                    print(f"{self.__class__.__name__}, backpeek_size: {i}, v: {v}")
                self.lines.ta[0] = v
                break