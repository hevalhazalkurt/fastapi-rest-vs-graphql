import asyncio
import os
import sys
from uuid import uuid4

from pydantic import BaseModel
from sqlalchemy import insert

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.db.session import AsyncSessionLocal
from app.models.association_tables import MovieGenreAssociation
from app.models.director import Director
from app.models.genre import Genre
from app.models.movie import Movie

CSV_FILE_PATH = "data/dummy_data.csv"


class DummyData(BaseModel):
    title: str
    year: int
    director: str
    genre: list[str]


async def get_file_data():
    try:
        with open(CSV_FILE_PATH) as csv_file:
            dummy_movie_data = csv_file.readlines()
    except Exception as e:
        print(f"Error for reading {CSV_FILE_PATH}: {e}")

    return dummy_movie_data[1::]


async def seed_dummy_data():
    directors_to_create: dict = dict()
    genres_to_create: dict = dict()
    movies_to_create: dict = dict()
    associations_to_create = []

    async with AsyncSessionLocal() as db:
        print("\nGetting dummy data...")
        processed = 0
        movie_data = await get_file_data()

        print("\nProcessing data...")
        for data in movie_data:
            movie_title, movie_year, director_name, genres = data.strip().split(",")

            director = directors_to_create.get(director_name, {"uuid": uuid4(), "name": director_name})
            if director_name not in directors_to_create:
                directors_to_create[director_name] = director

            movie = movies_to_create.get(
                movie_title, {"uuid": uuid4(), "title": movie_title, "release_year": int(movie_year), "director_id": director["uuid"]}
            )
            if movie_title not in movies_to_create:
                movies_to_create[movie_title] = movie

            for genre_name in genres.split("|"):
                genre = genres_to_create.get(genre_name, {"uuid": uuid4(), "name": genre_name})
                if genre_name not in genres_to_create:
                    genres_to_create[genre_name] = genre

                associations_to_create.append({"movie_id": movie["uuid"], "genre_id": genre["uuid"]})

            processed += 1

        print(
            f"Total directors to create: {len(directors_to_create)}, total genres to create: {len(genres_to_create)}, total movies to create: {len(movies_to_create)}"
        )

        print("\nCreating genres...")
        try:
            await db.execute(
                insert(Genre).values(list(genres_to_create.values())),
            )
        except Exception as e:
            print(f"Error for creating genres: {e}")

        print("\nCreating directors...")
        try:
            await db.execute(
                insert(Director).values(list(directors_to_create.values())),
            )
        except Exception as e:
            print(f"Error for creating directors: {e}")

        print("\nCreating movies...")
        try:
            await db.execute(
                insert(Movie).values(list(movies_to_create.values())),
            )
        except Exception as e:
            print(f"Error for creating movies: {e}")

        print("\nCreating movie-genre associations...")
        try:
            await db.execute(
                insert(MovieGenreAssociation).values(associations_to_create),
            )
        except Exception as e:
            print(f"Error for creating movies: {e}")

        print(f"Total processed movies: {processed}")
        await db.commit()


async def main():
    await seed_dummy_data()


if __name__ == "__main__":
    asyncio.run(main())
