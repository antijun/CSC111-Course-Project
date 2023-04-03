"""CSC111 Project Phase 2: Interactive Music Genre and Album Recommendation Tree (Album Data)

Description
===============================

This Python module contains the Album class which is used to identify the albums obtained from the data found in
rym_clean1.csv.

This file is Copyright (c) 2023 David Wu and Kevin Hu.
"""
import csv


# @check_contracts
class Album:
    """A class to represent a musical album.

    Instance Attributes:
        - name: The name of the album
        - artist: The artist/creator of the album
        - genres: A list of the genres associated with the album
        - rank: A number ranking based on the popularity of the album, measured through the number of review the album.
            The lower the value of rank, the higher the popularity
        - release: The date of release of the album in the form 'year-month-day'
        - descriptors: A list of descriptors/adjectives associated with the album

    Representation Invariants:
        - self.name != ''
        - self.artist != ''
        - self.genres != []
        - self.rank > 0
        - self.release is a valid date an in the form 'year-month-day'
        - self.descriptors != []
    """
    name: str
    artist: str
    genres: list[str]
    rank: int
    release: str
    descriptors: list[str]

    def __init__(self, name: str, artist: str, genres: list[str], rank: int, release: str,
                 descriptors: list[str]) -> None:
        """Initialize a new album with the given name, artist, genres, rank, release date, and decriptors.
        """
        self.name = name
        self.artist = artist
        self.genres = genres
        self.rank = rank
        self.release = release
        self.descriptors = descriptors


def create_albums() -> list[Album]:
    """This function creates a full list of albums using the data from rym_clean1.csv. Each element in the output list
    is an Album instance.
    """
    albums = []
    with open('datasets/rym_clean1.csv', 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            name = row[2]
            artist = row[3]
            if row[7] != 'NA':
                genres = row[6].split(', ') + row[7].split(', ')
            else:
                genres = row[6].split(', ')
            rank = int(row[1])
            release = row[4]
            descriptors = row[7].split(', ')
            album = Album(name, artist, genres, rank, release, descriptors)
            albums.append(album)
    return albums


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['csv'],  # the names (strs) of imported modules
        'allowed-io': ['create_albums'],  # the names (strs) of functions that call print/open/input
        'disable': ['too-many-arguments'],
        'max-line-length': 120
    })
