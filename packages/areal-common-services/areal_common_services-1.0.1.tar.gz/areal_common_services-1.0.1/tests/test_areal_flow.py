import base64
import sys

scripts_directory = sys.path[0]
services_directory = scripts_directory.replace("/scripts", "/services")
sys.path.append(services_directory)
print("Updated sys.path:", sys.path)
import image_editor


def new_image(image_base64, image_type, force_pdf_to_image=False):
    # PDF_BYTES or BYTES TO IMAGE
    decoded_image = base64.b64decode(
        image_base64
    )  # Decode the Base64 encoded bytes-like object or ASCII string
    if image_type == "data:application/pdf":
        # PDF to Pdf_images
        images = image_editor.pdf_to_images(
            decoded_image, force_pdf_to_image=force_pdf_to_image
        )
    else:
        # print("This is an IMAGE")
        images = [image_editor.bytes_to_image(decoded_image)]
    del decoded_image

    if image_type != "data:application/pdf":
        images = image_editor.reduce_giant_images(images, do_not_normalize=True)
    image = images[0]

    # TODO Annotation to be Called and the Rest of this to be Worked
    # _, annotation, _ = ocr_scan_image(image, image_type=image_type)
    # page_description = descriptions.parse_google_document_for_page(annotation)

    # if not page_description:
    #     logger.error('%s NO PAGE_DESCRIPTION!! [%s]' % (datetime.utcnow(), annotation.__class__.__name__))
    #
    # if page_description and options.get('get_sorted_text_with_detected_lines'):
    #     # from web.services import visual_line
    #     from common_services.services.detection import visual_line
    #     from common_services.services.descriptions import Signature, Marker, Visual_Line, Box, Lines
    #
    #     horizontal_lines, vertical_lines, non_filtered_horizontal_lines = visual_line.detect_lines_for_text_sorting(image)
    #     page_description.horizontal_lines = horizontal_lines
    #     page_description.vertical_lines = vertical_lines
    #     page_description.non_filtered_horizontal_lines = non_filtered_horizontal_lines


def ocr_scan_image(image, image_type):  # content = pdf_bytes
    import google_vision

    computer_vision_gateway = google_vision.GoogleVisionGateway()
    # image_bytes = image_editor.image_to_bytes(image) if not isinstance(image, bytes) else image
    annotation_text, annotation, confidence = computer_vision_gateway.scan(
        image=image, image_type=image_type
    )
    print("annotation_text", annotation_text)
    return annotation_text, annotation, confidence


def run_areal_server():
    inp_file = sys.argv[1]
    print(inp_file)
    file_base64 = image_editor.file_to_base64(inp_file)

    if inp_file and len(inp_file) > 5:
        if inp_file.lower()[-4:] == ".pdf":
            image_type = "data:application/pdf"
        elif inp_file.lower()[-4:] == ".png":
            image_type = "data:image/png"
        elif inp_file.lower()[-4:] == ".jpg":
            image_type = "data:image/jpg"
        else:
            image_type = "data:image/jpeg"
        new_image(file_base64, image_type=image_type)


if __name__ == "__main__":
    run_areal_server()
