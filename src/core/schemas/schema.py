from pydantic import BaseModel, Field

class DeliveryRoute(BaseModel):
    origin_location: str
    destiny_location: str
