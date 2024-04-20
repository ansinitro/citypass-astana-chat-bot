from typing import Union
from pydantic import BaseModel


class Coordinates(BaseModel):
    longitude: str
    latitude: str
