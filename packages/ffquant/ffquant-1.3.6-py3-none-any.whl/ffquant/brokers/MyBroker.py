import backtrader as bt
from datetime import datetime
import os
import requests
import json

__ALL__ = ['MyBroker']

class MyBroker(bt.BrokerBase):

    def __init__(self, id=None, cash=None, debug=False, *args, **kwargs):
        super(MyBroker, self).__init__(*args, **kwargs)
        self.base_url = os.environ.get('MY_BROKER_BASE_URL', 'http://192.168.25.247:8220')
        self.id = id if id is not None else os.environ.get('MY_BROKER_ID', "14282761")
        self.cash = cash
        self.orders = list()
        self.debug = debug

    def start(self):
        super(MyBroker, self).start()

        url = self.base_url + f"/orders/query/tv/{self.id}"

        pass

    def stop(self):
        super(MyBroker, self).stop()
        pass

    def getcash(self):
        print("MyBroker, getcash called")
        return self.cash

    def getvalue(self):
        # return self.cash + sum([d.close[0] * d.position.size for d in self.getdatas()])
        print("MyBroker, getvalue called")
        return self.cash

    def getposition(self, data):
        print("MyBroker, getposition called")
        url = self.base_url + f"/position/tv/{self.id}"
        response = requests.get(url).json()
        if self.debug:
            print(f"getposition, response: {response}")
        return super().getposition(data)

    def cancel(self, order):
        return super().cancel(order)
    
    def orderstatus(self, order):
        print("MyBroker, orderstatus called")
        pass

    def submit(self, order, **kwargs):
        url = self.base_url + f"/place/order/tv/{self.id}"

        data = {
            "symbol": order.data.p.symbol,
            "side": kwargs['side'],
            "qty": order.size,
            "price": order.price,
            "type": "market" if order.exectype == bt.Order.Market else "limit",
        }
        payload = f"content={json.dumps(data)}"
        if self.debug:
            print(f"submit, payload: {payload}")

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(url, headers=headers, data=payload).json()
        if self.debug:
            print(f"submit, response: {response}")
        return response
    
    def getcommissioninfo(self, data):
        print("MyBroker, getcommissioninfo called")
        return super().getcommissioninfo(data)

    def buy(self, owner, data, size, price=None, plimit=None, exectype=None, valid=None, tradeid=0, oco=None, trailamount=None, trailpercent=None, **kwargs):
        order = bt.order.BuyOrder(owner=owner, data=data, size=size, price=price, pricelimit=plimit, exectype=exectype, valid=valid, tradeid=tradeid, oco=oco, trailamount=trailamount, trailpercent=trailpercent)
        self.submit(order, **kwargs)
        return order

    def sell(self, owner, data, size, price=None, plimit=None, exectype=None, valid=None, tradeid=0, oco=None, trailamount=None, trailpercent=None, **kwargs):
        order = bt.order.SellOrder(owner=owner, data=data, size=size, price=price, pricelimit=plimit, exectype=exectype, valid=valid, tradeid=tradeid, oco=oco, trailamount=trailamount, trailpercent=trailpercent)
        self.submit(order, **kwargs)
        return order
    
    def get_notification(self):
        # print("MyBroker, get_notification called")
        pass

    def next(self):
        # print("MyBroker, next called")
        return super().next()
