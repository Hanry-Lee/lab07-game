# CPSC 110 Lab 7: Group Project - Chase & Collect Game

**I finished this lab/project solely.**

## GitHub Repository

https://github.com/Hanry-Lee/lab07-game/

## Project Overview

A PyGame video game following the How to Design Functions/Worlds/Programs (HtDF/W/P) formula. The player competes against an AI opponent to collect food items.

## Required Files

- character.py
- cs110.py
- food.py
- game.py
- install.py
- keys.py
- opponent.py
- player.py
- README.md
- run.py
- save_state.py
- sprite.py
- tests.py
- uml.png
- group_agreement.md

## Commands

```bash
python install.py     # Install dependencies
python run.py         # Run the game
python tests.py       # Run tests (44 passing)
```

## Game Controls

- **Mouse**: Move player
- **S**: Save game
- **L**: Load game
- **P**: Pause/Resume
- **ESC/Q**: Quit
- **R**: Restart (after game ends)
- **M**: Return to menu (after game ends)

## Architecture

Class hierarchy using inheritance, composition, and aggregation:

```
Sprite (x, y, size)
├── Food
└── Character (speed, color, count)
    ├── Player (human-controlled via mouse)
    └── Opponent (AI-controlled with state search)

FoodList (aggregation of Food items)
Game (composition with pygame.Surface, Clock)
```

## Requirements Checklist

| Requirement | Status |
|-------------|--------|
| Test suites for every non-draw function | 44 tests passing |
| Purpose statements, examples, signatures with typing | Implemented |
| Inheritance (Sprite → Character → Player/Opponent) | Implemented |
| Composition (Game contains Surface, Clock) | Implemented |
| Aggregation (FoodList contains List[Food]) | Implemented |
| Player: Non-trivial control system | Mouse control with eat/resize |
| Opponent: Non-trivial AI system | State search with scoring algorithm |
| Save state: File-based save/load | JSON file storage |
| UML class diagram | uml.png |
| Group agreement | group_agreement.md |

## System Descriptions

### Player System
- Mouse-controlled movement
- Collision detection with food
- Dynamic resizing based on food consumed
- Score tracking

### AI Opponent System
The opponent uses a state search algorithm (`find_best_food`) that scores food items based on:
- Distance to opponent (closer = better)
- Cluster bonus (food near other food = better)
- Player penalty (avoids food closer to player)

### Save State System
- Saves player position, size, count
- Saves opponent position, size, count
- Saves all food positions and sizes
- JSON file format (savegame.json)

## Code Standards

- Every non-draw function has tests
- All functions have: signature with typing, purpose statement, examples
- Shared logic in parent classes to minimize duplication
- HtDF recipe followed throughout
