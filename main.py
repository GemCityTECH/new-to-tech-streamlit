from pathlib import Path
import pandas
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
            loader.load_and_deserialize(session)
            st_init.empty()
    else:
        StreamlitAlchemyMixin.st_initialize(connection=CONNECTION)

    app()


def app() -> None:
    st.header("Streamlit: EPA air quality data 2023")
    with CONNECTION.session as session:
        render_sidebar(session)

def render_sidebar(session) -> None:
    views = {
        "Readme": render_readme,
        "Monitoring Sites": render_monitoring_sites,
    }
    choice = st.sidebar.radio("Go To Page:", views.keys())
    render_func = views.get(choice)
    render_func(session)

def render_readme(*_) -> None:
    st.write(Path("README.MD").read_text())

def render_monitoring_sites(session) -> None:
    st.subheader("Monitoring Sites")
    st.map(
        pandas.DataFrame([x.model_dump() for x in crud.get_monitoring_sites(session)]),
        longitude = 'longitude',
        latitude = 'latitude'
    )

if __name__ == "__main__":
    # initialize the database connection
    # (see https://docs.streamlit.io/library/api-reference/connections/st.connection)
    CONNECTION = st.connection("aq_data_db", type="sql")
    main()