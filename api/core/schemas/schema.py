from pydantic import BaseModel, Field
from typing import Optional

class DeliveryRoute(BaseModel):
    origin_location: str
    destiny_location: str
