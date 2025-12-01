"""Tests for stop_parser."""

from cs110 import expect, summarize
from stop_parser import *


# Instantiate Latitude
latitude = Latitude(49.2827)  # Example latitude for a stop (in Vancouver)

# Instantiate Longitude
longitude = Longitude(-123.1207)  # Example longitude for a stop (in Vancouver)

# Instantiate URL
url = URL("https://www.example.com")  # Valid URL for the stop

# Instantiate LocationType
location_type = LocationType.STATION  # Location is a station

# Instantiate WheelChairBoarding
wheelchair_boarding = WheelChairBoarding.ACCESSIBLE  # Wheelchair accessible

# Example instantiation of the StopTyped dataclass
stop_typed = StopTyped(
    stop_id="1",                             # Unique ID for the stop
    stop_code="123",                         # Stop code
    stop_name="Main Street Station",         # Stop name
    stop_desc="This is a description of the stop.",  # Stop description
    stop_lat=latitude,                       # Latitude instance
    stop_lon=longitude,                      # Longitude instance
    zone_id="Zone 1",                        # Zone ID
    stop_url=url,                            # Valid URL instance
    location_type=location_type,             # Location type enum
    parent_station="2",                      # Parent station's ID
    wheelchair_boarding=wheelchair_boarding  # Wheelchair accessibility enum
)

# Output some of the fields to demonstrate usage
print(f"Stop ID: {stop_typed.stop_id}")
print(f"Stop Name: {stop_typed.stop_name}")
print(f"Location Type: {stop_typed.location_type.name}")
print(f"Wheelchair Boarding: {stop_typed.wheelchair_boarding.name}")
print(f"Stop Latitude: {stop_typed.stop_lat.lat}")
print(f"Stop Longitude: {stop_typed.stop_lon.lon}")

# Test for parse_latitude
expect(parse_latitude("49.286458"), Latitude(49.286458))

# Test for parse_longitude
expect(parse_longitude("-123.140424"), Longitude(-123.140424))

# Test for parse_url with a valid URL
expect(parse_url("https://www.example.com"), URL("https://www.example.com"))

# Test for parse_url with an empty string (should return None)
expect(parse_url(""), None)

# Test for parse_location_type
expect(parse_location_type("0"), LocationType.STOP)

# Test for parse_wheelchair_boarding
expect(parse_wheelchair_boarding("1"), WheelChairBoarding.ACCESSIBLE)

# Test for parse_row_to_stop
row = "1,50001,Westbound Davie St @ Bidwell St,,49.286458,-123.140424,BUS ZN,,0,,1"
expected_stop = StopTyped(
    stop_id="1",
    stop_code="50001",
    stop_name="Westbound Davie St @ Bidwell St",
    stop_desc=None,
    stop_lat=Latitude(49.286458),
    stop_lon=Longitude(-123.140424),
    zone_id="BUS ZN",
    stop_url=None,
    location_type=LocationType.STOP,
    parent_station="",
    wheelchair_boarding=WheelChairBoarding.ACCESSIBLE
)
expect(parse_row_to_stop(row), expected_stop)

# Test for parse_stops with multiple rows
rows = [
    "1,50001,Westbound Davie St @ Bidwell St,,49.286458,-123.140424,BUS ZN,,0,,1",
    "10000,59326,Northbound No. 5 Rd @ McNeely Dr,,49.179962,-123.09149,BUS ZN,,0,,1"
]
expected_stops = [
    StopTyped(
        stop_id="1",
        stop_code="50001",
        stop_name="Westbound Davie St @ Bidwell St",
        stop_desc=None,
        stop_lat=Latitude(49.286458),
        stop_lon=Longitude(-123.140424),
        zone_id="BUS ZN",
        stop_url=None,
        location_type=LocationType.STOP,
        parent_station="",
        wheelchair_boarding=WheelChairBoarding.ACCESSIBLE
    ),
    StopTyped(
        stop_id="10000",
        stop_code="59326",
        stop_name="Northbound No. 5 Rd @ McNeely Dr",
        stop_desc=None,
        stop_lat=Latitude(49.179962),
        stop_lon=Longitude(-123.09149),
        zone_id="BUS ZN",
        stop_url=None,
        location_type=LocationType.STOP,
        parent_station="",
        wheelchair_boarding=WheelChairBoarding.ACCESSIBLE
    )
]
expect(parse_stops(rows), expected_stops)

summarize()