from ffquant.indicators.BaseIndicator import BaseIndicator
from datetime import datetime, timedelta
import pytz

__ALL__ = ['LongTermDirection']

class LongTermDirection(BaseIndicator):
    (BEARISH, NA, BULLISH) = (-1, 0, 1)

    lines = ('ltd',)

    def __init__(self):
        self.addminperiod(1)
        self.cache = {}

    def handle_api_resp(self, item):
        # BE CAREFULL!!!! closeTime stands for the beginning of the bar here
        result_time_str = datetime.fromtimestamp(item['closeTime']/ 1000).strftime('%Y-%m-%d %H:%M:%S')
        if item['longTermDir'] == 'BULLISH':
            self.cache[result_time_str] = self.BULLISH
        elif item['longTermDir'] == 'BEARISH':
            self.cache[result_time_str] = self.BEARISH

        if self.p.debug:
            print(f"{self.__class__.__name__}, result_time_str: {result_time_str}, long_term_dir: {item['longTermDir']}")

    def backpeek_for_result(self):
        current_bar_time = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        current_bar_time_str = current_bar_time.strftime('%Y-%m-%d %H:%M:%S')

        self.lines.ltd[0] = self.cache.get(current_bar_time_str, self.NA)
        for i in range(0, self.p.backpeek_size):
            v = self.cache.get((current_bar_time - timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M:%S'), self.NA)
            if v != self.NA:
                if self.p.debug:
                    print(f"{self.__class__.__name__}, backpeek_size: {i}, v: {v}")
                self.lines.ltd[0] = v
                break