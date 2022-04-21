from typing import List, Optional

from pydantic import BaseModel, Field

#Payload SCHEMAS
class Fuels(BaseModel):
    gasfired: float = Field(alias="gas(euro/MWh)")
    turbojet: float = Field(alias="kerosine(euro/MWh)")
    co2: float = Field(alias="co2(euro/ton)")
    windturbine: float = Field(alias="wind(%)")
    
    def __getitem__(self, item):
        return getattr(self, item)
    

class Powerplant(BaseModel):
    name: str
    type: str
    efficiency: float
    pmin: int
    pmax: int

class Payload(BaseModel):
    load: int
    fuels: Fuels
    powerplants: List[Powerplant]

    class Config:
        orm_mode = True




#Response SCHEMAS
class PowerplantResult(BaseModel):
    name: str
    p: float
