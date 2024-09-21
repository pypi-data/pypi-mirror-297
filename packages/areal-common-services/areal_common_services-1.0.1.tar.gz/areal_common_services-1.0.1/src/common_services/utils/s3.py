import json
from typing import Any, Optional, Type, TypeVar, Union

from pydantic import BaseModel, ValidationError

from common_services.settings import settings
from common_services.utils.aws import aws_session

T = TypeVar("T", bound=BaseModel)


def read_json_from_s3(
    object_key: str,
    bucket_name: str = settings.aws.s3.bucket_name,
    json_model: Optional[Type[T]] = None,
    s3=aws_session.client("s3"),
) -> Union[T, Any, None]:
    """Read JSON from an S3 bucket and optionally parse it using a Pydantic model."""

    try:
        body = s3.get_object(Bucket=bucket_name, Key=object_key)["Body"].read()

        my_json = json.loads(body)
        if json_model:
            my_json = json_model.model_validate(my_json)

        return my_json

    except (ValidationError, json.JSONDecodeError) as e:
        raise ValueError(f"Error reading JSON from S3: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error reading JSON from S3: {e}")
