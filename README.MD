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

- Add a 'genre' field to Book. Make sure that you can see this field using `GET /books` and update it using `PUT /books/{id}`.

- Add an endpoint that lets you `GET` a book by author and/or publication year.

- Add a `GET` endpoint that shows the average rating across all books.

- Add support for multiple ratings - and reviewers - per book, and to view both individual reviews and the average review score for a book.

### Moderate

- Add [caching](https://docs.streamlit.io/develop/concepts/architecture/caching) to the application where appropriate

- Return the summary and ratings for a book using [Goodreads' API](https://www.goodreads.com/api/index).

- Return author biographies using [Wikipedia's API](https://api.wikimedia.org/wiki/Getting_started_with_Wikimedia_APIs).

- Rework this book-based sample app into a different domain: customer tracking, RPG character creator, pizza store, etc.

### Complex

- Add an ORM tool such as SQLAlchemy and use it to persist data between runs.

- Migrate the app's API to GraphQL.

- Dockerize the app.

- Host/deploy the app publicly.

- Build a small JS UI in front of the API.


Parameter classes: https://aqs.epa.gov/aqsweb/documents/codetables/parameter_classes.html