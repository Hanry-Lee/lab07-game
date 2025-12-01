"""Parses routes.txt from GTFS."""
import re
from enum import Enum
from typing import List
from dataclasses import dataclass

# Import reusable components from stop_parser
from stop_parser import URL


@dataclass
class Route:
    """Raw data model for a route from routes.txt."""
    route_id: str            # Unique ID of the route
    agency_id: str           # Agency ID (foreign key)
    route_short_name: str    # Short name/number of the route
    route_long_name: str     # Full descriptive name of the route
    route_desc: str          # Description of the route
    route_type: int          # Type of transportation (0-12)
    route_url: str           # URL with route information
    route_color: str         # Color for route display (hex)
    route_text_color: str    # Text color for route display (hex)


@dataclass
class RouteType(Enum):
    """Enum to define different transportation types for a route."""
    TRAM = 0          # Tram, Streetcar, Light rail
    SUBWAY = 1        # Subway, Metro
    RAIL = 2          # Rail (intercity or long-distance)
    BUS = 3           # Bus
    FERRY = 4         # Ferry
    CABLE_TRAM = 5    # Cable tram
    AERIAL_LIFT = 6   # Aerial lift, suspended cable car
    FUNICULAR = 7     # Funicular
    TROLLEYBUS = 11   # Trolleybus
    MONORAIL = 12     # Monorail


@dataclass
class Color:
    """Class to validate and store a hex color code."""
    def __init__(self, color: str) -> None:
        """Initialize the Color after validating it."""
        if self.validate(color):
            self.color = color
        else:
            # Default colors as per GTFS spec
            self.color = color if color else None

    def validate(self, color: str) -> bool:
        """
        Purpose: Validates if the given string is a valid 6-character hex color.
        Example:
            validate("FFFFFF") -> True
            validate("FFF") -> False
            validate("GGGGGG") -> False
        """
        if not color:
            return True  # Empty is valid (will use default)
        regex = re.compile(r'^[0-9A-Fa-f]{6}$')
        return re.match(regex, color) is not None


@dataclass
class RouteTyped:
    """Typed data model for a route with validated fields."""
    route_id: str
    agency_id: str
    route_short_name: str
    route_long_name: str
    route_desc: str | None
    route_type: RouteType
    route_url: URL | None
    route_color: Color | None
    route_text_color: Color | None

    def __str__(self) -> str:
        """
        Purpose: Pretty-print the RouteTyped instance in a readable format.

        Example:
            Route ID: 1
            Short Name: 99
            Long Name: Commercial-Broadway/UBC (B-Line)
            Route Type: BUS
            Color: 0000FF
        """
        return (f"Route ID: {self.route_id}\n"
                f"Agency ID: {self.agency_id}\n"
                f"Short Name: {self.route_short_name}\n"
                f"Long Name: {self.route_long_name}\n"
                f"Description: {self.route_desc or 'N/A'}\n"
                f"Route Type: {self.route_type.name}\n"
                f"URL: {self.route_url.url if self.route_url else 'N/A'}\n"
                f"Color: {self.route_color.color if self.route_color else 'FFFFFF'}\n"
                f"Text Color: {self.route_text_color.color if self.route_text_color else '000000'}\n")


# Helper function to parse route type
def parse_route_type(value: str) -> RouteType:
    """
    Purpose: Convert a string to a RouteType enum.
    Example:
        parse_route_type("3") -> RouteType.BUS
        parse_route_type("0") -> RouteType.TRAM
    """
    return RouteType(int(value))


# Helper function to parse URL (reusing from stop_parser)
def parse_url(value: str) -> URL | None:
    """
    Purpose: Convert a string to a validated URL instance if not empty, or None if empty.
    Examples:
        parse_url("https://www.example.com") -> URL("https://www.example.com")
        parse_url("") -> None
    """
    return URL(value) if value else None


# Helper function to parse color
def parse_color(value: str) -> Color | None:
    """
    Purpose: Convert a string to a validated Color instance if not empty, or None if empty.
    Examples:
        parse_color("FFFFFF") -> Color("FFFFFF")
        parse_color("") -> None
    """
    return Color(value) if value else None


# Helper function to parse a row into RouteTyped
def parse_row_to_route(row: str) -> RouteTyped:
    """
    Purpose: Convert a comma-separated string row into a RouteTyped instance.
    Example:
        parse_row_to_route("1,agency1,99,Commercial-Broadway/UBC,,3,,,0000FF,FFFFFF")
            -> RouteTyped(route_id="1", route_short_name="99", ...)
    """
    columns = row.strip().split(',')

    # Manually parsing each field
    route_id = columns[0]
    agency_id = columns[1]
    route_short_name = columns[2]
    route_long_name = columns[3]
    route_desc = columns[4] if columns[4] else None
    route_type = parse_route_type(columns[5])
    route_url = parse_url(columns[6])
    route_color = parse_color(columns[7])
    route_text_color = parse_color(columns[8])

    # Return a RouteTyped instance
    return RouteTyped(
        route_id=route_id,
        agency_id=agency_id,
        route_short_name=route_short_name,
        route_long_name=route_long_name,
        route_desc=route_desc,
        route_type=route_type,
        route_url=route_url,
        route_color=route_color,
        route_text_color=route_text_color
    )


# Helper function to parse all rows
def parse_routes(rows: List[str]) -> List[RouteTyped]:
    """
    Purpose: Parse multiple rows of route data into a list of RouteTyped instances.
    Example:
        parse_routes([
            "1,agency1,99,Commercial-Broadway/UBC,,3,,,0000FF,FFFFFF",
            "2,agency1,44,UBC/Downtown,,3,,,FF0000,FFFFFF"
        ]) -> [RouteTyped(...), RouteTyped(...)]
    """
    return [parse_row_to_route(row) for row in rows]


def query_routes(routes: list[RouteTyped], **filters) -> list[RouteTyped]:
    """
    Purpose: Query the list of routes based on filters such as route_short_name, route_type, etc.
    Example:
        query_routes(routes, route_short_name="99") -> list of matching RouteTyped instances
    Args:
        routes: List of RouteTyped instances.
        **filters: Keyword arguments for filtering the routes.
    Returns:
        List of RouteTyped instances that match all the provided filters.
    """
    results = routes

    for attr, value in filters.items():
        results = [route for route in results if getattr(route, attr) == value]

    return results


# Main execution - will need routes.txt file to run
if __name__ == "__main__":
    try:
        with open("routes.txt", 'r') as file:
            lines = file.readlines()
            routes = parse_routes(lines[1:])  # Skip header
            print(f"There were {len(routes)} routes.")

            def query(**kwargs):
                """
                Purpose: Convenience function for querying routes.
                Examples:
                    query(route_short_name="99")
                    query(route_type=RouteType.BUS)
                """
                for r in query_routes(routes, **kwargs):
                    print(r)
    except FileNotFoundError:
        print("routes.txt not found. Please provide a routes.txt file to parse.")
