from sqlalchemy import Column, Integer, String, DateTime, Float, func
from .settings import Base
from datetime import datetime

class DeliveryRoute(Base):
    __tablename__ = 'deliveryroute'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    origin_osm_id = Column(Integer)
    origin_osm_type = Column(String(30))
    origin_location = Column(String)

    destiny_osm_id = Column(Integer)
    destiny_osm_type = Column(String(30))
    destiny_location = Column(String)
    distance_path = Column(Float)