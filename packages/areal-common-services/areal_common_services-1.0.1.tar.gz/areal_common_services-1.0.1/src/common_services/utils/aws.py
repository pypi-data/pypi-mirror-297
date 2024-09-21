import boto3
import boto3.session

from common_services.settings import settings

aws_session = boto3.session.Session(
    aws_access_key_id=settings.aws.access_key_id,
    aws_secret_access_key=settings.aws.secret_access_key,
    region_name="us-west-1",
)
