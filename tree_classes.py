from typing import Any, Optional


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

    def add_subtree(self, subtree) -> None:
        """Adds a subtree to this tree."""
        self._subtrees.append(subtree)

    def get_subtrees(self) -> list[Any]:
        """Returns the subtrees of this tree"""
        return self._subtrees


class AlbumTree(Tree):
    """A tree that represents albums in a hierarchical structure, each subtree is an album of the root genre."""

    def __init__(self, root: Optional[Any], subtrees: list[Any]) -> None:
        super().__init__(root, subtrees)
