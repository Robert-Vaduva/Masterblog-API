"""
A simple module for managing an SQLite movies database using SQLAlchemy.

Provides functions to retrieve, add, delete, and update movies, handling
common SQLAlchemy exceptions.

Database URL: "sqlite:///data/movies.db"

Functions:
    - get_all_movies()
    - add_movie(title, year, rating, url)
    - delete_movie(title)
    - update_movie(title, rating)
"""


import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError


# Define the database URL
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'movies.db')}"
# Create the engine
DEBUGGING_ACTIVE = False
engine = create_engine(DATABASE_URL, echo=DEBUGGING_ACTIVE)


def get_all_movies():
    """Retrieve all movies from the database."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT title, year, rating, url FROM movies"))
            movies = result.fetchall()
            return {row[0]: {"year": row[1],
                             "rating": row[2],
                             "url": row[3]} for row in movies}
    except IntegrityError as error:
        print(f"Get - Integrity error: {error.orig}")
    except OperationalError as error:
        print(f"Get - Operational error: {error.orig}")
    except SQLAlchemyError as error:
        print(f"Get - Database error: {error}")
    return None


def add_movie(title, year, rating, url):
    """Add a new movie to the database."""
    try:
        with engine.connect() as connection:
            connection.execute(text("INSERT INTO movies (title, year, rating, url) "
                                    "VALUES (:title, :year, :rating, :url)"),
                               {"title": title, "year": year, "rating": rating, "url": url})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
    except IntegrityError as error:
        print(f"Add - Integrity error: {error.orig}")
    except OperationalError as error:
        print(f"Add - Operational error: {error.orig}")
    except SQLAlchemyError as error:
        print(f"Add - Database error: {error}")


def delete_movie(title):
    """Delete a movie from the database."""
    try:
        with engine.connect() as connection:
            connection.execute(text("DELETE FROM movies WHERE title=:title"), {"title": title})
            connection.commit()
            print(f"Movie '{title}' deleted successfully.")
    except IntegrityError as error:
        print(f"Del - Integrity error: {error.orig}")
    except OperationalError as error:
        print(f"Del - Operational error: {error.orig}")
    except SQLAlchemyError as error:
        print(f"Del - Database error: {error}")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    try:
        with engine.connect() as connection:
            connection.execute(text("UPDATE movies SET rating=:rating WHERE title=:title"),
                               {"title": title, "rating": rating})
            connection.commit()
            print(f"Movie '{title}' updated successfully.")
    except IntegrityError as error:
        print(f"Upd - Integrity error: {error.orig}")
    except OperationalError as error:
        print(f"Upd - Operational error: {error.orig}")
    except SQLAlchemyError as error:
        print(f"Upd - Database error: {error}")
