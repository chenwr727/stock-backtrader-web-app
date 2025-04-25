import datetime
from typing import Any, Dict

from pydantic import BaseModel


class AkshareParams(BaseModel):
    """AkshareParams 模型"""

    symbol: str
    period: str
    start_date: str
    end_date: str
    adjust: str


class BacktraderParams(BaseModel):
    """BacktraderParams 模型"""

    start_date: datetime.date
    end_date: datetime.date
    start_cash: float
    commission_fee: float
    stake: int


class StrategyBase(BaseModel):
    """策略基础模型"""

    name: str
    params: Dict[str, Any]
