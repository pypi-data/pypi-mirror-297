"""
1- Page init
pdf -> sayfa sayfa page description olusturuyor.

page_service page seviyesinde

Question: init servisi her sayfanin init edilmesini bekleyip sonra document classification'mi cagiracak?

document classification
    her sayfa icin
        page classification aldim - verdim
    analiz yapmasi lazim


    {
            "organization_uuid": "uuid",
            "upload_session_name": "name",
            "upload_session_uuid": "uuid",
            "created_at": "2021-11-09T17:57:26.091172",
            "original_document_name": "TitlePackage_Title-Closing-Protection-Letter.pdf",
            "original_document_uuid": "88fa2647-b8ab-4d49-a0a0-b3612c13c524",
            ""
            "results":[
                {
                    "document_name": {},
                    "document_uuid": {},
                    "pages": [
                            {},
                            {},
                            {}
                        ],
                    "component_results": [
                    ],
                    "template_uuid": "4e43f618-c09c-4ebb-bbce-d4666657e34c"
                }
            ]
    }
"""

import uuid


class DocumentRunTime(object):
    def __init__(
        self,
        template_uuid,
        thumbnail_image,
        org_category_id="",
        org_category_name="",
        org_document_name="",
        template_name="",
        page=None,
        given_uuid="",
    ):
        self.uuid = given_uuid if given_uuid else str(uuid.uuid4())
        self.duplicate_ref = ""
        self.template_uuid = template_uuid
        self.template_name = template_name
        self.thumbnail_image = thumbnail_image
        self.org_category_id = org_category_id
        self.org_category_name = org_category_name
        self.org_document_name = org_document_name
        self.original_doc_uuid = page.original_document_uuid if page else None
        self.pages = []
        self.extracted_data = []
        self.add_page(page) if page else None

    def add_page(self, new_page):
        new_page.page_number = len(self.pages)
        self.pages.append(new_page)

    def reset_page_numbering(self):
        different_original_documents = []
        for page in self.pages:
            if page.original_document_uuid not in different_original_documents:
                different_original_documents.append(page.original_document_uuid)
        sorted_pages = []
        for dod in different_original_documents:
            filtered_pages = list(
                filter(lambda x: x.original_document_uuid == dod, self.pages)
            )
            filtered_pages.sort(key=lambda x: x.original_page_number)
            sorted_pages.extend(filtered_pages)
        for i, p in enumerate(sorted_pages):
            p.page_number = i
        self.pages = sorted_pages

    def update_page_templates(self, new_template, update_detected_template=False):
        for p in self.pages:
            p.mapped_template = new_template
            if update_detected_template:
                p.detected_template = new_template

    def get_document_pdf_bytes(self):
        from . import image_editor

        list_of_page_bytes = []
        for page in self.pages:
            list_of_page_bytes.append(page.image)
        document_pdf_bytes = image_editor.images_to_pdf(list_of_page_bytes)
        return document_pdf_bytes

    def to_json(self):
        return {
            "uuid": self.uuid,
            "duplicate_ref": self.duplicate_ref,
            "template_uuid": self.template_uuid,
            "template_name": self.template_name,
            "thumbnail_image": self.thumbnail_image,
            "org_category_id": self.org_category_id,
            "org_category_name": self.org_category_name,
            "org_document_name": self.org_document_name,
            "original_doc_uuid": self.original_doc_uuid,
            "pages": [p.to_json() for p in self.pages],
            "extracted_data": self.extracted_data,
        }


# OMPR = OCR Multi Page Result
class OcrMultiPageResult(DocumentRunTime):
    pass


class PageRunTime(object):
    def __init__(
        self,
        original_document_uuid,
        original_page_number,
        document=None,
        detected_template=None,
        dependency_modified=False,
        image=None,
        annotation=None,
        page_description=None,
        s3_uris=None,
        using_page_service=False,
    ):
        self.uuid = str(uuid.uuid4())
        self.detected_template = detected_template
        self.mapped_template = detected_template
        self.dependency_modified = dependency_modified
        self.original_document_uuid = original_document_uuid
        self.original_page_number = original_page_number
        self.document = document
        self.page_number = None
        self.annotation = annotation
        self.page_description = page_description
        self.annotation_confidence = (
            annotation.pages[0].blocks[0].confidence
            if annotation and hasattr(annotation, "pages") and len(annotation.pages)
            else 0.90
        )
        self.width = (
            annotation.pages[0].width
            if annotation and hasattr(annotation, "pages") and len(annotation.pages)
            else 0
        )
        self.height = (
            annotation.pages[0].height
            if annotation and hasattr(annotation, "pages") and len(annotation.pages)
            else 0
        )
        self.textract_response = None
        self.extracted_data = None
        self.archived_annotation = None  # Remove
        self.classification_key = None
        self.using_page_service = using_page_service
        self.s3_uris = s3_uris
        self._image = image
        # self.rotation = rotation.Enum

    @property
    def image(self):
        # stk = inspect.stack()[1].frame
        # print(f'PRT image {stk}')
        if self._image:
            return self._image
        return self.page_description.image if self.page_description else None

    def get_image_url(self, img_type="pdf", img_ext=None, img_size=None):
        uris = self.s3_uris
        img_dim = ""
        if isinstance(img_size, int):
            try:
                img_dim = "_" + uris.get("image_sizes", [])[img_size][2:]
            except IndexError:
                img_dim = ""

        return (
            (
                uris["doc_path"]
                + "/"
                + img_type
                + "/"
                + uris["doc_name"]
                + "_"
                + str(self.original_page_number)
                + img_dim
                + "."
                + (img_ext or uris["extension"])
            )
            if uris
            else ""
        )

    def to_json(self):
        return {
            "uuid": self.uuid,
            "original_document_uuid": self.original_document_uuid,
            "original_page_number": self.original_page_number,
            "document": self.document,  # TBD
            "page_number": self.page_number,
            "total_pages": 0,  # TBD
            "annotation_uri": self.annotation,
            "page_description_uri": self.page_description,
            "annotation_confidence": self.annotation_confidence,
            "width": self.width,
            "height": self.height,
            "detected_template": self.detected_template.uuid,
            "mapped_template": self.mapped_template.uuid,
            "dependency_modified": self.dependency_modified,
            "classification_key": self.classification_key,
            "using_page_service": self.using_page_service,
            "s3_uris": self.s3_uris,
            "image": self.get_image_url(),  # TBD
        }


class ComponentResult(object):  # Extracted Data
    def __init__(
        self, component, processed_value, confidence_rate, box, page, document_uuid=None
    ):
        self.uuid = str(uuid.uuid4())
        self.component = component
        self.grouped_data = []
        self.parent = None
        self.processed_value = processed_value
        self.confidence_rate = confidence_rate
        self.box = box  # class Box
        self.page = page
        self.document_uuid = document_uuid

    def __lt__(self, other):
        return self.page_number < other.page_number or weight(self) < weight(other)

    def dehydrate_component_result(self):
        return {
            "uuid": self.uuid,
            "component": {
                "uuid": self.component.uuid,
                "category": self.component.category,
                "name": self.component.name,
            },
            "processed_value": self.processed_value,
            "confidence_rate": round(self.confidence_rate, 2),
            "page": self.page.page_number,
        }

    def print(self):
        print(
            "ComponentResult [% 5s % 5s % 5s % 5s] [%15s] [%50s]"
            % (
                str(self.box.xmin) if self.box else "N/A",
                str(self.box.ymin) if self.box else "N/A",
                str(self.box.xmax) if self.box else "N/A",
                str(self.box.ymax) if self.box else "N/A",
                self.component.name,
                self.processed_value,
            )
        )
        # print("self.parent", self.parent)
        if self.grouped_data:
            for d in self.grouped_data:
                d.print()
