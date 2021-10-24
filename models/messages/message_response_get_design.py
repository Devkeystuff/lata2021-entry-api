from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass
@dataclass_json
class MessageResponseGetDesign:
    design_id: int = 0
    design_uuid: str = ''
    title: str = ''
    description: str = ''
    qr_code_img: str = ''
    elevation_map_img: str = ''
    lines_design_img: str = ''
    normal_map_img: str = ''
    is_success: bool = False
    edition_title: str = ''
    edition_desc: str = ''
    error_code: int = 0
    error_desc: str = ''
