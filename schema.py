from pydantic import BaseModel, ConfigDict

class Geo(BaseModel):
    state_name: str
    county: str
    city: str | None
    
    # ORM magic that automatically creates schema.Geo from model.Geo
    model_config = ConfigDict(from_attributes=True)