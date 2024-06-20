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

    id = Column(Integer, nullable=False, primary_key=True)
    site_num = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

class Measurement(Base, StreamlitAlchemyMixin):
    __tablename__ = "measurement"

    monitoring_site_id = Column(Integer, ForeignKey("monitoring_site.id"))
    monitoring_site = relationship("MonitoringSite", foreign_keys=[monitoring_site_id])

    id = Column(Integer, nullable=False, primary_key=True)
    parameter_code = Column(Integer, nullable=True)
    parameter_name = Column(String, nullable=False)
    datum = Column(String, nullable=False)
    sample_duration = Column(String, nullable=False)
    pollutant_standard = Column(String, nullable=True)
    metric_used = Column(String, nullable=True)
    method_name = Column(String, nullable=True)
    year = Column(Integer, nullable=False)
    units_of_measure = Column(String, nullable=False)
    observation_count = Column(Integer, nullable=False)
    observation_percent = Column(Integer, nullable=False)
    arithmetic_mean = Column(Float, nullable=False)
    arithmetic_standard_dev = Column(Float, nullable=False)
    percentile_99 = Column(Float, nullable=False)
    percentile_90 = Column(Float, nullable=False)