from pydantic import BaseModel
from typing import Optional

class DatasasiaBase(BaseModel):
    datetime: str
    temperature: float
    humidity: float
    windspeed: float
    general_diffuse_flows: float
    diffuse_flows: float
    power_consumption_zone1: float
    power_consumption_zone2: float
    power_consumption_zone3: float

class DatasasiaCreate(DatasasiaBase):
    pass

class DatasasiaUpdate(BaseModel):
    temperature: Optional[float]
    humidity: Optional[float]
    windspeed: Optional[float]
    general_diffuse_flows: Optional[float]
    diffuse_flows: Optional[float]
    power_consumption_zone1: Optional[float]
    power_consumption_zone2: Optional[float]
    power_consumption_zone3: Optional[float]

class Datasasia(DatasasiaBase):
    id: int

    class Config:
        orm_mode = True
