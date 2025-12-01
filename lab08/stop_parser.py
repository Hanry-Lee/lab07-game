"""Parses stops.txt from GTFS."""
import re
import uuid
from enum import Enum
from typing import List
from dataclasses import dataclass


@dataclass
class Stop:
    stop_id: str             # Unique ID of the stop
    stop_code: str           # Code identifier for the stop
    stop_name: str           # Name of the stop
    stop_desc: str           # Description of the stop
    stop_lat: float          # Latitude of the stop (valid range: -90 to 90)
    stop_lon: float          # Longitude of the stop (valid range: -180 to 180)
    zone_id: str             # Zone ID associated with the stop
    stop_url: str            # Valid URL pointing to stop information
    location_type: int       # Type of location (0: Stop, 1: Station, etc.)
    parent_station: int      # ID of the parent station, if applicable
    wheelchair_boarding: int # Wheelchair accessibility (0: unknown, 1: accessible, 2: not accessible)



@dataclass
class Range:
    """Class to validate if a given value is within a specified range."""
    def validate(self, value:     float | int,
                       min_value: float | int,
                       max_value: float | int) -> float | int | None:
        """
        Purpose: Validates if the value is within the specified min and max range.
        Example:
            validate(10,0,10) -> True
            validate(10,0, 9) -> False
        """
        if not (min_value <= value <= max_value):
            raise ValueError(
                f"Value {value} is out of range [{min_value}, {max_value}]"
            )
        return value


@dataclass
class Latitude(Range):
    """Class to validate the latitude value."""
    def __init__(self, lat: float) -> None:
        self.lat = self.validate(lat, -90.0, 90.0)  # Latitude must be in the range [-90, 90]


@dataclass
class Longitude(Range):
    """Class to validate the longitude value."""
    def __init__(self, lon: float) -> None:
        self.lon = self.validate(lon, -180.0, 180.0)  # Longitude must be in the range [-180, 180]
        

@dataclass
class LocationType(Enum):
    """Enum to define different location types for a stop."""
    STOP = 0       # Standard stop
    STATION = 1    # Station
    ENTRANCE = 2   # Entrance/exit
    GENERIC = 3    # Generic node
    BOARDING = 4   # Boarding area


@dataclass
class WheelChairBoarding(Enum):
    INHERIT = 0        # Parentless means none, otherwise inherit
    ACCESSIBLE = 1     # Some accessible path or vehicles
    INACCESSIBLE = 2   # No accessible paths or vehicles


@dataclass
class URL:
    """Class to validate and store a URL."""
    def __init__(self, url: str) -> None:
        """Initialize the URL after validating it."""
        if self.validate(url):
            self.url = url
            
    def validate(self, url: str) -> bool:
        """
        Purpose: Validates if the given string is a valid URL.
        Example:
            validate("https://hello.com") -> True
            validate("hts://hello.com") -> False
        """
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # Protocol (http, https, ftp)
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # Domain name
            r'localhost|'  # Localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # IPv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # IPv6
            r'(?::\d+)?'  # Optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
        return re.match(regex, url) is not None  # Returns True if the URL is valid, otherwise False


@dataclass
class StopTyped:
    stop_id: str 
    stop_code: str
    stop_name: str
    stop_desc: str | None
    stop_lat: Latitude
    stop_lon: Longitude
    zone_id: str
    stop_url: URL | None
    location_type: LocationType
    parent_station: str # Foreign
    wheelchair_boarding: WheelChairBoarding
    
    def __str__(self) -> str:
        """
        Purpose: Pretty-print the StopTyped instance in a readable format.
        
        Example:
            Stop Name: Westbound Davie St @ Bidwell St
            Stop Code: 50001
            Latitude: 49.286458, Longitude: -123.140424
            Zone ID: BUS ZN
            Location Type: STOP
            Wheelchair Boarding: ACCESSIBLE
        """
        return (f"Stop Name: {self.stop_name}\n"
                f"Stop Code: {self.stop_code}\n"
                f"Stop Description: {self.stop_desc or 'N/A'}\n"
                f"Latitude: {self.stop_lat.lat}, Longitude: {self.stop_lon.lon}\n"
                f"Zone ID: {self.zone_id}\n"
                f"URL: {self.stop_url.url if self.stop_url else 'N/A'}\n"
                f"Location Type: {self.location_type.name}\n"
                f"Wheelchair Boarding: {self.wheelchair_boarding.name}\n")


# Helper function to parse latitude
def parse_latitude(value: str) -> Latitude:
    """
    Purpose: Convert a string to a validated Latitude instance.
    Example:
        parse_latitude("49.286458") -> Latitude(49.286458)
    """
    return Latitude(float(value))

# Helper function to parse longitude
def parse_longitude(value: str) -> Longitude:
    """
    Purpose: Convert a string to a validated Longitude instance.
    Example:
        parse_longitude("-123.140424") -> Longitude(-123.140424)
    """
    return Longitude(float(value))

# Helper function to parse the URL
def parse_url(value: str) -> URL | None:
    """
    Purpose: Convert a string to a validated URL
    instance if not empty, or None if empty.
    Examples:
        parse_url("https://www.example.com") -> URL("https://www.example.com")
        parse_url("") -> None
    """
    return URL(value) if value else None

# Helper function to parse LocationType
def parse_location_type(value: str) -> LocationType:
    """
    Purpose: Convert a string to a LocationType enum.
    Example:
        parse_location_type("0") -> LocationType.STOP
    """
    return LocationType(int(value))

# Helper function to parse WheelChairBoarding
def parse_wheelchair_boarding(value: str) -> WheelChairBoarding:
    """
    Purpose: Convert a string to a WheelChairBoarding enum.
    Example:
        parse_wheelchair_boarding("1") -> WheelChairBoarding.ACCESSIBLE
    """
    return WheelChairBoarding(int(value))

# Helper function to parse a row into StopTyped
def parse_row_to_stop(row: str) -> StopTyped:
    """
    Purpose: Convert a comma-separated string row into a StopTyped instance.
    Example:
        parse_row_to_stop("1,50001,Westbound Davie St @ Bidwell St,,49.286458,-123.140424,BUS ZN,,0,,1") 
            -> StopTyped(stop_id="1", stop_code="50001", stop_name="Westbound Davie St @ Bidwell St", ...)
    """
    columns = row.split(',')

    # Manually parsing each field
    stop_id = columns[0]
    stop_code = columns[1]
    stop_name = columns[2]
    stop_desc = columns[3] if columns[3] else None
    stop_lat = parse_latitude(columns[4])  # Use helper to parse latitude
    stop_lon = parse_longitude(columns[5])  # Use helper to parse longitude
    zone_id = columns[6]
    stop_url = parse_url(columns[7])  # Use helper to parse URL
    location_type = parse_location_type(columns[8])  # Use helper to parse location type
    parent_station = columns[9]  # Generating new UniqueID for parent station
    wheelchair_boarding = parse_wheelchair_boarding(columns[10])  # Use helper to parse wheelchair boarding

    # Return a StopTyped instance
    return StopTyped(
        stop_id=stop_id,
        stop_code=stop_code,
        stop_name=stop_name,
        stop_desc=stop_desc,
        stop_lat=stop_lat,
        stop_lon=stop_lon,
        zone_id=zone_id,
        stop_url=stop_url,
        location_type=location_type,
        parent_station=parent_station,
        wheelchair_boarding=wheelchair_boarding
    )

# Helper function to parse all rows
def parse_stops(rows: List[str]) -> List[StopTyped]:
    """
    Purpose: Parse multiple rows of stop data into a list of StopTyped instances.
    Example:
        parse_stops([
            "1,50001,Westbound Davie St @ Bidwell St,,49.286458,-123.140424,BUS ZN,,0,,1",
            "10000,59326,Northbound No. 5 Rd @ McNeely Dr,,49.179962,-123.09149,BUS ZN,,0,,1"
        ]) -> [StopTyped(...), StopTyped(...)]
    """
    return [parse_row_to_stop(row) for row in rows]


def query_stops(stops: list[StopTyped], **filters) -> list[StopTyped]:
    """
    Purpose: Query the list of stops based on filters such as stop_name, stop_code, zone_id, etc.
    Example:
        query_stops(stops, stop_name="Westbound Davie St @ Bidwell St") -> list of matching StopTyped instances
    Args:
        stops: List of StopTyped instances.
        **filters: Keyword arguments for filtering the stops (e.g., stop_name="Westbound Davie St @ Bidwell St").
    Returns:
        List of StopTyped instances that match all the provided filters.
    """
    results = stops

    for attr, value in filters.items():
        results = [stop for stop in results if getattr(stop, attr) == value]
    
    return results


with open("stops.txt", 'r') as file:
    lines = file.readlines()
    stops = parse_stops(lines[1:])
    print(f"There were {len(stops)} stops.")

    def query(**kwargs):
        """
        Purpose: Convenience function for querying stops.
        Examples:
            query(stop_name="Westbound Davie St @ Bidwell St")
            query(stop_code="50011")
        """
        for s in query_stops(stops, **kwargs):
            print(s)
    
    


