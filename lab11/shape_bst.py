"""
W11 Lab: BST for Shape class (from lab09 group project)
Group Lab - Option 1: Using existing sortable class from project

This integrates with the Shape class from lab09 shape_parser.py
Shapes are sorted by dist_traveled (distance along route)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Any


# =============================================================================
# Shape Class (from lab09 - made sortable)
# =============================================================================
@dataclass
class Shape:
    """
    Shape point from GTFS shapes.txt (from lab09 group project).
    Added comparison operators for BST sorting by dist_traveled.

    Examples:
        >>> s1 = Shape("1", 49.0, -123.0, 1, 100.0)
        >>> s2 = Shape("1", 49.1, -123.1, 2, 200.0)
        >>> s1 < s2
        True
    """
    id: str
    lat: float
    lon: float
    sequence: int
    dist_traveled: float

    def __lt__(self, other: Shape) -> bool:
        return self.dist_traveled < other.dist_traveled

    def __le__(self, other: Shape) -> bool:
        return self.dist_traveled <= other.dist_traveled

    def __gt__(self, other: Shape) -> bool:
        return self.dist_traveled > other.dist_traveled

    def __ge__(self, other: Shape) -> bool:
        return self.dist_traveled >= other.dist_traveled

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Shape):
            return NotImplemented
        return self.dist_traveled == other.dist_traveled and self.id == other.id

    def __repr__(self) -> str:
        return f"Shape({self.id}, seq={self.sequence}, dist={self.dist_traveled})"


# =============================================================================
# BST Node
# =============================================================================
@dataclass
class BSTNode:
    """A node in the BST."""
    data: Any
    left: Optional[BSTNode] = None
    right: Optional[BSTNode] = None


# =============================================================================
# ShapeBST - BST for Shape objects
# =============================================================================
@dataclass
class ShapeBST:
    """
    BST for Shape objects from group project.
    Sorts shapes by dist_traveled.
    """
    root: Optional[BSTNode] = None

    # -------------------------------------------------------------------------
    # Setters
    # -------------------------------------------------------------------------
    def add(self, shape: Shape) -> bool:
        """
        Add a shape to the BST.

        Signature: Shape -> bool
        Purpose: Insert shape sorted by dist_traveled.

        Examples:
            >>> tree = ShapeBST()
            >>> tree.add(Shape("1", 49.0, -123.0, 1, 100.0))
            True
        """
        if self.root is None:
            self.root = BSTNode(shape)
            return True
        return self._add_helper(self.root, shape)

    def _add_helper(self, node: BSTNode, shape: Shape) -> bool:
        if shape < node.data:
            if node.left is None:
                node.left = BSTNode(shape)
                return True
            return self._add_helper(node.left, shape)
        else:
            if node.right is None:
                node.right = BSTNode(shape)
                return True
            return self._add_helper(node.right, shape)

    # -------------------------------------------------------------------------
    # Getters
    # -------------------------------------------------------------------------
    def contains(self, shape: Shape) -> bool:
        """
        Check if shape exists in BST.

        Signature: Shape -> bool
        Purpose: Search for a shape.
        """
        return self._contains_helper(self.root, shape)

    def _contains_helper(self, node: Optional[BSTNode], shape: Shape) -> bool:
        if node is None:
            return False
        if shape == node.data:
            return True
        if shape < node.data:
            return self._contains_helper(node.left, shape)
        return self._contains_helper(node.right, shape)

    def get_min(self) -> Optional[Shape]:
        """Get shape with smallest dist_traveled."""
        if self.root is None:
            return None
        return self._get_min_node(self.root).data

    def _get_min_node(self, node: BSTNode) -> BSTNode:
        if node.left is None:
            return node
        return self._get_min_node(node.left)

    def get_max(self) -> Optional[Shape]:
        """Get shape with largest dist_traveled."""
        if self.root is None:
            return None
        return self._get_max_node(self.root).data

    def _get_max_node(self, node: BSTNode) -> BSTNode:
        if node.right is None:
            return node
        return self._get_max_node(node.right)

    def get_size(self) -> int:
        """Return number of shapes in BST."""
        return self._size_helper(self.root)

    def _size_helper(self, node: Optional[BSTNode]) -> int:
        if node is None:
            return 0
        return 1 + self._size_helper(node.left) + self._size_helper(node.right)

    # -------------------------------------------------------------------------
    # Deleters
    # -------------------------------------------------------------------------
    def delete(self, shape: Shape) -> bool:
        """
        Delete a shape from BST.

        Signature: Shape -> bool
        Purpose: Remove shape while keeping BST property.
        """
        if not self.contains(shape):
            return False
        self.root = self._delete_helper(self.root, shape)
        return True

    def _delete_helper(self, node: Optional[BSTNode], shape: Shape) -> Optional[BSTNode]:
        if node is None:
            return None

        if shape < node.data:
            node.left = self._delete_helper(node.left, shape)
        elif shape > node.data:
            node.right = self._delete_helper(node.right, shape)
        else:
            if node.left is None and node.right is None:
                return None
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = self._get_min_node(node.right)
            node.data = successor.data
            node.right = self._delete_helper(node.right, successor.data)
        return node

    def clear(self) -> None:
        """Remove all shapes."""
        self.root = None

    # -------------------------------------------------------------------------
    # Traversals
    # -------------------------------------------------------------------------
    def inorder(self) -> List[Shape]:
        """Return shapes sorted by dist_traveled."""
        result = []
        self._inorder_helper(self.root, result)
        return result

    def _inorder_helper(self, node: Optional[BSTNode], result: List[Shape]) -> None:
        if node is None:
            return
        self._inorder_helper(node.left, result)
        result.append(node.data)
        self._inorder_helper(node.right, result)

    # -------------------------------------------------------------------------
    # Utility
    # -------------------------------------------------------------------------
    def print_tree(self) -> None:
        """Print BST structure."""
        if self.root is None:
            print("Empty tree")
            return
        self._print_helper(self.root, 0, "Root: ")

    def _print_helper(self, node: BSTNode, level: int, prefix: str) -> None:
        print(" " * (level * 4) + prefix + str(node.data))
        if node.left or node.right:
            if node.left:
                self._print_helper(node.left, level + 1, "L-- ")
            if node.right:
                self._print_helper(node.right, level + 1, "R-- ")


# =============================================================================
# Demo
# =============================================================================
if __name__ == "__main__":
    print("ShapeBST Demo - using Shape class from lab09")
    print("=" * 50)

    # Sample shapes like from shapes.txt
    shapes = [
        Shape("route1", 49.0, -123.0, 1, 0.0),
        Shape("route1", 49.1, -123.1, 2, 150.5),
        Shape("route1", 49.2, -123.2, 3, 320.0),
        Shape("route1", 49.3, -123.3, 4, 480.5),
        Shape("route1", 49.4, -123.4, 5, 650.0),
    ]

    tree = ShapeBST()
    print("\nAdding shapes:")
    for s in shapes:
        tree.add(s)
        print(f"  Added: {s}")

    print("\nBST Structure:")
    tree.print_tree()

    print(f"\nSize: {tree.get_size()}")
    print(f"Min dist: {tree.get_min()}")
    print(f"Max dist: {tree.get_max()}")

    print("\nShapes sorted by distance:")
    for s in tree.inorder():
        print(f"  {s}")

    print("\nDeleting shape with dist=150.5...")
    tree.delete(Shape("route1", 49.1, -123.1, 2, 150.5))
    print(f"New size: {tree.get_size()}")
