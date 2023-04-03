"""CSC111 Project Phase 2: Interactive Music Genre and Album Recommendation Tree (Genre Data)

Description
===============================

This Python module contains the Genre class which is used to identify the genres obtained from the data found in 
genres_dataset.csv.

This file is Copyright (c) 2023 David Wu and Kevin Hu.
"""


import csv
from typing import Optional


# @check_contracts
class Genre:
    """A class to represent a musical genre.

    Instance Attributes:
        - name: the name of the genre
        - parent_genre: the name of theparent genre of the genre(if the genre is a subgenre, it will have a parent
            genre), if genre is instead a main genre with no parnet genre, this attribtue is set to None

    Representation Invariants:
        - self.name != ''
    """
    name: str
    parent_genre: Optional[str]

    def __init__(self, name: str, parent_genre: Optional[str]) -> None:
        self.name = name
        self.parent_genre = parent_genre


def create_genres() -> list[Genre]:
    """This function creates a full list of genres using the data from genres_dataset.csv. Each element in the element
    is a Genre instance.
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


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['csv'],  # the names (strs) of imported modules
        'allowed-io': ['create_genres'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
