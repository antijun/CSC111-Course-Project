"""CSC111 Project Phase 2: Interactive Music Genre and Album Recommendation Tree (Tree Structures)

Description
===============================

This Python module contains the Tree class and a couple of the standard tree methods. The child class of Tree, AlbumTree
, is also found here.

This file is Copyright (c) 2023 David Wu and Kevin Hu.
"""
from typing import Any, Optional


# @check_contracts
class Tree:
    """A recursive tree data structure.

    Private Instance Attributes:
      - _root: The item stored at this tree's root, or None if the tree is empty.
      - _subtrees: The list of subtrees of this tree. When the tree is empty, this attribute is empty when self._root is
       None. This attribute may also be empty if self._root is not None, representing a tree with just one item at the
       root

    Representation Invariants:
        - self._root is not None or self._subtrees == []
        - all(not subtree.is_empty() for subtree in self._subtrees)
    """
    _root: Optional[Any]
    _subtrees: list[Any]

    def __init__(self, root: Optional[Any], subtrees: list[Any]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        Preconditions:
            - root is not none or subtrees == []
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Returns whether this tree is empty."""
        return self._root is None

    def root(self) -> Any:
        """Returns the root of this tree."""
        return self._root

    def add_subtree(self, subtree) -> None:
        """Adds a subtree to this tree."""
        self._subtrees.append(subtree)

    def get_subtrees(self) -> list[Any]:
        """Returns the subtrees of this tree"""
        return self._subtrees


class AlbumTree(Tree):
    """A child class of Tree that represents albums in a hierarchical structure. Each subtree is an album of the root
    album.
    """

    def __init__(self, root: Optional[Any], subtrees: list[Any]) -> None:
        """Initialize a new AlbumTree with the given root value and subtrees.

        Preconditions:
            - root is not none or subtrees == []
        """
        super().__init__(root, subtrees)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'disable': [],
        'max-line-length': 120
    })
