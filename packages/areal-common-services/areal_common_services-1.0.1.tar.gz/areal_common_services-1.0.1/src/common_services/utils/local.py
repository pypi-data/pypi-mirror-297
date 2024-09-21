import json
from typing import Any, Optional, Type, TypeVar, Union

from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


def read_json_from_local(
    file_path: str,
    json_model: Optional[Type[T]] = None,
) -> Union[T, Any, None]:
    """Read JSON from an S3 bucket and optionally parse it using a Pydantic model."""
    try:
        my_file = open(file_path, "r")

        my_json = json.load(my_file)

        if json_model:
            my_json = json_model.model_validate(my_json)

        return my_json

    except (FileNotFoundError, json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"Error reading JSON from local file: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error reading JSON from local file: {e}")
