from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass
@dataclass_json
class MessageResponseGenerateDesign:
    design_id: int = 0
    design_uuid: str = ''
    elevation_map_img: str = ''
    normal_map_img: str = ''
    design_img: str = ''
    is_success: bool = False
    error_code: int = 0
    error_desc: str = ''
