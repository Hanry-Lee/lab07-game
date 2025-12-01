"""
W11 Lab: FamilyTree Implementation
Using Peppa Pig's Family Tree from https://peppapig.fandom.com/wiki/Pig_Family

A FamilyTree is a special structure where:
- Each parent has one or more partners
- Each child has two parents
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional


# =============================================================================
# Node Data Structure
# =============================================================================
@dataclass
class Node:
    """
    A Node in the FamilyTree representing a family member.

    Attributes:
        name: The name of the family member
        parents: List of parent Nodes (typically 0-2)
        partners: List of partner Nodes (spouses)
        children: List of child Nodes
        siblings: List of sibling Nodes
    """
    name: str
    parents: List[Node] = field(default_factory=list)
    partners: List[Node] = field(default_factory=list)
    children: List[Node] = field(default_factory=list)
    siblings: List[Node] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"Node({self.name})"


# =============================================================================
# FamilyTree Data Structure
# =============================================================================
@dataclass
class FamilyTree:
    """
    A FamilyTree data structure that organizes family members.

    Attributes:
        root: The root node of the tree (typically oldest known ancestor)
        members: Dictionary mapping names to Nodes for easy lookup
    """
    root: Optional[Node] = None
    members: dict = field(default_factory=dict)

    def __post_init__(self):
        """Initialize members dict if root is provided."""
        if self.root:
            self.members[self.root.name] = self.root

    # =========================================================================
    # addParent Function
    # =========================================================================
    def addParent(self, child: Node, parent: Node) -> bool:
        """
        Add a parent to a child node.

        Signature: Node, Node -> bool

        Purpose: Establishes a parent-child relationship by adding the parent
        to the child's parents list and the child to the parent's children list.

        Examples:
            >>> tree = FamilyTree()
            >>> peppa = Node("Peppa")
            >>> mummy = Node("Mummy Pig")
            >>> tree.addParent(peppa, mummy)
            True
            >>> mummy in peppa.parents
            True
            >>> peppa in mummy.children
            True

        Args:
            child: The child Node to add a parent to
            parent: The parent Node to be added

        Returns:
            bool: True if parent was added successfully, False otherwise
        """
        # Check if parent already exists in child's parents
        if parent in child.parents:
            return False

        # Check if child already has 2 parents
        if len(child.parents) >= 2:
            return False

        # Add parent to child's parents list
        child.parents.append(parent)

        # Add child to parent's children list (if not already there)
        if child not in parent.children:
            parent.children.append(child)

        # Add parent to members dict if not already there
        if parent.name not in self.members:
            self.members[parent.name] = parent

        # Add child to members dict if not already there
        if child.name not in self.members:
            self.members[child.name] = child

        return True

    # =========================================================================
    # addChild Function
    # =========================================================================
    def addChild(self, parent: Node, child: Node) -> bool:
        """
        Add a child to a parent node.

        Signature: Node, Node -> bool

        Purpose: Establishes a parent-child relationship by adding the child
        to the parent's children list and the parent to the child's parents list.

        Examples:
            >>> tree = FamilyTree()
            >>> mummy = Node("Mummy Pig")
            >>> george = Node("George")
            >>> tree.addChild(mummy, george)
            True
            >>> george in mummy.children
            True
            >>> mummy in george.parents
            True

        Args:
            parent: The parent Node to add a child to
            child: The child Node to be added

        Returns:
            bool: True if child was added successfully, False otherwise
        """
        # Check if child already exists in parent's children
        if child in parent.children:
            return False

        # Check if child already has 2 parents and this parent isn't one
        if len(child.parents) >= 2 and parent not in child.parents:
            return False

        # Add child to parent's children list
        parent.children.append(child)

        # Add parent to child's parents list (if not already there)
        if parent not in child.parents:
            child.parents.append(parent)

        # Add parent to members dict if not already there
        if parent.name not in self.members:
            self.members[parent.name] = parent

        # Add child to members dict if not already there
        if child.name not in self.members:
            self.members[child.name] = child

        return True

    # =========================================================================
    # addPartner Function
    # =========================================================================
    def addPartner(self, person1: Node, person2: Node) -> bool:
        """
        Add a partner relationship between two nodes.

        Signature: Node, Node -> bool

        Purpose: Establishes a partnership (marriage/spouse) relationship
        between two family members.

        Examples:
            >>> tree = FamilyTree()
            >>> mummy = Node("Mummy Pig")
            >>> daddy = Node("Daddy Pig")
            >>> tree.addPartner(mummy, daddy)
            True
            >>> daddy in mummy.partners
            True
            >>> mummy in daddy.partners
            True

        Args:
            person1: First partner Node
            person2: Second partner Node

        Returns:
            bool: True if partnership was added successfully, False otherwise
        """
        # Check if they are already partners
        if person2 in person1.partners:
            return False

        # Cannot be partner with yourself
        if person1 is person2:
            return False

        # Add each other as partners
        person1.partners.append(person2)
        person2.partners.append(person1)

        # Add both to members dict if not already there
        if person1.name not in self.members:
            self.members[person1.name] = person1
        if person2.name not in self.members:
            self.members[person2.name] = person2

        return True

    # =========================================================================
    # addSibling Function
    # =========================================================================
    def addSibling(self, child: Node, sibling: Node) -> bool:
        """
        Add a sibling relationship between two nodes.

        Signature: Node, Node -> bool

        Purpose: Establishes a sibling relationship between two family members.
        Also shares parents between siblings.

        Examples:
            >>> tree = FamilyTree()
            >>> peppa = Node("Peppa")
            >>> george = Node("George")
            >>> tree.addSibling(peppa, george)
            True
            >>> george in peppa.siblings
            True
            >>> peppa in george.siblings
            True

        Args:
            child: The existing child Node
            sibling: The sibling Node to be added

        Returns:
            bool: True if sibling was added successfully, False otherwise
        """
        # Check if they are already siblings
        if sibling in child.siblings:
            return False

        # Cannot be sibling with yourself
        if child is sibling:
            return False

        # Add each other as siblings
        child.siblings.append(sibling)
        sibling.siblings.append(child)

        # Share parents - add child's parents to sibling
        for parent in child.parents:
            if parent not in sibling.parents and len(sibling.parents) < 2:
                sibling.parents.append(parent)
                if sibling not in parent.children:
                    parent.children.append(sibling)

        # Add both to members dict if not already there
        if child.name not in self.members:
            self.members[child.name] = child
        if sibling.name not in self.members:
            self.members[sibling.name] = sibling

        return True

    # =========================================================================
    # Helper Functions
    # =========================================================================
    def get_member(self, name: str) -> Optional[Node]:
        """Get a family member by name."""
        return self.members.get(name)

    def get_depth(self, node: Optional[Node] = None, visited: set = None) -> int:
        """Calculate the depth of the tree from a given node."""
        if node is None:
            node = self.root
        if node is None:
            return 0

        if visited is None:
            visited = set()

        if node.name in visited:
            return 0
        visited.add(node.name)

        if not node.children:
            return 1

        max_depth = 0
        for child in node.children:
            depth = self.get_depth(child, visited.copy())
            max_depth = max(max_depth, depth)

        return 1 + max_depth

    def get_width(self) -> int:
        """Get the total number of family members."""
        return len(self.members)

    def print_tree(self, node: Optional[Node] = None, level: int = 0, visited: set = None):
        """Print the family tree structure."""
        if node is None:
            node = self.root
        if node is None:
            print("Empty tree")
            return

        if visited is None:
            visited = set()

        if node.name in visited:
            return
        visited.add(node.name)

        indent = "  " * level
        partners_str = ", ".join([p.name for p in node.partners]) if node.partners else "None"
        print(f"{indent}{node.name} (partners: {partners_str})")

        for child in node.children:
            self.print_tree(child, level + 1, visited)


# =============================================================================
# Build Peppa Pig Family Tree
# =============================================================================
def build_peppa_pig_family_tree() -> FamilyTree:
    """
    Build the Peppa Pig family tree based on official family tree.

    Official Family Structure (from Peppa Pig wiki):

    Generation 0 (Great-Great-Grandparents):
    - Great Aunt Pig's parents (for depth requirement)

    Generation 1 (Great-Aunt level):
    - Great Aunt Pig (Granny Pig's aunt - shown in old grey photo)

    Generation 2 (Grandparents):
    - Grandpa Pig + Granny Pig (married)

    Generation 3 (Parents):
    - Uncle Pig + Aunty Pig (Uncle is Mummy's brother, Aunty married in)
    - Daddy Pig + Mummy Pig (Daddy married in, Mummy is Granny's daughter)
    - Dottie Pig (Mummy's sister, no partner)

    Generation 4 (Children):
    - Chloé Pig, Alexander Pig (Uncle & Aunty's children)
    - Peppa Pig, George Pig, Evie Pig (Daddy & Mummy's children)
    """
    tree = FamilyTree()

    # =========================================================================
    # Create all family members (Nodes)
    # =========================================================================

    # Generation 0: Great-Great-Grandparents (for depth >= 4)
    great_great_grandpa = Node("Great Great Grandpa Pig")
    great_great_grandma = Node("Great Great Grandma Pig")

    # Generation 1: Great Aunt level
    great_aunt_pig = Node("Great Aunt Pig")  # Granny's aunt (old grey photo)
    great_grandpa_pig = Node("Great Grandpa Pig")  # Granny's father

    # Generation 2: Grandparents
    granny_pig = Node("Granny Pig")
    grandpa_pig = Node("Grandpa Pig")

    # Generation 3: Parents (all on same level)
    mummy_pig = Node("Mummy Pig")       # Granny & Grandpa's daughter
    uncle_pig = Node("Uncle Pig")        # Granny & Grandpa's son (Mummy's brother)
    dottie_pig = Node("Dottie Pig")      # Granny & Grandpa's daughter (Mummy's sister)
    daddy_pig = Node("Daddy Pig")        # Married into family
    aunty_pig = Node("Aunty Pig")        # Married into family (Uncle's wife)

    # Generation 4: Children
    peppa = Node("Peppa Pig")
    george = Node("George Pig")
    evie = Node("Evie Pig")
    chloe = Node("Chloé Pig")
    alexander = Node("Alexander Pig")

    # Set root to oldest ancestor
    tree.root = great_great_grandpa
    tree.members[great_great_grandpa.name] = great_great_grandpa

    # =========================================================================
    # Build relationships using the implemented functions
    # =========================================================================

    # --- Generation 0: Great-Great-Grandparents ---
    tree.addPartner(great_great_grandpa, great_great_grandma)

    # --- Generation 0 -> 1: Great-Great-Grandparents to Great-Grandparents ---
    tree.addChild(great_great_grandpa, great_aunt_pig)
    tree.addChild(great_great_grandma, great_aunt_pig)
    tree.addChild(great_great_grandpa, great_grandpa_pig)
    tree.addChild(great_great_grandma, great_grandpa_pig)
    tree.addSibling(great_aunt_pig, great_grandpa_pig)

    # --- Generation 1 -> 2: Great Grandpa to Granny ---
    tree.addChild(great_grandpa_pig, granny_pig)

    # --- Generation 2: Grandparents partnership ---
    tree.addPartner(granny_pig, grandpa_pig)

    # --- Generation 2 -> 3: Grandparents to Parents ---
    # Mummy Pig (daughter of Granny & Grandpa)
    tree.addChild(granny_pig, mummy_pig)
    tree.addChild(grandpa_pig, mummy_pig)

    # Uncle Pig (son of Granny & Grandpa - Mummy's BROTHER)
    tree.addChild(granny_pig, uncle_pig)
    tree.addChild(grandpa_pig, uncle_pig)

    # Dottie Pig (daughter of Granny & Grandpa - Mummy's sister)
    tree.addChild(granny_pig, dottie_pig)
    tree.addChild(grandpa_pig, dottie_pig)

    # Set siblings
    tree.addSibling(mummy_pig, uncle_pig)
    tree.addSibling(mummy_pig, dottie_pig)
    tree.addSibling(uncle_pig, dottie_pig)

    # --- Generation 3: Parents partnerships ---
    tree.addPartner(mummy_pig, daddy_pig)   # Daddy married in
    tree.addPartner(uncle_pig, aunty_pig)   # Aunty married in

    # --- Generation 3 -> 4: Parents to Children ---
    # Peppa, George, Evie (children of Mummy & Daddy)
    tree.addChild(mummy_pig, peppa)
    tree.addChild(daddy_pig, peppa)
    tree.addChild(mummy_pig, george)
    tree.addChild(daddy_pig, george)
    tree.addChild(mummy_pig, evie)
    tree.addChild(daddy_pig, evie)
    tree.addSibling(peppa, george)
    tree.addSibling(peppa, evie)
    tree.addSibling(george, evie)

    # Chloé, Alexander (children of Uncle & Aunty)
    tree.addChild(uncle_pig, chloe)
    tree.addChild(aunty_pig, chloe)
    tree.addChild(uncle_pig, alexander)
    tree.addChild(aunty_pig, alexander)
    tree.addSibling(chloe, alexander)

    return tree


# =============================================================================
# Main - Demo
# =============================================================================
if __name__ == "__main__":
    # Build the Peppa Pig family tree
    family_tree = build_peppa_pig_family_tree()

    print("=" * 60)
    print("PEPPA PIG FAMILY TREE")
    print("=" * 60)

    # Print tree structure
    print("\nFamily Tree Structure:")
    print("-" * 40)
    family_tree.print_tree()

    # Print statistics
    print("\n" + "-" * 40)
    print(f"Tree Depth: {family_tree.get_depth()}")
    print(f"Tree Width (total members): {family_tree.get_width()}")

    # Demo: Access specific family members
    print("\n" + "-" * 40)
    print("Demo - Peppa's Family:")
    peppa = family_tree.get_member("Peppa Pig")
    if peppa:
        print(f"  Parents: {[p.name for p in peppa.parents]}")
        print(f"  Siblings: {[s.name for s in peppa.siblings]}")
        print(f"  Grandparents (Mummy's side): {[p.name for p in peppa.parents[0].parents]}")
