from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass
@dataclass_json
class MessageRequestGenerateDesign:
    api_key: str = ''
    is_preview: bool = False
    title: str = ''
    description: str = ''
    design_uuid: str = ''
    qr_code_img: str = ''
    elevation_map_img: str = ''
    shirt_img: str = ''
    edition_title: str = ''
    edition_desc: str = ''
    west: float = .0
    north: float = .0
    east: float = .0
    south: float = .0
