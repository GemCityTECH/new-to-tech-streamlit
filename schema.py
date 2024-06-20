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
    id: int
    geo: Geo

    model_config = ConfigDict(from_attributes=True)

class MeasurementBase(BaseModel):
    monitoring_site_id: int
    parameter_code: int | None
    parameter_name: str
    datum: str
    sample_duration: str
    pollutant_standard: str | None
    metric_used: str | None
    method_name: str | None
    year: int
    units_of_measure: str
    observation_count: int
    observation_percent: int # Yes really
    arithmetic_mean: float
    arithmetic_standard_dev: float
    percentile_99: float
    percentile_90: float

class Measurement(MeasurementBase):
    id: int

    model_config = ConfigDict(from_attributes=True)