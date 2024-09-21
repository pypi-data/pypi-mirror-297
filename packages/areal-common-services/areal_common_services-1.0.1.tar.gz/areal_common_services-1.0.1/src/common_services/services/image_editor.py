import base64
import datetime
import io
import logging
import os
from os.path import isfile, join

import cv2
import numpy as np
from pdf2image import convert_from_bytes
from PIL import ExifTags, Image
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter, utils

debug = False
time_debug = False

IMAGE_MAX_SIZE = 2880
DEFAULT_IMAGE_WIDTH = 1024

logger = logging.getLogger("areal")
logging.getLogger("pdfminer").setLevel(logging.ERROR)


class CropperFailedException(Exception):
    def __init__(self, msg):
        super(CropperFailedException, self).__init__("Cropper failed: " + msg)


def bytes_to_image(image_bytes):
    with io.BytesIO(image_bytes) as b:
        with Image.open(b) as image:
            image.load()
            # exif = {
            #     PIL.ExifTags.TAGS[k]: v
            #     for k, v in image._getexif().items()
            #     if k in PIL.ExifTags.TAGS
            # }
            # print("\n\nafter_load", exif)
            return image


def bytes_to_stream(image_bytes):
    return io.BytesIO(image_bytes)


def change_mode(image, mode):
    if hasattr(image, "mode") and image.mode != mode:
        image = image.convert(mode)
    return image


def change_format(image, format):
    if isinstance(image, bytes):
        return bytes_to_image(image)

    if image.format == format:
        return image

    with io.BytesIO() as temp:
        image.save(temp, format=format)
        image_with_new_format = bytes_to_image(temp.getvalue())
        temp.close()
    return image_with_new_format


def cleanup_noise(image):
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = cv2.multiply(img, 1.2)

    # create a kernel for the erode() function
    kernel = np.ones((2, 2), np.uint8)

    # erode() the image to bolden the text
    img = cv2.erode(img, kernel, iterations=1)

    # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 121, 2)
    # img = cv2.GaussianBlur(img, (1, 1), 0)
    # ret3, img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
    cleaned_image = Image.fromarray(img)
    return cleaned_image


def crop_to_boundries(image, x, y, width, height):
    return image.crop((x, y, x + width, y + height))


def file_to_base64(filepath):
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def file_to_images(path, force_pdf_to_image=False, size=None, dpi=200):
    if path.lower().endswith("pdf"):
        with open(path, "rb") as f:
            pdf_bytes = f.read()
            return pdf_to_images(
                pdf_bytes, force_pdf_to_image=force_pdf_to_image, size=size, dpi=dpi
            )
    else:
        with Image.open(path) as image:
            image.load()
            images = reduce_giant_images([image], do_not_normalize=True)
            return images


def file_to_pdf(path):
    images = []
    with open(path, "rb") as file:
        pdf = PdfFileReader(file)
        for page in range(pdf.getNumPages()):
            pdf_pageObj = pdf.getPage(page)
            pdf_pageObj = fix_pdf_rotation(pdf_pageObj)
            pdf_out = PdfFileWriter()
            pdf_out.addPage(pdf_pageObj)
            with io.BytesIO() as output_pdf:
                pdf_out.write(output_pdf)
                image = output_pdf.getvalue()
                images.append(image)
                output_pdf.close()
    return images


def fix_pdf_rotation(pageObj):
    rotation_debug = False
    print("\n\nFIX_PDF_ROTATION") if rotation_debug else None
    try:
        if not (
            isinstance(pageObj.get("/Rotate"), int)
            or isinstance(pageObj.get("/Rotate"), str)
            or isinstance(pageObj.get("/Rotate"), bytes)
        ):
            print(
                "  !!  Warning: IndirectObject. Returning"
            ) if rotation_debug else None
            return pageObj
        print(
            "pageObj.get('/Rotate'):", pageObj.get("/Rotate")
        ) if rotation_debug else None
        orientation_degrees_value = pageObj.get(
            "/Rotate"
        )  # TypeError: int() argument must be a string, a bytes-like object or a number, not 'IndirectObject'
        orientation_degrees = (
            int(orientation_degrees_value)
            if isinstance(orientation_degrees_value, str)
            else pageObj.get("/Rotate")
        )
        is_portrait = bool(
            abs(pageObj.mediaBox.getUpperRight_x() - pageObj.mediaBox.getUpperLeft_x())
            < abs(
                pageObj.mediaBox.getUpperRight_y() - pageObj.mediaBox.getLowerRight_y()
            )
        )
        print(
            "Initial Orientation Degrees:",
            orientation_degrees,
            "--- is_portrait:",
            is_portrait,
            pageObj.mediaBox.getUpperRight_x() - pageObj.mediaBox.getUpperLeft_x(),
            pageObj.mediaBox.getUpperRight_y() - pageObj.mediaBox.getLowerRight_y(),
        ) if rotation_debug else None
        count = 0
        print(
            "Starting UL(%d, %d) UR(%d, %d) LL(%d, %d) LR(%d, %d)"
            % (
                pageObj.mediaBox.getUpperLeft_x(),
                pageObj.mediaBox.getUpperLeft_y(),
                pageObj.mediaBox.getUpperRight_x(),
                pageObj.mediaBox.getUpperRight_y(),
                pageObj.mediaBox.getLowerLeft_x(),
                pageObj.mediaBox.getLowerLeft_y(),
                pageObj.mediaBox.getLowerRight_x(),
                pageObj.mediaBox.getLowerRight_y(),
            )
        ) if rotation_debug else None
        if (is_portrait and orientation_degrees == 270) or (
            not is_portrait and (orientation_degrees == 0 or orientation_degrees == 180)
        ):
            while orientation_degrees != 0 and count < 4:
                pageObj = (
                    pageObj.rotateClockwise(90)
                    if orientation_degrees < 90
                    else pageObj.rotateCounterClockwise(90)
                )
                orientation_degrees = int(pageObj.get("/Rotate"))
                is_portrait = bool(
                    abs(
                        pageObj.mediaBox.getUpperRight_x()
                        - pageObj.mediaBox.getUpperLeft_x()
                    )
                    < abs(
                        pageObj.mediaBox.getUpperRight_y()
                        - pageObj.mediaBox.getLowerRight_y()
                    )
                )
                print(
                    "New Orientation Degrees:",
                    orientation_degrees,
                    "--- is_portrait Now:",
                    is_portrait,
                ) if rotation_debug else None
                print(
                    orientation_degrees,
                    ": UL(%d, %d) UR(%d, %d) LL(%d, %d) LR(%d, %d)"
                    % (
                        pageObj.mediaBox.getUpperLeft_x(),
                        pageObj.mediaBox.getUpperLeft_y(),
                        pageObj.mediaBox.getUpperRight_x(),
                        pageObj.mediaBox.getUpperRight_y(),
                        pageObj.mediaBox.getLowerLeft_x(),
                        pageObj.mediaBox.getLowerLeft_y(),
                        pageObj.mediaBox.getLowerRight_x(),
                        pageObj.mediaBox.getLowerRight_y(),
                    ),
                ) if rotation_debug else None
                count += 1
            return pageObj

        print("NO PDF NATIVE ROTATION") if rotation_debug else None
        return pageObj
    except ValueError:
        return pageObj


def get_pdf_page_in_bytes(pdf_file_bytes, page):
    pdf = PdfFileReader(io.BytesIO(pdf_file_bytes))
    if pdf.isEncrypted:
        pdf.decrypt("")

    if page >= pdf.numPages:
        return None

    page_object = pdf.getPage(page)
    pdf_writer = PdfFileWriter()
    pdf_writer.addPage(page_object)
    with io.BytesIO() as temporary_pdf:
        pdf_writer.write(temporary_pdf)  # Page Object to Bytes
        pdf_page_bytes = temporary_pdf.getvalue()
        temporary_pdf.close()
    return pdf_page_bytes


def seperate_pdf_into_pages(filepath, foldername):
    pages = []
    with open(filepath, "rb") as file:
        pdf = PdfFileReader(file)
        for page in range(pdf.getNumPages()):
            pdf_pageObj = pdf.getPage(page)
            pdf_pageObj = fix_pdf_rotation(pdf_pageObj)
            pdf_out = PdfFileWriter()
            pdf_out.addPage(pdf_pageObj)
            filename = os.path.basename(filepath)
            new_filename = filename[:-4] + "_AREALSPLIT_page_" + str(page + 1) + ".pdf"
            new_filename = new_filename.replace(" ", "_")
            new_filepath = join(foldername, new_filename)
            if not isfile(new_filepath):
                with open(new_filepath, "wb") as new_file:
                    pdf_out.write(new_file)
                # with io.BytesIO() as output_pdf:
                #     pdf_out.write(output_pdf)
                #     image = output_pdf.getvalue()
                #     images.append(image)
                #     with open(filename[:-4] + '_copy2.pdf', 'wb') as new_file_2:
                #         pdf_in = PdfFileReader(io.BytesIO(image))
                #         pdf_out_2 = PdfFileWriter()
                #         pdf_out_2.addPage(pdf_in.getPage(0))
                #         pdf_out_2.write(new_file_2)
                #         new_file_2.close()
            else:
                print("File exits:", os.path.basename(new_filepath))
            pages.append(new_filepath)
    return pages


def read_pdf(pdf_path_or_data):
    if isinstance(pdf_path_or_data, str):
        with open(pdf_path_or_data, "rb") as file:
            pdf = PdfFileReader(file)
            page = pdf.getPage(0)
            page_content = page.extractText()
            # print("READING PDF. Page count:", pdf.numPages)
            # print("Document info:", pdf.documentInfo)
            # print("Count of line splits:", len(page_content.split(' ')))
            file.close()
            return page_content
    elif isinstance(pdf_path_or_data, bytes):
        pdf = PdfFileReader(bytes_to_stream(pdf_path_or_data))
        page = pdf.getPage(0)
        page_content = page.extractText()
        # print("READING PDF. Page count:", pdf.numPages)
        # print("Document info:", pdf.documentInfo)
        # print("Count of line splits:", len(page_content.split(' ')))
        return page_content


def image_to_base64(image_or_pdf):
    if isinstance(image_or_pdf, bytes):
        # If it's in bytes, then it should be a PDF page
        image = pdf_to_images(image_or_pdf, force_pdf_to_image=True)[0]  #
    else:
        image = image_or_pdf

    image = change_mode(image, "RGB")
    with io.BytesIO() as buffered:
        image.save(buffered, format="JPEG")
        base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
        buffered.close()
    return base64_image


def pdf_to_base64(pdf_document):
    pdf_encoded_bytes = None
    if isinstance(pdf_document, bytes):
        pdf_encoded_bytes = base64.b64encode(pdf_document).decode("utf-8")
    return pdf_encoded_bytes


def image_to_bytes(image):
    image = change_mode(image, "RGB")
    jpeg_image = None
    with io.BytesIO() as b:
        image.save(b, format="JPEG")
        jpeg_image = b.getvalue()
        b.close()
    return jpeg_image


def pil_image_to_pdf_bytes(image):
    # covert image to pdf bytes
    pdf_bytes = None
    with io.BytesIO() as buffered:
        image.save(buffered, "PDF", resolution=200.0, save_all=True)
        pdf_bytes = buffered.getvalue()
        buffered.close()
    return pdf_bytes


def images_to_pdf(images):
    EOF_MARKER = b"%%EOF"
    im1 = images[0]
    pdf = None
    if isinstance(im1, bytes):
        pdf = PdfFileMerger()
        for p in images:
            if p:
                pdf.append(bytes_to_stream(p))

    with io.BytesIO() as buffered:
        pdf.write(buffered) if pdf else im1.save(
            buffered, "PDF", resolution=200.0, save_all=True, append_images=images[1:]
        )

        buffered_bytes = buffered.getvalue()
        # print("buffered_bytes", buffered_bytes[-32:])
        # buffered_bytes b'2 0 R\n>>\nstartxref\n992896\n%%EOF\n'

        # check if EOF is somewhere else in the file
        if EOF_MARKER in buffered_bytes:
            # we can remove the early %%EOF and put it at the end of the file
            buffered_bytes = buffered_bytes.replace(EOF_MARKER, b"")
            buffered_bytes = buffered_bytes + EOF_MARKER
            # print("new buffered_bytes", buffered_bytes[-32:])
        else:
            # Some files really don't have an EOF marker
            buffered_bytes = buffered_bytes[:-5] + EOF_MARKER
            # print("new buffered_bytes", buffered_bytes[-32:])

        pdf_encoded_bytes = base64.b64encode(buffered_bytes).decode("utf-8")
        buffered.close()

    return pdf_encoded_bytes


def write_pdf_images_to_pdf_file(images, file_path):
    pdf = PdfFileMerger()
    for page in images:
        if page:
            pdf.append(
                bytes_to_stream(page)
            )  # Input: fileobj – Output file. Can be a filename or any kind of file-like object (Stream).

    with open(file_path, "wb") as new_pdf_file:
        pdf.write(new_pdf_file)
        new_pdf_file.close()

    return True


def normalize(image):
    # print("services/image_editor/normalize")
    image = change_mode(image, "RGB")
    image = change_format(image, "PNG")
    return image


# @lru_cache(maxsize=256)
def pdf_to_images(
    pdf_bytes,
    force_pdf_to_image=False,
    size=None,
    dpi=200,
    fmt="jpeg",
    force_no_pdf_link_removal=False,
):
    # start_time = datetime.datetime.now()
    if force_pdf_to_image:
        if size:
            if size == 9999:
                # FORCE USING ORIGINAL SIZE
                # print("\n\n Forcing Original Size")
                size = None
            else:
                # USE THE SIZE PROVIDED TO FUNCTION
                pass
        else:
            size = IMAGE_MAX_SIZE

        pages = convert_from_bytes(
            pdf_bytes, size=size, dpi=dpi, fmt=fmt
        )  # fmt='png' | 'jpeg' | default='ppm' No compression
        if not pages:
            return None
        return pages
    else:
        pages = list()
        # Convert raw bytes to stream. Stream are file-like objects that you can use at your convenience in run-time without saving the file
        try:
            pdf = PdfFileReader(bytes_to_stream(pdf_bytes), strict=False)
            if pdf.isEncrypted:
                pdf.decrypt("")
        except (utils.PdfReadError, NotImplementedError) as exp:
            logger.error("PDF error, skipping [%s]", exp)
            return None

        if not pdf or not int(float(pdf.getNumPages())):
            logger.error("\nNO PDF")
            return None
        for page in range(pdf.getNumPages()):
            page_object = pdf.getPage(page)
            page_object = fix_pdf_rotation(page_object)
            # print("\n\n\npage_object.mediaBox", page_object.mediaBox)
            pdf_out = PdfFileWriter()
            pdf_out.addPage(page_object)
            with io.BytesIO() as output_pdf:
                if not force_no_pdf_link_removal:
                    pdf_out.removeLinks()  # New - Yasin Found the Recursive Nature of the Issue
                pdf_out.write(output_pdf)
                image = output_pdf.getvalue()
                pages.append(image)
                output_pdf.close()
        # print('services/image_editor/pdf_to_images PDF to PDF_PAGES Conversion:[%d] ms' % int((datetime.datetime.now() - start_time).total_seconds() * 1000))
        return pages


def reduce_giant_images(images, do_not_normalize=True):
    start_time = datetime.datetime.now() if time_debug else None

    max_size = IMAGE_MAX_SIZE
    reduced_images = []
    for image in images:
        image = image if do_not_normalize else normalize(image)

        if time_debug:
            end_time = datetime.datetime.now()
            time_spent = int((end_time - start_time).total_seconds() * 1000)
            print(">>>> Image NORMALIZATION Took =", time_spent, "ms")
            start_time = datetime.datetime.now()

        # TODO TURN DEBUG FALSE
        image.save("/tmp/1_original.png") if debug else None

        image = fixexif(image)

        if time_debug:
            end_time = datetime.datetime.now()
            time_spent = int((end_time - start_time).total_seconds() * 1000)
            print(">>>> Image FIXEXIF Took =", time_spent, "ms")
            start_time = datetime.datetime.now()

        # TODO TURN DEBUG FALSE
        image.save("/tmp/2_post_fixeif.png") if debug else None

        width, height = image.size
        if width > max_size or height > max_size:
            image = resize_to_maximum(image, max_size)

            if time_debug:
                print(
                    "reduce_giant_images reduced height width",
                    height,
                    width,
                    ">>>",
                    image.size,
                )
                end_time = datetime.datetime.now()
                time_spent = int((end_time - start_time).total_seconds() * 1000)
                print(">>>> Image RESIZE_TO_MAXIMUM Took =", time_spent, "ms")
                # logger.info('A giant image of %d bytes exceeded ratio by %f. Old=%s New=%s', file_size, ratio, str((width, height)), str(image.size))

        reduced_images.append(image)

        # TODO TURN DEBUG FALSE
        image.save("/tmp/3_post_fixeif_normalization.png") if debug else None

    return reduced_images


def fixexif(img):
    import piexif

    exif_bytes = None
    try:
        if "exif" in img.info:
            exif_dict = piexif.load(img.info["exif"])
            if piexif.ImageIFD.Orientation in exif_dict["0th"]:
                ori = exif_dict["0th"][piexif.ImageIFD.Orientation]
                old_ori = ori
                # print('Orientation %s' % ori)
                exif_dict["0th"][piexif.ImageIFD.Orientation] = 1
                if ori == 6:
                    img = img.rotate(-90, expand=True)
                elif ori == 8:
                    img = img.rotate(90, expand=True)
                elif ori == 3:
                    img = img.rotate(180)
                elif ori == 2:
                    img = img.transpose(Image.FLIP_LEFT_RIGHT)
                elif ori == 5:
                    img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                elif ori == 7:
                    img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                elif ori == 4:
                    img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
                print("New Orientation %s" % ori) if old_ori != ori else None
                exif_dict["Exif"][41729] = b"1"
                # FYI. Supressed: /Users/argunkilic/Documents/Development/dokumanai-web/env/lib/python3.7/site-packages/PIL/TiffImagePlugin.py:802: UserWarning: Corrupt EXIF data.
                # TODO: Change height and width of the image if it is +-90 rotated
                exif_bytes = piexif.dump(exif_dict)
                # img.save('/tmp/tmp_img.jpg', format='JPEG', exif=exif_bytes)
                with io.BytesIO() as t:
                    img.save(
                        t, format="JPEG", exif=exif_bytes
                    )  # temp test delete this!
                    return bytes_to_image(t.getvalue())
    except Exception as e:
        print("Error exif: %s" % e) if debug else None
    return img


def resize(image, new_width=0, new_height=0):
    new_width = int(new_width)
    new_height = int(new_height)
    width, height = image.size
    if new_width == width or new_height == height:
        return image
    if new_width and not new_height:
        new_height = stretch(width, height, new_width)
    if not new_width and new_height:
        new_width = stretch(height, width, new_height)
    new_image = image.resize((new_width, new_height), Image.LANCZOS)
    image.close()
    image = new_image
    # image.load()
    return image


def resize_to_maximum(image, new_maximum):
    width, height = image.size
    return (
        resize(image, new_width=new_maximum)
        if width > height
        else resize(image, new_height=new_maximum)
    )


def resize_to_minimum(image, new_minimum):
    width, height = image.size
    return (
        resize(image, new_height=new_minimum)
        if width > height
        else resize(image, new_width=new_minimum)
    )


def rotate(image, degrees):
    annotation = image.ocr_annotation if image.ocr_annotation else ""
    w, h = image.size
    image = resize(image, new_width=w * 2)
    image = image.rotate(
        (1 * degrees), resample=Image.BICUBIC, expand=True, fillcolor="#2F3942"
    )
    w, h = image.size
    image = resize(image, new_width=w / 2)
    image.load()
    image.ocr_annotation = annotation
    return image


def stretch(current_active_dimension, current_orthogonal_dimension, new_dimension):
    return int(
        current_orthogonal_dimension
        / ((current_active_dimension * 1.0) / new_dimension)
    )


def _correct_rotation(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == "Orientation":
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)

    except (AttributeError, KeyError, IndexError):
        # Image doesn't have EXIF
        pass

    return image


def get_pdf_size(pdf_bytes):
    pdf = PdfFileReader(io.BytesIO(pdf_bytes))
    pdf_pageObj = pdf.getPage(0)
    pdf_width = abs(
        pdf_pageObj.mediaBox.getUpperRight_x() - pdf_pageObj.mediaBox.getUpperLeft_x()
    )
    pdf_height = abs(
        pdf_pageObj.mediaBox.getUpperRight_y() - pdf_pageObj.mediaBox.getLowerRight_y()
    )
    return pdf_pageObj, (pdf_width, pdf_height)
