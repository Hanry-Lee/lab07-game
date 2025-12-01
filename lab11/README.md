# W11 Lab: Graphs

## What I Did

For this lab I implemented two tree structures:
1. **FamilyTree** (Individual lab)
2. **BST** (Group lab)

I did the group lab by myself and chose Option 1 (sortable class + BST).

---

## Individual Lab - FamilyTree

I used **Peppa Pig's Family Tree** from https://peppapig.fandom.com/wiki/Pig_Family

### Functions (with HTDF):
- `addParent(child, parent)`
- `addChild(parent, child)`
- `addPartner(person1, person2)`
- `addSibling(child, sibling)`

### Tree stats:
- Depth: 5 (needed >= 4)
- Width: 16 members (needed >= 10)

---

## Group Lab - BST

I used the `Shape` class from **lab09 group project** and made it sortable by `dist_traveled`. Then built a BST with it.

### BST methods:
- **Setters:** `add()`
- **Getters:** `contains()`, `get_min()`, `get_max()`, `get_size()`
- **Deleters:** `delete()`, `clear()`
- **Traversal:** `inorder()`

---

## Files

| File | Description |
|------|-------------|
| `family_tree.py` | FamilyTree implementation |
| `shape_bst.py` | BST with Shape class (from lab09) |

## How to Run

```
python family_tree.py
python shape_bst.py
```
