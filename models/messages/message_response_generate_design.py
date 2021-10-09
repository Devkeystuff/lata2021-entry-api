from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass
@dataclass_json
class MessageResponseGenerateDesign:
  design_id: int = 0
  is_success: bool = False
  error_code: int = 0
  error_desc: str = ''