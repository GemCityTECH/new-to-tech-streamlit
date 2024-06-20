from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from streamlit_sqlalchemy import StreamlitAlchemyMixin

Base = declarative_base()

# TODO this table might perform better with an ID column and some indexes
class Geo(Base, StreamlitAlchemyMixin):
    __tablename__ = "geo"

    id = Column(Integer, nullable=False, primary_key=True)
    state_name = Column(String, nullable=False)
    county = Column(String, nullable=False)
    city = Column(String, nullable=True)

    monitoring_sites = relationship("MonitoringSite", back_populates="geo")

    __table_args__ = (UniqueConstraint('state_name', 'county', 'city'),)
    
class MonitoringSite(Base, StreamlitAlchemyMixin):
    __tablename__ = "monitoring_site"

    geo_id = Column(Integer, ForeignKey("geo.id"))
    geo = relationship("Geo", foreign_keys=[geo_id])

    site_num = Column(Integer, nullable=False, primary_key=True)
    latitude = Column(Float, nullable=False, primary_key=True)
    longitude = Column(Float, nullable=False, primary_key=True)