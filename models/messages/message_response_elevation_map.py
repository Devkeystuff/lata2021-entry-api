from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass
@dataclass_json
class MessageResponseElevationMap:
    elevation_map_file: str = ''
    normal_map_file: str = ''
