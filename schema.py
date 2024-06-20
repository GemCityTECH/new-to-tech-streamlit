from pydantic import BaseModel, ConfigDict

class GeoBase(BaseModel):
    state_name: str
    county: str
    city: str | None

    def __hash__(self) -> int:
        return hash((type(self),) + tuple(self.__dict__.values()))

class Geo(GeoBase):
    id: int
    
    # ORM magic that automatically creates schema.Geo from model.Geo
    model_config = ConfigDict(from_attributes=True)

class MonitoringSiteBase(BaseModel):
    geo_id: int
    site_num: int
    latitude: float
    longitude: float

    def __hash__(self) -> int:
        return hash((type(self),) + (self.site_num, self.latitude, self.longitude))

class MonitoringSite(MonitoringSiteBase):
    geo: Geo

    model_config = ConfigDict(from_attributes=True)
