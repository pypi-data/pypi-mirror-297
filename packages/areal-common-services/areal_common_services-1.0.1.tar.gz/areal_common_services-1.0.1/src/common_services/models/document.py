from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ExtractedData(BaseModel):
    approved_value: str
    grouped_data: List[Any]
    page: int
    uuid: str
    processed_value: str
    confidence_rate: float
    height_percent: float
    width_percent: float
    x_percent: float
    y_percent: float


class ComponentResultExtractedData(BaseModel):
    approved_value: str
    confidence_rate: float
    from_page_number: int
    height_percent: float
    name: str
    processed_value: str
    uuid: str
    width_percent: float
    x_percent: float
    y_percent: float
    component: Dict[str, str]
    grouped_data: List[Any]


class ComponentResult(BaseModel):
    accepts_multiple: bool
    category: str
    name: str
    uuid: str
    arla_id: Optional[str]
    extracted_data: List[ComponentResultExtractedData]


class Document(BaseModel):
    approved_at: Optional[str]
    auto_pushed_at: Optional[str]
    created_at: str
    download_urls: Dict[str, str]
    duplicate_ref: Optional[str]
    mlops_pushed_at: Optional[str]
    name: str
    notes: Optional[str]
    original_document_uuid: str
    original_page_numbers: List[int]
    page_count: int
    pushed_at: Optional[str]
    resource_uri: str
    rui: Optional[str]
    state: str
    status: str
    template: Dict[str, Any]
    updated_at: str
    upload_session: Dict[str, Any]
    user_extracted_data: Optional[str]
    uuid: str

    component_results: List[ComponentResult]
    extracted_data: List[ExtractedData]
    pages: List[Any]  # TODO: This is pickled
