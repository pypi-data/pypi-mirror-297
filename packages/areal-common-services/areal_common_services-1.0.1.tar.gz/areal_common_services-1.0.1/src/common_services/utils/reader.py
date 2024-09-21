from typing import Any, Optional, Type, TypeVar, Union

from pydantic import BaseModel

from common_services.utils.local import read_json_from_local
from common_services.utils.s3 import read_json_from_s3

T = TypeVar("T", bound=BaseModel)


def read_from(
    filepath_or_objectkey: str,
    where: str = "local",
    json_model: Optional[Type[T]] = None,
) -> Union[T, Any, None]:
    try:
        if where not in ["local", "s3"]:
            raise ValueError(f"Invalid value for 'where': {where}")
        if where == "local":
            return read_json_from_local(
                file_path=filepath_or_objectkey, json_model=json_model
            )

        return read_json_from_s3(
            object_key=filepath_or_objectkey, json_model=json_model
        )
    except ValueError:
        return None
    except Exception:
        return None
