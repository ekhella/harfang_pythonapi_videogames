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
