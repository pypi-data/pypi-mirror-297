import uuid
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class Page(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    original_document_uuid: str
    original_page_number: int
    document: Optional[Any] = None
    page_number: Optional[int] = None
    detected_template: Optional[str] = None
    mapped_template: Optional[str] = None
    dependency_modified: bool = False
    annotation: Optional[str] = None
    page_description: Optional[str] = None
    annotation_confidence: float = 0.90
    width: int = 0
    height: int = 0
    textract_response: Optional[Any] = None
    extracted_data: Optional[Any] = None
    archived_annotation: Optional[Any] = None
    classification_key: Optional[str] = None
    using_page_service: bool = False
    s3_uris: Optional[Dict[str, Any]] = None
    image: Optional[bytes] = None
