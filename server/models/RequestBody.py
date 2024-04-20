from typing import Union
from pydantic import BaseModel
from .Coordinates import Coordinates


class RequestBody(BaseModel):
    sight_name: str
    user_geolocation: Union[Coordinates, None] = None
