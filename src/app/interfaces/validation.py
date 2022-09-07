import json
from typing import Any


def validate_and_convert_json(json_str: str, check_type: Any) -> Any:
    if type(json_str) is str:
        json_data = json.loads(json_str)
    else:
        json_data = json_str
    check_type.validate(json_data)
    return check_type.parse_obj(json_data)
