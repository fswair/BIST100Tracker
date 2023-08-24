from requests import get
from bs4 import BeautifulSoup as BS
from typing import Callable
from asyncio import sleep, get_event_loop, iscoroutinefunction
from time import time
from models import Shares

### telegram komutu verildiği farz edilerek 
user_inputs = [
    "/addtarget PAPIL 37"
]

class Filter:
    def __init__(self, stock: str, price_target: float | int, change_in_24h: float | int, filter_requested_id: float | int):
        self.id = id(self)
        self.stock = stock
        self.change_in_24h = change_in_24h
        self.price_target = price_target
        self.filter_requested_id = filter_requested_id

    def validator(self, share: "Shares"):
        if share.close >= int(self.price_target):
            return True
        else:
            return False

filters = list(map(lambda input: Filter(*(input.split()[1:]), filter_requested_id=0, change_in_24h=0), user_inputs))

class Filters:
    def __new__(cls):
        return filters     
    

class BIST:
    def __init__(self):
        self.request = get("https://www.isyatirim.com.tr/en-us/analysis/stocks/Pages/bist-data-table.aspx?endeks=09#page-1")
        self.bs = BS(self.request.content, "html.parser")
        self.funcs = []
    def get_shares(self, as_json: bool = False):
        rows = self.bs.select_one("tbody#temelTBody_Ozet").select("tr")
        shares = list(map(lambda row: map(lambda data: data.text, filter(bool, row.select("td"))), rows))
        for i, share in enumerate(shares):
            s = []
            for v in share:
                if v.find(",") == -1:
                    v = v[:].replace(".", "")
                else:
                    v = v[:v.find(",")].replace(".", "")
                if "." in v and v[0].isdigit() and v[-1].isdigit():
                    s.append(float(v))
                elif v.isdigit():
                    s.append(int(v))
                else:
                    s.append(v)
            shares[i] = s

        shares = list(map(lambda data: Shares(*(data + [time()])), shares))
        shares = list(filter(lambda share: share.close, shares))
        if as_json:
            shares = list(map(lambda share: share.__dict__, shares))
        return shares
    def get_close_prices(self):
        return list(map(lambda q: q.close, self.get_shares()))
    
    async def _on_filter(self):
        shares = self.get_shares()
        filters: list[Filter] = Filters()
        for share in shares:
            share.add()
            for filter in filters:
                if share.stock == filter.stock and filter.validator(share):
                    for func in self.funcs:
                        #print("%s kullanıcısının filtresi gerçekleşti.." % filter.filter_requested_id)
                        if iscoroutinefunction(func):
                            await func(share, filter)
                        else:
                            func(share, filter)
        await sleep(300)
        return await self._on_filter()
    def on_filter(self, func: Callable):
        self.funcs.append(func)
    
    def run(self):
        print("[LOG] Hisseler kontrol edilmeye başlandı...")
        return get_event_loop().run_until_complete(self._on_filter())