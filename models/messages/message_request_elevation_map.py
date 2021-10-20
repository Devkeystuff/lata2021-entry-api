from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass
@dataclass_json
class MessageRequestElevationMap:
    api_key: str = ''
    south: float = .0
    north: float = .0
    west: float = .0
    east: float = .0
