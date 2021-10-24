import time
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class LatLngBounds:
    south: float = .0
    north: float = .0
    west: float = .0
    east: float = .0

