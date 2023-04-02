import csv
from typing import Optional


class Genre:
    """
    A class to represent a genre.
    """
    name: str
    parent_genre: Optional[str]

    def __init__(self, name, parent_genre):
        self.name = name
        self.parent_genre = parent_genre


def create_genres() -> list[Genre]:
    """
    This function creates the full list of genres.
    """
    genres = []
    with open('datasets/genres_dataset.csv', 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            name = row[0]
            if row[1] == 'NA':
                parent_genre = None
            else:
                parent_genre = row[1]
            genre = Genre(name, parent_genre)
            genres.append(genre)
    return genres
