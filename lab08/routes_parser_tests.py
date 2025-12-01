"""Tests for routes_parser."""

from cs110 import expect, summarize
from routes_parser import *


# Test Color validation
color_valid = Color("FFFFFF")
color_valid_2 = Color("0000FF")
color_empty = Color("")

# Test RouteType enum
route_type_bus = RouteType.BUS
route_type_tram = RouteType.TRAM

# Test URL (imported from stop_parser)
url = URL("https://www.translink.ca")

# Example instantiation of the RouteTyped dataclass
route_typed = RouteTyped(
    route_id="1",
    agency_id="agency1",
    route_short_name="99",
    route_long_name="Commercial-Broadway/UBC (B-Line)",
    route_desc="Rapid transit bus service",
    route_type=RouteType.BUS,
    route_url=url,
    route_color=Color("0000FF"),
    route_text_color=Color("FFFFFF")
)

# Output some of the fields to demonstrate usage
print(f"Route ID: {route_typed.route_id}")
print(f"Short Name: {route_typed.route_short_name}")
print(f"Long Name: {route_typed.route_long_name}")
print(f"Route Type: {route_typed.route_type.name}")
print(f"Color: {route_typed.route_color.color}")
print()

# Test for parse_route_type
expect(parse_route_type("0"), RouteType.TRAM)
expect(parse_route_type("1"), RouteType.SUBWAY)
expect(parse_route_type("2"), RouteType.RAIL)
expect(parse_route_type("3"), RouteType.BUS)
expect(parse_route_type("4"), RouteType.FERRY)
expect(parse_route_type("7"), RouteType.FUNICULAR)

# Test for parse_url with a valid URL
expect(parse_url("https://www.example.com"), URL("https://www.example.com"))

# Test for parse_url with an empty string (should return None)
expect(parse_url(""), None)

# Test for parse_color with a valid color
expect(parse_color("FFFFFF"), Color("FFFFFF"))
expect(parse_color("0000FF"), Color("0000FF"))

# Test for parse_color with an empty string (should return None)
expect(parse_color(""), None)

# Test for Color validation
expect(Color("FFFFFF").validate("FFFFFF"), True)
expect(Color("").validate("GGGGGG"), False)
expect(Color("").validate("FFF"), False)
expect(Color("").validate(""), True)

# Test for parse_row_to_route
row = "1,agency1,99,Commercial-Broadway/UBC,,3,,0000FF,FFFFFF"
expected_route = RouteTyped(
    route_id="1",
    agency_id="agency1",
    route_short_name="99",
    route_long_name="Commercial-Broadway/UBC",
    route_desc=None,
    route_type=RouteType.BUS,
    route_url=None,
    route_color=Color("0000FF"),
    route_text_color=Color("FFFFFF")
)
expect(parse_row_to_route(row), expected_route)

# Test for parse_row_to_route with URL
row_with_url = "2,agency1,44,UBC/Downtown,Express service,3,https://www.translink.ca,FF0000,000000"
expected_route_with_url = RouteTyped(
    route_id="2",
    agency_id="agency1",
    route_short_name="44",
    route_long_name="UBC/Downtown",
    route_desc="Express service",
    route_type=RouteType.BUS,
    route_url=URL("https://www.translink.ca"),
    route_color=Color("FF0000"),
    route_text_color=Color("000000")
)
expect(parse_row_to_route(row_with_url), expected_route_with_url)

# Test for parse_routes with multiple rows
rows = [
    "1,agency1,99,Commercial-Broadway/UBC,,3,,0000FF,FFFFFF",
    "2,agency1,44,UBC/Downtown,,3,,FF0000,000000"
]
expected_routes = [
    RouteTyped(
        route_id="1",
        agency_id="agency1",
        route_short_name="99",
        route_long_name="Commercial-Broadway/UBC",
        route_desc=None,
        route_type=RouteType.BUS,
        route_url=None,
        route_color=Color("0000FF"),
        route_text_color=Color("FFFFFF")
    ),
    RouteTyped(
        route_id="2",
        agency_id="agency1",
        route_short_name="44",
        route_long_name="UBC/Downtown",
        route_desc=None,
        route_type=RouteType.BUS,
        route_url=None,
        route_color=Color("FF0000"),
        route_text_color=Color("000000")
    )
]
expect(parse_routes(rows), expected_routes)

# Test for query_routes
test_routes = parse_routes(rows)
expect(len(query_routes(test_routes, route_short_name="99")), 1)
expect(len(query_routes(test_routes, route_type=RouteType.BUS)), 2)
expect(len(query_routes(test_routes, route_short_name="999")), 0)

summarize()
