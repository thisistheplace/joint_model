from pydantic import BaseModel, ValidationError
import json
from typing import Any


def validate_and_convert_json(input: Any, check_type: BaseModel) -> Any:
    """Validates input and attempts to convert to check_type

    Args:
        input: input to validate
        check_type: type to validate against

    Returns:
        check_type object instantiated with input

    Raise:
        pydantic.ValidationError: if input is invalid
        TypeError: if check_type does not inherit from BaseModel
    """
    if not issubclass(check_type, BaseModel):
        raise TypeError(
            f"check_type of type: {type(check_type)}, must inherit from pydantic.BaseModel"
        )

    if type(input) is str:
        json_data = json.loads(input)
    else:
        json_data = input

    try:
        check_type.validate(json_data)
    except TypeError:
        raise ValidationError(
            f"Input type {type(input)} could not be validated against {type(check_type)}",
            check_type,
        )

    return check_type.parse_obj(json_data)
