import json
from typing import Any

def validate_json(json_str: str, check_type: Any) -> dict:
    if type(json_str) is str:
        json_data = json.loads(json_str)
    else:
        json_data = json_str
    check_type.validate(json_data)
    return json_data