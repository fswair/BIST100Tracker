from pydantic.dataclasses import dataclass
from pydantic import BaseModel
from mentodb import Mento, MentoConnection

@dataclass
class ShareModel(BaseModel):
    stock: str
    name: str
    sector: str
    close: float | int
    market_cap_tl: float | int
    market_cap_usd: float | int
    float_rate: float | int
    paid_in_capital: float | int
    added_date: int

@dataclass
class FilterModel(BaseModel):
    id: int
    stock: str
    change_in_24h: float
    price_target: float
    filter_requested_by: int

connection = MentoConnection("./database/database.db")
mento = Mento(connection)

@dataclass
class Shares:
    stock: str
    name: str
    sector: str
    close: float | int
    market_cap_tl: float | int
    market_cap_usd: float | int
    float_rate: float | int
    paid_in_capital: float | int
    added_date: int
    def add(self):
        return mento.insert("shares", data=dict(stock=self.stock, name=self.name, sector=self.sector, close=self.close, market_cap_tl=self.market_cap_tl, market_cap_usd=self.market_cap_usd, float_rate=self.float_rate, paid_in_capital=self.paid_in_capital, added_date=self.added_date))