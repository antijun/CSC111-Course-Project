from typing import Any, Optional
from albums_data import Album, albums
from genres_data import Genre, genres


class Tree:
    """Abstract Tree Class"""
    _root: Optional[Any]
    _subtrees: list[Any]

    def __init__(self, root: Optional[Any], subtrees: list[Any]) -> None:
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Returns whether this tree is empty."""
        return self._root is None

    @property
    def subtrees(self):
        """Returns the subtrees of this tree."""
        return self._subtrees

    @property
    def root(self):
        """Returns the root of this tree."""
        return self._root

    def add_subtree(self, subtree) -> None:
        """Add a subtree to this game tree."""
        self._subtrees.append(subtree)

    def get_subtrees(self) -> list[Any]:
        """Add a subtree to this game tree."""
        return self._subtrees


class GenreTree(Tree):
    """A tree that represents genres in a hierarchical structure, each subtree is a subgenre of the root genre."""

    def __init__(self, root: Optional[Any], subtrees: list[Any]) -> None:
        super().__init__(root, subtrees)


class AlbumTree(Tree):
    """A tree that represents albums in a hierarchical structure, each subtree is an album of the root genre."""

    def __init__(self, root: Optional[Any], subtrees: list[Any]) -> None:
        super().__init__(root, subtrees)


# parent_genres = {genre.parent_genre for genre in genres}


def create_genre_tree(genre_list: list[Genre]) -> GenreTree:
    """Creates a GenreTree that contains all the genres in the genres dataset."""
    parent_genres = {genre.parent_genre for genre in genre_list}
