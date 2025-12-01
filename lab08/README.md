# Lab 08: File I/O

## Individual Component

Created `routes_parser.py` following the pattern from `stop_parser.py`:

- `Route` dataclass: Raw data model mirroring CSV columns
- `RouteType` enum: TRAM, SUBWAY, RAIL, BUS, FERRY, CABLE_TRAM, AERIAL_LIFT, FUNICULAR, TROLLEYBUS, MONORAIL
- `Color` class: Validates 6-character hex color codes
- `RouteTyped` dataclass: Typed model with validated fields
- Helper functions: `parse_route_type`, `parse_url`, `parse_color`
- `parse_row_to_route`: Converts CSV row to RouteTyped
- `parse_routes`: Parses multiple rows
- `query_routes`: Filters routes by attributes

Test suite in `routes_parser_tests.py` (21 tests, all passing).

## Group Component

Designed and implemented game state management for a game project:

### Specification
- `game_state_spec.md`: Defines player.csv and food.csv formats with field types

### Parsers
- `player_parser.py`: Parses player data (position, size, speed, color, count)
- `food_parser.py`: Parses food data (position, size)
- `game_state_csv.py`: Manages loading/saving game state

### Validation Types
- `ScreenX`, `ScreenY`: Screen coordinate validation (1280x720)
- `PositiveInt`, `PositiveFloat`: Non-negative number validation
- `Color`: Color name validation

### Tests
- `player_parser_tests.py`: 21 tests, all passing
- `food_parser_tests.py`: 10 tests, all passing

## Files

| File | Purpose |
|------|---------|
| routes_parser.py | GTFS routes parser |
| routes_parser_tests.py | Routes parser tests |
| player_parser.py | Game player parser |
| player_parser_tests.py | Player parser tests |
| food_parser.py | Game food parser |
| food_parser_tests.py | Food parser tests |
| game_state_csv.py | Game state manager |
| game_state_spec.md | Game state specification |
| stop_parser.py | Provided GTFS stops parser |
| stop_parser_tests.py | Provided stops parser tests |
| stops.txt | Sample GTFS data |
| uml.png | UML diagram |
| contributions.txt | References |
