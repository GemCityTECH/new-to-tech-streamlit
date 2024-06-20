from pathlib import Path
import os

import streamlit as st

import csv_loader
import crud
from model import Base
from streamlit_sqlalchemy import StreamlitAlchemyMixin

SQLITE_DATABASE_FILE = "aq_data.db"

def main():
    if not Path(SQLITE_DATABASE_FILE).exists():
        Base.metadata.create_all(CONNECTION.engine)
        StreamlitAlchemyMixin.st_initialize(connection=CONNECTION)
        
        # Populate database
        with CONNECTION.session as session:
            st_init = st.warning("Initializing DB", icon="🔥")
            loader = csv_loader.EPACSVLoader()
            geos = loader.load_and_deserialize()
            crud.create_geos(session, geos)
            st_init.empty()
    else:
        StreamlitAlchemyMixin.st_initialize(connection=CONNECTION)

    app()


def app() -> None:
    st.header("Streamlit: EPA air quality data 2023")
    #render_sidebar(session)


if __name__ == "__main__":
    # initialize the database connection
    # (see https://docs.streamlit.io/library/api-reference/connections/st.connection)
    CONNECTION = st.connection("aq_data_db", type="sql")
    main()