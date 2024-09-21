import json
import logging
import os
from functools import lru_cache

from google.cloud import vision
from retry import retry

debug = False
logger = logging.getLogger("areal")


class GoogleVisionGateway(object):
    def __init__(self):
        credentials = None
        EMPTY_RESPONSE = ("", 0)

        gac = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_TEST")

        # JSON file
        gac_file = open(gac, "r")

        print("gac", gac)
        if gac:
            credentials = json.loads(gac_file.read())

        self.google_client = vision.ImageAnnotatorClient(credentials=credentials)
        self.ocr_text, self.confidence = EMPTY_RESPONSE

    def scan(self, image, image_type):
        if image_type == "data:application/pdf":
            scanned = self.scan_pdf(image)
        else:
            scanned = self.scan_image(image)

        return scanned

    @lru_cache(maxsize=100)
    @retry(tries=10, delay=2, backoff=2, jitter=1)
    def scan_image(self, image_bytes):
        # print("--- scan_image is called here") if debug else debug
        google_image = vision.types.Image(content=image_bytes)
        extract = self.google_client.document_text_detection(google_image)
        annotation = extract.full_text_annotation
        if annotation and annotation.pages and annotation.pages[0].blocks:
            self.confidence = annotation.pages[0].blocks[0].confidence
            self.ocr_text = annotation.text
        return (self.ocr_text or "").strip(), annotation, self.confidence

    def scan_pdf(self, content):
        print("--- scan_pdf is called here")
        requests = [
            {
                "input_config": {"mime_type": "application/pdf", "content": content},
                "features": [
                    {"type": vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION},
                ],
                "pages": [],
            }
        ]
        annotation = []
        response = self.google_client.batch_annotate_files(requests)
        for image_response in response.responses[0].responses:
            _annotation = image_response.full_text_annotation
            annotation.append(_annotation)
        return annotation[0].text, annotation[0], self.confidence
