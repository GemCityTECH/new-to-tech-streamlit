from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from streamlit_sqlalchemy import StreamlitAlchemyMixin

Base = declarative_base()

# TODO this table might perform better with an ID column and some indexes
class Geo(Base, StreamlitAlchemyMixin):
    __tablename__ = "geo"

    state_name = Column(String, nullable=False, primary_key=True)
    county = Column(String, nullable=False, primary_key=True)
    city = Column(String, nullable=True, primary_key=True)
    
    # TODO can you add these columns?
    # latitude = Column(String, nullable=True)
    # longitude = Column(String, nullable=True)
