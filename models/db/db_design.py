from dataclasses import dataclass
from dataclasses_json import dataclass_json
import time


@dataclass
@dataclass_json
class DbDesign:
  design_id: int = 0
  design_uuid: str = ''
  qr_img_file_name: str = ''
  world_img_file_name: str = ''
  is_deleted: bool = False
  created: float = time.time()
  modified: float = time.time()