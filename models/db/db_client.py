import time
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class DbClient:
    client_id: int = 0
    api_key: str = ''
    name: str = ''
    is_deleted: bool = False
    created: float = time.time()
    modified: float = time.time()
