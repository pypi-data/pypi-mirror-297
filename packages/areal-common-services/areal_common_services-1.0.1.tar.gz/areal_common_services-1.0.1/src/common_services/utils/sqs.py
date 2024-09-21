import json
from typing import List, Type, TypeVar
from uuid import uuid4

from pydantic import BaseModel, ValidationError

from common_services.settings import settings
from common_services.utils.aws import aws_session

T = TypeVar("T", bound=BaseModel)


def read_messages_from_sqs(
    input_json_model: Type[T],
    sqs=aws_session.client("sqs"),
) -> List[T]:
    """Read messages from an SQS queue and parse them using the Message Pydantic model."""

    validated_messages: List[T] = []
    total_messages = 0
    successful_messages = 0

    try:
        received_messages = sqs.receive_message(
            QueueUrl=settings.aws.sqs.read_queue_url, MaxNumberOfMessages=10
        )
        for message in received_messages["Messages"]:
            try:
                assert "Body" in message
                validated_input = input_json_model.model_validate_json(message["Body"])
                validated_messages.append(validated_input)

                assert "ReceiptHandle" in message
                sqs.delete_message(
                    QueueUrl=settings.aws.sqs.read_queue_url,
                    ReceiptHandle=message["ReceiptHandle"],
                )
                successful_messages += 1

            except (json.JSONDecodeError, ValidationError) as e:
                raise ValueError(f"Error reading JSON from SQS: {e}")
            except Exception:
                raise Exception("Unexpected error reading JSON from SQS")

    except Exception:
        raise Exception("Unexpected error in SQS read operation")

    success_rate = (
        (successful_messages / total_messages * 100) if total_messages > 0 else 0
    )
    return validated_messages


def write_message_to_sqs(
    message: BaseModel,
    sqs=aws_session.client("sqs"),
) -> None:
    """Write a message to SQS"""

    try:
        message_body = message.model_dump_json(exclude_none=True)
        message_group_id = str(uuid4())

        sqs.send_message(
            QueueUrl=settings.aws.sqs.write_queue_url,
            MessageBody=message_body,
            DelaySeconds=0,
            MessageGroupId=message_group_id,
        )

    except (json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"Error writing JSON to SQS: {e}")
    except Exception:
        raise Exception("Unexpected error in SQS write operation")
