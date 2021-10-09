from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass
@dataclass_json
class MessageRequestGenerateDesign:
  title: str = ''
  desc: str = ''
  design_uuid: str = ''
  qr_img_file_name: str = ''
  world_img_file_name: str = '' 