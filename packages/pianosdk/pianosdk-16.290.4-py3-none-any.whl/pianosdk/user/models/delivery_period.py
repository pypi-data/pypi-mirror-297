from datetime import date, datetime
from pydantic.main import BaseModel
from typing import Optional


class DeliveryPeriod(BaseModel):
    address_pub_id: Optional[str] = None
    to: Optional[str] = None
    delivery_period_pub_id: Optional[str] = None
    _from: Optional[str] = None


DeliveryPeriod.model_rebuild()
