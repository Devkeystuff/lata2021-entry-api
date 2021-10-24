from dataclasses import dataclass
from dataclasses_json import dataclass_json
import time


@dataclass_json
@dataclass
class DbDesign:
    design_id: int = 0
    design_uuid: str = ''
    title: str = ''
    description: str = ''
    qr_code_img: str = ''
    elevation_map_img: str = ''
    lines_design_img: str = ''
    edition_title: str = ''
    edition_desc: str = ''
    is_deleted: bool = False
    created: float = time.time()
    modified: float = time.time()
