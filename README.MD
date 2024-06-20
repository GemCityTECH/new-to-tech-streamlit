# GCT-Rest

A sample repository to support New To Tech sessions exploring databases for [Gem City Tech](https://gemcity.tech/).

Basic app structure shamelessly stolen from [here](https://home.gerardbentley.com/blog/streamlit-fullstack/).

See relevant presentations:

- [RDBMS](https://docs.google.com/presentation/d/1cmLywUwfPG6yc__uEnZ49O2Cemh6x4fI4CyGgDx_o2I/edit?usp=sharing)
- [Data Structures](https://docs.google.com/presentation/d/13P_k7j2VxEfq7kFk3gwkf90bCYeEUwDsFpwkA4Nr6G4/edit?usp=sharing)
- [Database Decisions](https://docs.google.com/presentation/d/11_EXPhHBXfTu1a_QX-bj2Tua2JwFg8tp_OF8d4qqk80/edit?usp=sharing)

## How to run

### Prerequisites

You must have Python 3.12 and [Poetry](https://python-poetry.org/docs/#installation) installed.

### Execution

Ensuring that you have Poetry available in your terminal, run

```bash
poetry shell
```

to use Poetry's virtual environment, and then

```bash
poetry install
```

to install Streamlit and the other dependencies. Then, run the app using Streamlit:

```bash
streamlit run main.py
```

## Suggested Exercises

### Starting Out

- Add the 'address' field to the database (which model class does it belong in?)

- Add a page (reachable from the sidebar) which allows you to search for and display a Geo

- Display all measurement sites in the above Geo both in a table and on a map

- Add forms where Geos and/or Measurement Sites can be created, updated, and deleted

- Display measurement data

### More Involved

- Add [caching](https://docs.streamlit.io/develop/concepts/architecture/caching) to the application where appropriate

- Grab measurement data for previous years [here](https://aqs.epa.gov/aqsweb/airdata/download_files.html) and incorporate them into the app

- Create a map of measurement sites where measurements (selectable from a dropdown) exceed a threshold (set by a slider)
