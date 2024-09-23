from datetime import date, datetime
from pydantic.main import BaseModel
from typing import Optional
from pianosdk.user.models.delivery_period import DeliveryPeriod
from typing import List


class DeliverySchedule(BaseModel):
    main_address_pub_id: Optional[str] = None
    delivery_periods: Optional['List[DeliveryPeriod]'] = None


DeliverySchedule.model_rebuild()
