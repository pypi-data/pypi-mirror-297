from typing import Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class S3(BaseModel):
    bucket_name: str


class SQS(BaseModel):
    read_queue_url: str
    write_queue_url: str


class Lambda(BaseModel):
    sentence_transformer: str


class Aws(BaseModel):
    access_key_id: str
    secret_access_key: str
    region: str = "us-west-1"
    s3: S3
    sqs: SQS
    Lambda: Optional[Lambda]


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    aws: Aws


settings = TestSettings()  # type: ignore[unused-ignore]
