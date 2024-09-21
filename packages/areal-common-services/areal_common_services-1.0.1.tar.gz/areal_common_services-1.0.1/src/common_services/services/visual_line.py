import io
import logging
import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from . import image_editor

logger = logging.getLogger("areal")

debug = False
debug_print = False
debug_image_save = False


def draw_img_2(lines, image):
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    for line in lines:
        x1, y1, x2, y2 = map(int, line[0])
        # x1, y1, x2, y2 = line[0]
        # cv2.line(cv_image, (x1, y1), (x2, y2), (0, 255, 0), 1)
        cv2.line(cv_image, (x1, y1), (x2, y2), (0, 255, 0), 3)

    output_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
    output_image.show()


def draw_img(lines, image):
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    for line in lines:
        x1, y1, x2, y2 = line
        # cv2.line(cv_image, (x1, y1), (x2, y2), (0, 255, 0), 1)
        cv2.line(cv_image, (x1, y1), (x2, y2), (0, 255, 0), 3)

    output_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
    output_image.show()


def horizontal_vertical_intersect(horizontal_line, vertical_line, threshold=7):
    xmin_h, ymin_h, xmax_h, ymax_h = horizontal_line
    xmin_v, ymin_v, xmax_v, ymax_v = vertical_line

    # if x1 < x3-7 and x3 <= x2-7 and y3 >= y1 and y4 <= y2:
    # if x3 > x1 or (7 > abs(x1-x3) and abs(x1-x3) > 0):
    #    if x2 > x3 or (7 > abs(x2-x3) and abs(x2-x3) > 0):
    if xmin_v > xmin_h and xmax_h > xmax_v:
        if ymin_h >= ymin_v or (threshold > abs(ymin_v - ymin_h)):
            if ymax_v > ymin_h or (threshold > abs(ymax_v - ymin_h)):
                return True

    return False


def merge_intervals(intervals):
    if not intervals:
        return []

    # Sort the intervals based on the start time
    sorted_intervals = sorted(intervals, key=lambda x: x[0])

    merged_intervals = [sorted_intervals[0]]

    for current_interval in sorted_intervals[1:]:
        last_merged_interval = merged_intervals[-1]

        # Check for overlap
        if current_interval[0] <= last_merged_interval[1]:
            # Merge the overlapping intervals
            last_merged_interval = (
                last_merged_interval[0],
                max(last_merged_interval[1], current_interval[1]),
            )
            merged_intervals[-1] = last_merged_interval
        else:
            # No overlap, add the current interval to the merged list
            merged_intervals.append(current_interval)

    return merged_intervals


def define_ranges(coordinates, threshold):
    range_list = []
    for coordinate in set(coordinates):
        range_list.append((coordinate - threshold, coordinate + threshold))

    merged_ranges = merge_intervals(range_list)

    my_dict = dict()
    for ranges in merged_ranges:
        my_dict[ranges] = []

    return my_dict


def horizontal_line_store_wrt_y_axis(horizontal_lines, threshold=5):
    my_dict = define_ranges([y[0][1] for y in horizontal_lines], threshold)

    for line in horizontal_lines:
        xmin, ymin, xmax, ymax = line[0]

        for key in my_dict:
            left_range, right_range = key

            if left_range <= ymin <= right_range:
                my_dict[key].append(line)

    return my_dict


def vertical_line_store_wrt_x_axis(vertical_lines, threshold=5):
    my_dict = define_ranges([x[0][0] for x in vertical_lines], threshold)

    for line in vertical_lines:
        xmin, ymin, xmax, ymax = line[0]

        for key in my_dict:
            left_range, right_range = key

            if left_range <= xmin <= right_range:
                my_dict[key].append(line)

    return my_dict


def arrange_y_coordinates_of_horizontal_lines(horizontal_lines):
    new_lines = []
    for lines in horizontal_lines:
        xmin, ymin, xmax, ymax = lines[0]
        new_y = np.mean([ymin, ymax])
        new_y = int(new_y)
        new_lines.append(np.asarray([xmin, new_y, xmax, new_y]).reshape(1, 4))

    return new_lines


def arrange_x_coordinates_of_vertical_lines(vertical_lines):
    new_lines = []
    for lines in vertical_lines:
        xmin, ymin, xmax, ymax = lines[0]
        new_x = np.mean([xmin, xmax])
        new_x = int(new_x)
        new_lines.append(np.asarray([new_x, ymin, new_x, ymax]).reshape(1, 4))

    return new_lines


def filter_vertical_lines(vertical_lines, threshold=5):
    vertical_lines = arrange_x_coordinates_of_vertical_lines(vertical_lines)
    vertical_lines = vertical_line_store_wrt_x_axis(vertical_lines, threshold=threshold)

    for keys, vertical_line_list in vertical_lines.items():
        ind_1 = 0
        while ind_1 < len(vertical_line_list):
            horizontal_line_1 = vertical_line_list[ind_1]
            xmin_1, ymin_1, xmax_1, ymax_1 = horizontal_line_1[0]

            deleted_inds = []

            ind_2 = ind_1 + 1
            while ind_2 < len(vertical_line_list):
                horizontal_line_2 = vertical_line_list[ind_2]

                xmin_2, ymin_2, xmax_2, ymax_2 = horizontal_line_2[0]

                if ymin_1 <= ymin_2 <= ymax_1 and ymax_1 >= ymax_2:
                    xmin_1, ymin_1, xmax_1, ymax_1 = xmin_1, ymin_1, xmin_1, ymax_1
                    deleted_inds.append(ind_2)

                elif ymin_1 <= ymin_2 < ymax_1 <= ymax_2:
                    xmin_1, ymin_1, xmax_1, ymax_1 = (
                        (xmin_1 + xmin_2) / 2,
                        ymin_1,
                        (xmin_1 + xmin_2) / 2,
                        ymax_2,
                    )
                    deleted_inds.append(ind_2)

                elif ymin_2 <= ymin_1 < ymax_2 and ymax_2 >= ymax_1:
                    xmin_1, ymin_1, xmax_1, ymax_1 = xmin_2, ymin_2, xmin_2, ymax_2
                    deleted_inds.append(ind_2)

                elif ymin_2 <= ymin_1 < ymax_2 <= ymax_1:
                    xmin_1, ymin_1, xmax_1, ymax_1 = (
                        (xmin_1 + xmin_2) / 2,
                        ymin_2,
                        (xmin_1 + xmin_2) / 2,
                        ymax_1,
                    )
                    deleted_inds.append(ind_2)

                ind_2 += 1

            if len(deleted_inds) > 0:
                ind = 0
                while ind < len(deleted_inds):
                    item = deleted_inds[ind]
                    vertical_lines[keys].pop(item)
                    deleted_inds = [i - 1 for i in deleted_inds]
                    ind += 1

                vertical_lines[keys][ind_1] = [[xmin_1, ymin_1, xmax_1, ymax_1]]
                ind_1 = 0

            else:
                ind_1 += 1

    filtered_list = []
    for key, vertical_line_list in vertical_lines.items():
        for line in vertical_line_list:
            x1, y1, x2, y2 = line[0]
            filtered_list.append(
                np.asarray([int(x1), int(y1), int(x2), int(y2)]).reshape(1, 4)
            )

    return filtered_list


def filter_horizontal_lines(horizontal_lines, threshold=5):
    horizontal_lines = arrange_y_coordinates_of_horizontal_lines(horizontal_lines)
    horizontal_line_dict = horizontal_line_store_wrt_y_axis(
        horizontal_lines, threshold=threshold
    )

    for keys, horizontal_line_list in horizontal_line_dict.items():
        ind_1 = 0
        while ind_1 < len(horizontal_line_list):
            horizontal_line_1 = horizontal_line_list[ind_1]
            xmin_1, ymin_1, xmax_1, ymax_1 = horizontal_line_1[0]

            deleted_inds = []

            ind_2 = ind_1 + 1
            while ind_2 < len(horizontal_line_list):
                horizontal_line_2 = horizontal_line_list[ind_2]

                xmin_2, ymin_2, xmax_2, ymax_2 = horizontal_line_2[0]

                if xmin_1 <= xmin_2 <= xmax_1 and xmax_1 >= xmax_2:
                    xmin_1, ymin_1, xmax_1, ymax_1 = xmin_1, ymin_1, xmax_1, ymax_1
                    deleted_inds.append(ind_2)

                elif xmin_1 <= xmin_2 <= xmax_1 <= xmax_2:
                    xmin_1, ymin_1, xmax_1, ymax_1 = (
                        xmin_1,
                        (ymin_1 + ymin_2) / 2,
                        xmax_2,
                        (ymax_1 + ymin_2) / 2,
                    )
                    deleted_inds.append(ind_2)

                elif xmin_2 <= xmin_1 <= xmax_2 and xmax_2 >= xmax_1:
                    xmin_1, ymin_1, xmax_1, ymax_1 = xmin_2, ymin_2, xmax_2, ymin_2
                    deleted_inds.append(ind_2)

                elif xmin_2 <= xmin_1 <= xmax_2 <= xmax_1:
                    xmin_1, ymin_1, xmax_1, ymax_1 = (
                        xmin_2,
                        (ymin_1 + ymin_2) / 2,
                        xmax_1,
                        (ymax_1 + ymin_2) / 2,
                    )
                    deleted_inds.append(ind_2)

                ind_2 += 1

            if len(deleted_inds) > 0:
                ind = 0
                while ind < len(deleted_inds):
                    item = deleted_inds[ind]
                    horizontal_line_dict[keys].pop(item)
                    deleted_inds = [i - 1 for i in deleted_inds]
                    ind += 1

                horizontal_line_dict[keys][ind_1] = [[xmin_1, ymin_1, xmax_1, ymax_1]]
                ind_1 = 0

            else:
                ind_1 += 1

    filtered_list = []
    for key, horizontal_line_list in horizontal_line_dict.items():
        for line in horizontal_line_list:
            x1, y1, x2, y2 = line[0]
            filtered_list.append(
                np.asarray([int(x1), int(y1), int(x2), int(y2)]).reshape(1, 4)
            )

    return filtered_list


def get_lines(img_bin, kernel, final_kernel):
    img_bin_line = cv2.morphologyEx(
        ~img_bin, cv2.MORPH_OPEN, kernel
    )  # detecting Horizontal lines by applying horizontal kernel
    img_bin_final = cv2.dilate(
        img_bin_line, final_kernel, iterations=1
    )  # adding a layer of dilation to close small gaps
    contours, _ = cv2.findContours(
        img_bin_final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Filter horizontal lines based on aspect ratio
    lines = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # lines.append((x, y, x + w, y + h))
        lines.append(
            np.asarray([x, y, x + w, y + h]).reshape(1, 4)
        )  # Store top-left and bottom-right coordinates

    return lines


def filter_horizontal_lines_for_text_sorting(horizontal_lines):
    filtered_lines = []

    for line in horizontal_lines:
        xmin_horizontal, ymin_horizontal, xmax_horizontal, ymax_horizontal = line[0]

        if len(filtered_lines) > 0:
            found = False
            for filtered_line in filtered_lines:
                xmin_filtered, ymin_filtered, xmax_filtered, ymax_filtered = (
                    filtered_line[0]
                )

                if abs(ymin_filtered - ymin_horizontal) <= 7:
                    if (
                        abs(xmin_horizontal - xmin_filtered) <= 10
                        and abs(xmax_filtered - xmax_horizontal) <= 10
                    ):
                        found = True
                        break
            if not found:
                filtered_lines.append(line)
        else:
            filtered_lines.append(line)

    return filtered_lines


def find_all_horizontals(
    all_horizontal_lines, non_splitted_horizontals, filtered_horizontal_lines
):
    horizontal_lines = (
        all_horizontal_lines + non_splitted_horizontals + filtered_horizontal_lines
    )
    horizontal_lines = filter_horizontal_lines_for_text_sorting(horizontal_lines)
    return horizontal_lines


def normalize_lines(line_array, image_width, image_height):
    normalized_lines = []
    for line in line_array:
        xmin, ymin, xmax, ymax = line[0]

        xmin_normalized = round(xmin / image_width, 3)
        xmax_normalized = round(xmax / image_width, 3)

        ymin_normalized = round(ymin / image_height, 3)
        ymax_normalized = round(ymax / image_height, 3)

        normalized_lines.append(
            [xmin_normalized, ymin_normalized, xmax_normalized, ymax_normalized]
        )

    return normalized_lines


def inverse_normalize_coordinates(normalized_coordinates, width, height):
    coordinates = []
    for line in normalized_coordinates:
        xmin_normalized, ymin_normalized, xmax_normalized, ymax_normalized = line

        xmin = int(xmin_normalized * width)
        xmax = int(xmax_normalized * width)

        ymin = int(ymin_normalized * height)
        ymax = int(ymax_normalized * height)

        coordinates.append(np.asarray([xmin, ymin, xmax, ymax]).reshape(1, 4))

    return coordinates


def get_percentages_from_coordinates(coordinates, page_width, page_height):
    x1, y1, x2, y2 = coordinates
    x, y, w, h = x1, y1, abs(x2 - x1), abs(y2 - y1)
    return (
        round(x / page_width, 3),
        round(y / page_height, 3),
        round(w / page_width, 3),
        round(h / page_height, 3),
    )


def image_to_bytearray(image):
    # Bellek dosyası oluştur
    img_byte_array = io.BytesIO()

    # Resmi bellek dosyasına kaydet
    image.save(img_byte_array, format="JPEG")

    # Bellek dosyasının içeriğini bir bytearray olarak döndür
    return bytearray(img_byte_array.getvalue())


def create_lines(
    image,
    save_to_file=False,
    vertical_thickness=None,
    horizontal_thickness=None,
    horizontal_line_width_threshold=25,
    vertical_line_length_threshold=55,
):
    horizontal_lines, vertical_lines = detect_lines_for_line_creation(
        image,
        line_filter_gap_threshold=5,
        horizontal_line_width_threshold=horizontal_line_width_threshold,
        vertical_line_length_threshold=vertical_line_length_threshold,
    )
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    if horizontal_thickness:
        for line in horizontal_lines:
            x1, y1, x2, y2 = line[0]
            # cv2.line(cv_image, (x1, y1), (x2, y2), (0, 255, 0), 1)
            cv2.line(cv_image, (x1, y1), (x2, y2), (0, 0, 0), horizontal_thickness)

    if vertical_thickness:
        for line in vertical_lines:
            x1, y1, x2, y2 = line[0]
            # cv2.line(cv_image, (x1, y1), (x2, y2), (0, 255, 0), 1)
            cv2.line(cv_image, (x1, y1), (x2, y2), (0, 0, 0), vertical_thickness)

    output_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))

    if save_to_file:
        return image_to_bytearray(output_image)
    else:
        return output_image


def detect_lines(
    image, horizontal_line_width_threshold=35, vertical_line_length_threshold=55
):
    # image = np.array(image)
    gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # binarising the image

    height, width, _ = image.shape
    print(f"Image size: {width}x{height} pixels") if debug_print else None

    # line_min_width = width // 10
    line_min_width_hor = width // horizontal_line_width_threshold
    line_min_len_ver = height // vertical_line_length_threshold
    dilation_size = 2

    img_bin = cv2.adaptiveThreshold(
        gray_scale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 2
    )
    final_kernel = np.ones((dilation_size, dilation_size), np.uint8)

    kernal_h = np.ones(
        (1, line_min_width_hor), np.uint8
    )  # defining horizontal kernel for morphological operations
    kernel_v = np.ones(
        (line_min_len_ver, 1), np.uint8
    )  # defining vertical kernel for morphological operations

    vertical_lines = get_lines(img_bin, kernel_v, final_kernel)
    horizontal_lines = get_lines(img_bin, kernal_h, final_kernel)

    return horizontal_lines, vertical_lines


def detect_lines_for_text_sorting(
    image, horizontal_line_width_threshold=35, vertical_line_length_threshold=55
):
    print("\n--visual_line.py--") if debug_print else None
    if not image:
        print("Error:No Image") if debug_print else None
        return [], [], []

    try:
        if isinstance(image, bytes):
            # This is a pdf
            print("This is a PDF") if debug_print else None
            pil_image = image_editor.pdf_to_images(
                image, force_pdf_to_image=True, size=2880
            )[0]
            original_image = np.array(pil_image)
        else:
            print("This is a PIL image") if debug_print else None
            original_image = np.array(image)
    except Exception as e:
        print("Issue converting to image array", e) if debug_print else None
        return [], [], []

    # Detect Lines
    height, width, _ = original_image.shape
    # print(f"Image size: {width}x{height} pixels")

    horizontal_lines, vertical_lines = detect_lines(
        original_image,
        horizontal_line_width_threshold=horizontal_line_width_threshold,
        vertical_line_length_threshold=vertical_line_length_threshold,
    )
    horizontal_lines = filter_horizontal_lines(horizontal_lines)
    vertical_lines = filter_vertical_lines(vertical_lines)

    # Iterate over the output lines and draw them on the image
    if isinstance(horizontal_lines, type(None)):
        return [[], []]

    filtered_horizontal_lines = sorted(
        horizontal_lines, key=lambda x: (x[0][1], x[0][0])
    )
    filtered_vertical_lines = sorted(vertical_lines, key=lambda x: (x[0][1], x[0][0]))

    non_splitted_horizontals = []
    for i, line in enumerate(filtered_vertical_lines):
        x1, y1, x2, y2 = line[0]

        ind = 0
        while ind < len(filtered_horizontal_lines):
            horizontal_line = filtered_horizontal_lines[ind]
            _x1, _y1, _x2, _y2 = horizontal_line[0]

            # Check if the horizontal line intersects the vertical line
            if horizontal_vertical_intersect(horizontal_line[0], line[0], threshold=10):
                # Split the horizontal line into two segments

                if abs(_x1 - x1) > 10:
                    filtered_horizontal_lines.append(
                        np.asarray([_x1, _y1, x1, _y2]).reshape(1, 4)
                    )  # For visualization
                if abs(x1 - _x2) > 10:
                    if debug:
                        filtered_horizontal_lines.append(
                            np.asarray([x1 + 15, _y1, _x2, _y2]).reshape(1, 4)
                        )  # For visualization
                    else:
                        filtered_horizontal_lines.append(
                            np.asarray([x1, _y1, _x2, _y2]).reshape(1, 4)
                        )  # For visualization
                non_splitted_horizontals.append(filtered_horizontal_lines.pop(ind))
                ind = 0
            else:
                ind += 1

    all_horizontals = find_all_horizontals(
        horizontal_lines, non_splitted_horizontals, filtered_horizontal_lines
    )

    return (
        normalize_lines(filtered_horizontal_lines, width, height),
        normalize_lines(filtered_vertical_lines, width, height),
        normalize_lines(all_horizontals, width, height),
    )


def detect_lines_for_line_creation(
    image,
    line_filter_gap_threshold=5,
    horizontal_line_width_threshold=35,
    vertical_line_length_threshold=55,
):
    print("\n--visual_line.py--") if debug_print else None
    if not image:
        print("Error:No Image") if debug_print else None

    pil_image = image
    if isinstance(pil_image, bytes):
        # This is a pdf
        print("This is a PDF") if debug_print else None
        original_image = image_editor.pdf_to_images(
            pil_image, force_pdf_to_image=True, size=2880
        )[0]
    elif isinstance(pil_image, dict):
        original_image = pil_image
        print("This is an image url") if debug_print else None
    else:
        original_image = pil_image
        print("This is a PIL image") if debug_print else None

    # Detect Lines
    original_image = np.array(original_image)
    height, width, _ = original_image.shape
    print(f"Image size: {width}x{height} pixels") if debug_print else None

    horizontal_lines, vertical_lines = detect_lines(
        original_image,
        horizontal_line_width_threshold=horizontal_line_width_threshold,
        vertical_line_length_threshold=vertical_line_length_threshold,
    )
    horizontal_lines = filter_horizontal_lines(
        horizontal_lines, line_filter_gap_threshold
    )
    vertical_lines = filter_vertical_lines(vertical_lines, line_filter_gap_threshold)

    if isinstance(horizontal_lines, type(None)):
        return []

    # if debug:
    #    draw_img_2(filtered_horizontal_lines, image)
    # if debug:
    #    draw_img_2(filtered_vertical_lines, image)

    filtered_horizontal_lines = sorted(
        horizontal_lines, key=lambda x: (x[0][1], x[0][0])
    )
    filtered_vertical_lines = sorted(vertical_lines, key=lambda x: (x[0][1], x[0][0]))

    for i, line in enumerate(filtered_vertical_lines):
        x1, y1, x2, y2 = line[0]

        ind = 0
        while ind < len(filtered_horizontal_lines):
            horizontal_line = filtered_horizontal_lines[ind]
            _x1, _y1, _x2, _y2 = horizontal_line[0]

            # Check if the horizontal line intersects the vertical line
            if horizontal_vertical_intersect(horizontal_line[0], line[0], threshold=7):
                # Split the horizontal line into two segments

                if abs(_x1 - x1) > 10:
                    filtered_horizontal_lines.append(
                        np.asarray([_x1, _y1, x1, _y2]).reshape(1, 4)
                    )  # For visualization
                if abs(x1 - _x2) > 10:
                    if debug:
                        filtered_horizontal_lines.append(
                            np.asarray([x1 + 15, _y1, _x2, _y2]).reshape(1, 4)
                        )  # For visualization
                    else:
                        filtered_horizontal_lines.append(
                            np.asarray([x1, _y1, _x2, _y2]).reshape(1, 4)
                        )  # For visualization
                filtered_horizontal_lines.pop(ind)
                ind = 0
            else:
                ind += 1

    if debug:
        cv_image = cv2.cvtColor(np.array(original_image), cv2.COLOR_RGB2BGR)

        def draw_final_lines(lines, color_code, thickness):
            for line in lines:
                x1, y1, x2, y2 = line[0]
                # cv2.line(cv_image, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cv2.line(cv_image, (x1, y1), (x2, y2), color_code, thickness)

        # draw_final_lines(sorted_lines, (255, 0, 0), thickness = 2)
        # draw_final_lines(vertical_lines, (0, 255, 0), thickness = 2)
        draw_final_lines(filtered_horizontal_lines, (0, 0, 255), thickness=2)

        # line = filtered_lines[10]
        # print(line)
        # x1, y1, x2, y2 = line[0]
        # cv2.line(cv_image, (x1, y1), (x2, y2), (0, 0, 255), 3)
        # Save the image with drawn lines
        output_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
        output_image.show()
        # output_image.save(r'C:\Users\berke\Desktop\areal\ocr\line_detection\output\page_13.png')

    if debug_image_save:
        cv_image = cv2.cvtColor(np.array(original_image), cv2.COLOR_RGB2BGR)
        for line in filtered_horizontal_lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(cv_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Save the image with drawn lines
        output_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
        output_image.save("/Users/argunkilic/Desktop/visual_lines.jpg", "JPEG")

    return filtered_horizontal_lines, filtered_vertical_lines


def detect_lines_for_annotation_tagging(
    image,
    line_filter_gap_threshold=5,
    horizontal_line_width_threshold=35,
    vertical_line_length_threshold=55,
    make_lines_thicker=True,
):
    print("\n--visual_line.py--") if debug_print else None
    if not image:
        print("Error:No Image") if debug_print else None

    pil_image = image
    if isinstance(pil_image, bytes):
        # This is a pdf
        print("This is a PDF") if debug_print else None
        original_image = image_editor.pdf_to_images(
            pil_image, force_pdf_to_image=True, size=2880
        )[0]
    elif isinstance(pil_image, dict):
        original_image = pil_image
        print("This is an image url") if debug_print else None
    else:
        original_image = pil_image
        print("This is a PIL image") if debug_print else None

    # Detect Lines
    original_image = np.array(original_image)
    height, width, _ = original_image.shape
    print(f"Image size: {width}x{height} pixels") if debug_print else None

    horizontal_lines, vertical_lines = detect_lines(
        original_image,
        horizontal_line_width_threshold=horizontal_line_width_threshold,
        vertical_line_length_threshold=vertical_line_length_threshold,
    )
    horizontal_lines = filter_horizontal_lines(
        horizontal_lines, line_filter_gap_threshold
    )
    vertical_lines = filter_vertical_lines(vertical_lines, line_filter_gap_threshold)

    if isinstance(horizontal_lines, type(None)):
        return []

    # if debug:
    #    draw_img_2(filtered_horizontal_lines, image)
    # if debug:
    #    draw_img_2(filtered_vertical_lines, image)

    filtered_horizontal_lines = sorted(
        horizontal_lines, key=lambda x: (x[0][1], x[0][0])
    )
    filtered_vertical_lines = sorted(vertical_lines, key=lambda x: (x[0][1], x[0][0]))

    for i, line in enumerate(filtered_vertical_lines):
        x1, y1, x2, y2 = line[0]

        ind = 0
        while ind < len(filtered_horizontal_lines):
            horizontal_line = filtered_horizontal_lines[ind]
            _x1, _y1, _x2, _y2 = horizontal_line[0]

            # Check if the horizontal line intersects the vertical line
            if horizontal_vertical_intersect(horizontal_line[0], line[0], threshold=7):
                # Split the horizontal line into two segments

                if abs(_x1 - x1) > 10:
                    filtered_horizontal_lines.append(
                        np.asarray([_x1, _y1, x1, _y2]).reshape(1, 4)
                    )  # For visualization
                if abs(x1 - _x2) > 10:
                    if debug:
                        filtered_horizontal_lines.append(
                            np.asarray([x1 + 15, _y1, _x2, _y2]).reshape(1, 4)
                        )  # For visualization
                    else:
                        filtered_horizontal_lines.append(
                            np.asarray([x1, _y1, _x2, _y2]).reshape(1, 4)
                        )  # For visualization
                filtered_horizontal_lines.pop(ind)
                ind = 0
            else:
                ind += 1

    if debug:
        cv_image = cv2.cvtColor(np.array(original_image), cv2.COLOR_RGB2BGR)

        def draw_final_lines(lines, color_code, thickness):
            for line in lines:
                x1, y1, x2, y2 = line[0]
                # cv2.line(cv_image, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cv2.line(cv_image, (x1, y1), (x2, y2), color_code, thickness)

        # draw_final_lines(sorted_lines, (255, 0, 0), thickness = 2)
        # draw_final_lines(vertical_lines, (0, 255, 0), thickness = 2)
        draw_final_lines(filtered_horizontal_lines, (0, 0, 255), thickness=2)

        # line = filtered_lines[10]
        # print(line)
        # x1, y1, x2, y2 = line[0]
        # cv2.line(cv_image, (x1, y1), (x2, y2), (0, 0, 255), 3)
        # Save the image with drawn lines
        output_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
        output_image.show()
        # output_image.save(r'C:\Users\berke\Desktop\areal\ocr\line_detection\output\page_13.png')

    if debug_image_save:
        cv_image = cv2.cvtColor(np.array(original_image), cv2.COLOR_RGB2BGR)
        for line in filtered_horizontal_lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(cv_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Save the image with drawn lines
        output_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
        output_image.save("/Users/argunkilic/Desktop/visual_lines.jpg", "JPEG")

    normalized_lines = []
    for line in filtered_horizontal_lines:
        x1, y1, x2, y2 = line[0]
        if make_lines_thicker:
            y1 = y1 - 3
            y2 = y2 + 3
        print(
            f"Normalized filtered line: {(x1, y1)} to {(x2, y2)}"
        ) if debug_print else None
        normalized_lines.append(
            get_percentages_from_coordinates((x1, y1, x2, y2), width, height)
        )

    return normalized_lines


def show(image, image_name=""):
    show_wait_destroy = False
    if show_wait_destroy:
        if image.shape and len(image.shape) == 2:
            img_h, img_w = image.shape
            image = cv2.resize(image, (int(img_w * 0.5), int(img_h * 0.5)))
        cv2.imshow(image_name, image)
        cv2.moveWindow(image_name, 0, 0)
        cv2.waitKey(0)
        cv2.destroyWindow(image_name)
    else:
        fig, ax = plt.subplots(figsize=(10, 14))
        fig.canvas.set_window_title(image_name)
        ax.imshow(image)
        # ax.set_axis_off()
        plt.tight_layout()
        plt.show()


def run():
    inp_file = sys.argv[1]
    print(inp_file)
    images = image_editor.file_to_images(inp_file)
    pil_image = images[0]
    # img = create_lines(pil_image,vertical_thickness=3,horizontal_thickness=3,horizontal_line_width_threshold=35,vertical_line_length_threshold=55)
    detect_lines_for_annotation_tagging(
        pil_image,
        line_filter_gap_threshold=5,
        horizontal_line_width_threshold=35,
        vertical_line_length_threshold=55,
    )


if __name__ == "__main__":
    run()
