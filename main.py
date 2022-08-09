from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.core.database.settings import engine, Base, get_db
from src.core.database import models
from src.core.schemas import schema
from sqlalchemy.orm import Session
from src.core.services import get_location, get_route_distance
from datetime import datetime

app = FastAPI()

origins = [
    "localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get('/')
async def read_all_routes(db: Session = Depends(get_db)):
    return db.query(models.DeliveryRoute).all()


@app.get('/location')
async def get_location_address(query: str):
    locations = get_location(query=query, first=False)
    return [i['display_name'] for i in locations]


@app.post('/')
async def create_route(route: schema.DeliveryRoute, db: Session = Depends(get_db)):
    try:
        origin = get_location(query=route.origin_location)
        destiny = get_location(query=route.destiny_location)

        lat1, lon1 = origin['lat'], origin['lon']
        lat2, lon2 = destiny['lat'], destiny['lon']

        distance_path = get_route_distance(lat1, lon1, lat2, lon2)
    except:
        raise HTTPException(status_code=404)

    delivery_route = models.DeliveryRoute()

    delivery_route.origin_osm_id = origin['osm_id']
    delivery_route.origin_osm_type = origin['osm_type']
    delivery_route.origin_location = origin['display_name']

    delivery_route.destiny_osm_id = destiny['osm_id']
    delivery_route.destiny_osm_type = destiny['osm_type']
    delivery_route.destiny_location = destiny['display_name']

    delivery_route.distance_path = distance_path

    db.add(delivery_route)
    db.commit()


    return [
            {
                "created_at": datetime.now(),
                "destiny_location": delivery_route.destiny_location,
                "origin_location": delivery_route.origin_location,
                "distance_path": delivery_route.distance_path,
            }
        ]