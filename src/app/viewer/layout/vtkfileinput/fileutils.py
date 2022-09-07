import base64

from ....interfaces import Model
from ....interfaces.validation import validate_and_convert_json


def parse_contents(contents: str, filename: str) -> Model:
    _, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    if "json" in filename.lower():
        return validate_and_convert_json(decoded.decode("utf-8"), Model)
    else:
        raise TypeError("Only .json file extensions are supported!")
