from pydantic import BaseModel


class StrategyBase(BaseModel):
    name: str
    params: dict
