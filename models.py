from typing import List
from pydantic import BaseModel, Field
from datetime import date

class VideoGame(BaseModel):
    name: str = Field(..., min_length=1)
    release_date: date
    studio: str = Field(..., min_length=1)
    ratings: int = Field(..., ge=0, le=20)  # Exemple : note entre 0 et 20
    platforms: List[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "The Witcher 3 : Wild Hunt",
                "release_date": "2015-05-19",
                "studio": "CD Projekt RED",
                "ratings": 19,
                "platforms": ["PC", "PS4", "PS5", "Switch", "One"]
            }
        }

test_db: List[VideoGame] = [
    VideoGame(
        name="The Witcher 3 : Wild Hunt",
        release_date="2015-05-19",
        studio="CD Projekt RED",
        ratings=19,
        platforms=["PC", "PS4", "PS5", "Switch", "One"]
    ),
    VideoGame(
        name="Mario Kart 8 Deluxe",
        release_date="2017-04-28",
        studio="Nintendo",
        ratings=16,
        platforms=["Switch"]
    ),
    VideoGame(
        name="Don't Starve",
        release_date="2013-04-23",
        studio="Capybara Games",
        ratings=17,
        platforms=["PC", "PS4", "Switch", "One", "WiiU", "PS3"]
    )
]