import csv
# import pandas as pd


class Album:
    """
    A class to represent an album.
    """
    name: str
    artist: str
    genres: list[str]
    rank: int
    release: str
    descriptors: list[str]

    def __init__(self, name, artist, genres, rank, release, descriptors):
        self.name = name
        self.artist = artist
        self.genres = genres
        self.rank = rank
        self.release = release
        self.descriptors = descriptors


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
