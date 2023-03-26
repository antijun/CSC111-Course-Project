from typing import Any, Optional
from albums_data import Album, albums

class Tree:
    """Abstract Tree Class"""

    _root: Optional[Any]
    _subtrees: list[Tree]

    def __init__(self, root: Optional[Any], subtrees: list[AbstractTree]) -> None:
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Returns whether this tree is empty."""
        return self._root is None


class GenreTree(Tree):
    """A tree that represents genres in a hierarchical structure, each subtree is a subgenre of the root genre."""
    pass


class AlbumTree(Tree):
    """A tree that represents albums in a hierarchical structure, each subtree is an album of the root genre."""
