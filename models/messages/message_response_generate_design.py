from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass
@dataclass_json
class MessageResponseGenerateDesign:
    design_id: int = 0
    design_uuid: str = ''
    qr_code_img: str = ''
    shirt_img: str = ''
    elevation_map_img: str = ''
    lines_design_img: str = ''
    edition_title: str = ''
    edition_desc: str = ''
    is_success: bool = False
    error_code: int = 0
    error_desc: str = ''
