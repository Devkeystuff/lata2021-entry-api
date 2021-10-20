from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass
@dataclass_json
class MessageRequestGenerateDesign:
    api_key: str = ''
    title: str = ''
    description: str = ''
    design_uuid: str = ''
    qr_img_file_name: str = ''
    height_map_img_file_name: str = ''
