import math
import re
import string
from collections import defaultdict

import numpy as np

from . import constants


def custom_round(number):
    decimal_part = number - int(number)  # Extract the decimal part
    if decimal_part < 0.5:
        return math.floor(number)
    else:
        return math.ceil(number)


def normalize_thresholds_in_x_axis(threshold, page_width):
    return int(custom_round((threshold / 1700) * page_width))


def normalize_thresholds_in_y_axis(threshold, page_height):
    return int(custom_round((threshold / 2200) * page_height))


def normalize_page_area(threshold, page_width, page_height):
    area = threshold / (1700 * 2200)
    normalized_area = area * page_width * page_height
    return int(custom_round(normalized_area))


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


def merge_close_distances(dictionary, distance=5):
    result_dict = defaultdict(list)
    sorted_keys = list(dictionary.keys())
    current_key = None
    current_values = []
    current_keys = []
    for key in sorted_keys:
        if current_key is None:
            current_key = key
            current_values = dictionary[key]
            current_keys.append(key)
        elif abs(key - current_key) < distance:
            current_values.extend(dictionary[key])
            current_keys.append(key)
        else:
            current_values = sorted(current_values, key=lambda x: x[0])
            mean_key = int(sum(current_keys) / len(current_keys))
            result_dict[mean_key] = current_values
            current_key = key
            current_values = dictionary[key]
            current_keys = [current_key]

    # Add the last set of values
    if current_key is not None:
        current_values = sorted(current_values, key=lambda x: x[0])
        mean_key = int(sum(current_keys) / len(current_keys))
        result_dict[mean_key] = current_values
        result_dict[mean_key] = current_values

    return result_dict


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


def arrange_y_coordinates_of_horizontal_lines(horizontal_lines):
    new_lines = []
    for lines in horizontal_lines:
        xmin, ymin, xmax, ymax = lines[0]
        new_y = np.mean([ymin, ymax])
        new_y = int(new_y)
        new_lines.append(np.asarray([xmin, new_y, xmax, new_y]).reshape(1, 4))

    return new_lines


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


def filter_lines_wtr_occurences(dictionary):
    keys_to_remove = [
        key
        for key, horizontal_line_list in dictionary.items()
        if len(horizontal_line_list) < 2
    ]
    for key in keys_to_remove:
        del dictionary[key]

    return dictionary


def filter_pattern_lines(pattern_dict):
    return {
        key: lines_list
        for key, lines_list in pattern_dict.items()
        if len(lines_list) >= 2
    }


def organise_information_order(info_dict):
    search_keys = [
        "city",
        "state",
        "zip",
        "phone",
        "name",
        "address",
        "firm",
        "listing",
        "date",
        "associate",
        "broker",
    ]
    infos = list(info_dict.keys())

    infos_1 = [keys.split("<split>")[0] for keys in infos]
    infos_2 = [keys.split("<split>")[1] for keys in infos]

    entire_infos_1 = " ".join(infos_1).lower()

    new_info_dict = dict()
    for keys in search_keys:
        if keys in entire_infos_1:
            merged_list = [s1 + " : " + s2 for s1, s2 in zip(infos_1, infos_2)]
            break
        else:
            merged_list = [s1 + " : " + s2 for s1, s2 in zip(infos_2, infos_1)]
            break

    for ind, new_keys in enumerate(merged_list):
        new_info_dict[new_keys] = info_dict[infos[ind]]

    return new_info_dict


def sort_text_with_horizontal_wo_vertical(info_dict, my_dict):
    for info_text, info_item in info_dict.items():
        index_merged, index_deleted = info_item

        my_dict[index_merged].text = info_text
        del my_dict[index_deleted]

    my_dict = {index: value for index, (key, value) in enumerate(my_dict.items())}

    return my_dict


def find_vertical_lines_intersection(line1, line2):
    xmin1, ymin1, xmax1, ymax1 = line1
    xmin2, ymin2, xmax2, ymax2 = line2

    # Calculate the overlapping y-range
    common_y_min = max(ymin1, ymin2)
    common_y_max = min(ymax1, ymax2)

    # Check if there is a valid overlapping y-range
    if common_y_min <= common_y_max:
        intersection_range = (common_y_min, common_y_max)
        return intersection_range
    else:
        return None


def find_vertical_line_pairs(vertical_lines):
    pair_list = []
    for left_ind, vertical_line_left in enumerate(vertical_lines):
        xmin_left, ymin_left, xmax_left, ymax_left = vertical_line_left[0]
        for right_ind, vertical_line_right in enumerate(vertical_lines[left_ind + 1 :]):
            xmin_right, ymin_right, xmax_right, ymax_right = vertical_line_right[0]

            intersection_range = find_vertical_lines_intersection(
                vertical_line_left[0], vertical_line_right[0]
            )

            if intersection_range:
                pair_list.append(
                    [
                        [
                            xmin_left,
                            intersection_range[0],
                            xmax_left,
                            intersection_range[1],
                        ],
                        [
                            xmin_right,
                            intersection_range[0],
                            xmax_right,
                            intersection_range[1],
                        ],
                    ]
                )

    return pair_list


def find_horizontal_line_pairs(horizontal_lines, page_width, page_height):
    pair_list = []

    # Convert the list of lists to a numpy array
    horizontal_lines_array = np.array([line[0] for line in horizontal_lines])

    x_diffs_threshold = normalize_thresholds_in_x_axis(
        threshold=10, page_width=page_width
    )
    y_diffs_threshold = normalize_thresholds_in_y_axis(
        threshold=10, page_height=page_height
    )
    y_min_diffs_threshold = normalize_thresholds_in_y_axis(
        threshold=7, page_height=page_height
    )
    y_max_diffs_threshold = y_min_diffs_threshold
    for left_ind, line_up in enumerate(horizontal_lines_array):
        xmin_up, ymin_up, xmax_up, ymax_up = line_up

        # Use array slicing for more concise code
        potential_matches = horizontal_lines_array[left_ind + 1 :]

        # Calculate differences between coordinates
        x_diffs = np.abs(potential_matches[:, 0] - xmin_up)
        y_diffs = np.abs(potential_matches[:, 2] - xmax_up)
        y_min_diffs = np.abs(potential_matches[:, 1] - ymin_up)
        y_max_diffs = np.abs(ymax_up - potential_matches[:, 3])

        # Use boolean indexing to filter potential matches
        valid_matches = (
            (x_diffs < x_diffs_threshold)
            & (y_diffs < y_diffs_threshold)
            & (y_min_diffs > y_min_diffs_threshold)
            & (y_max_diffs > y_max_diffs_threshold)
        )

        # Append valid pairs to the result
        pair_list.extend(
            [
                [[line_up.tolist()], [line_down.tolist()]]
                for line_down in potential_matches[valid_matches]
            ]
        )

    return pair_list


def find_horizontal_line_pairs_with_filtering(
    horizontal_lines, page_width, page_height
):
    # This function filter horizontal line pairs so works faster than find_horizontal_line_pairs
    pair_list = []

    # Convert the list of lists to a numpy array
    horizontal_lines_array = np.array([line[0] for line in horizontal_lines])

    x_diffs_threshold = normalize_thresholds_in_x_axis(
        threshold=10, page_width=page_width
    )
    y_diffs_threshold = normalize_thresholds_in_y_axis(
        threshold=10, page_height=page_height
    )
    y_min_diffs_threshold = normalize_thresholds_in_y_axis(
        threshold=7, page_height=page_height
    )
    y_max_diffs_threshold = y_min_diffs_threshold
    for left_ind, line_up in enumerate(horizontal_lines_array):
        xmin_up, ymin_up, xmax_up, ymax_up = line_up

        # Use array slicing for more concise code
        potential_matches = horizontal_lines_array[left_ind + 1 :]

        # Calculate differences between coordinates
        x_diffs = np.abs(potential_matches[:, 0] - xmin_up)
        y_diffs = np.abs(potential_matches[:, 2] - xmax_up)
        y_min_diffs = np.abs(potential_matches[:, 1] - ymin_up)
        y_max_diffs = np.abs(ymax_up - potential_matches[:, 3])

        # Use boolean indexing to filter potential matches
        valid_matches = (
            (x_diffs < x_diffs_threshold)
            & (y_diffs < y_diffs_threshold)
            & (y_min_diffs > y_min_diffs_threshold)
            & (y_max_diffs > y_max_diffs_threshold)
        )

        # Append valid pairs to the result
        # pair_list.extend([[[line_up.tolist()], [line_down.tolist()]] for line_down in potential_matches[valid_matches]])
        sorted_matches = potential_matches[valid_matches][
            np.argsort(potential_matches[valid_matches][:, 1])
        ]
        if len(sorted_matches) > 0:
            sorted_matches = sorted_matches[0]
            # Append valid pairs to the result
            pair_list.extend([[[line_up], [sorted_matches]]])
    return pair_list


def find_bbox_from_lines(
    left_vertical,
    horizontal_line_1,
    right_vertical,
    horizontal_line_2,
    page_width,
    page_height,
):
    xmin_left_vertical, ymin_left_vertical, xmax_left_vertical, ymax_left_vertical = (
        left_vertical
    )
    (
        xmin_upper_horizontal,
        ymin_upper_horizontal,
        xmax_upper_horizontal,
        ymax_upper_horizontal,
    ) = horizontal_line_1[0]
    (
        xmin_right_vertical,
        ymin_right_vertical,
        xmax_right_vertical,
        ymax_right_vertical,
    ) = right_vertical
    (
        xmin_lower_horizontal,
        ymin_lower_horizontal,
        xmax_lower_horizontal,
        ymax_lower_horizontal,
    ) = horizontal_line_2[0]

    x_min_horizontal_threshold = normalize_thresholds_in_x_axis(
        threshold=10, page_width=page_width
    )
    x_min_vertical_threshold = normalize_thresholds_in_x_axis(
        threshold=7, page_width=page_width
    )
    y_min_vertical_threshold = normalize_thresholds_in_y_axis(
        threshold=7, page_height=page_height
    )

    if (
        abs(xmin_upper_horizontal - xmin_lower_horizontal) < x_min_horizontal_threshold
        and abs(xmax_upper_horizontal - xmax_lower_horizontal)
        < x_min_horizontal_threshold
        and abs(xmin_left_vertical - xmin_lower_horizontal) <= x_min_vertical_threshold
        and abs(xmin_right_vertical - xmax_lower_horizontal) <= x_min_vertical_threshold
        and (
            (
                abs(ymin_left_vertical - ymin_upper_horizontal)
                <= y_min_vertical_threshold
                and ymin_upper_horizontal <= ymax_left_vertical
            )
            or ymin_left_vertical <= ymin_upper_horizontal <= ymax_left_vertical
        )
        and (
            (
                abs(ymax_left_vertical - ymin_lower_horizontal)
                <= y_min_vertical_threshold
                and ymin_left_vertical <= ymin_lower_horizontal
            )
            or ymin_left_vertical <= ymin_lower_horizontal <= ymax_left_vertical
        )
    ):
        # Calculate the bounding box coordinates
        bbox_x1 = min(
            xmin_left_vertical,
            xmax_left_vertical,
            xmin_right_vertical,
            xmax_right_vertical,
        )
        bbox_y1 = min(
            ymin_upper_horizontal,
            ymax_upper_horizontal,
            ymin_lower_horizontal,
            ymax_lower_horizontal,
        )
        bbox_x2 = max(
            xmin_left_vertical,
            xmax_left_vertical,
            xmin_right_vertical,
            xmax_right_vertical,
        )
        bbox_y2 = max(
            ymin_upper_horizontal,
            ymax_upper_horizontal,
            ymin_lower_horizontal,
            ymax_lower_horizontal,
        )

        return (bbox_x1, bbox_y1, bbox_x2, bbox_y2)
    else:
        return None


def find_smallest_bboxes(bboxes):
    result_bboxes = []

    for ind, bbox_bigger in enumerate(bboxes):
        xmin_box_bigger, ymin_box_bigger, xmax_box_bigger, ymax_box_bigger = bbox_bigger

        is_smallest = True

        for bbox_smaller in bboxes:
            xmin_box_smaller, ymin_box_smaller, xmax_box_smaller, ymax_box_smaller = (
                bbox_smaller
            )

            if (
                bbox_bigger != bbox_smaller
                and xmin_box_smaller >= xmin_box_bigger
                and xmax_box_smaller <= xmax_box_bigger
                and ymin_box_smaller >= ymin_box_bigger
                and ymax_box_smaller <= ymax_box_bigger
            ):
                is_smallest = False
                break

        if is_smallest:
            result_bboxes.append(bbox_bigger)

    return result_bboxes


def merge_neighbor_bboxes(bboxes, page_width, page_height):
    merged_bboxes = []
    new_bboxes = []
    # Sort the bounding boxes based on ymin
    sorted_bboxes = sorted(bboxes, key=lambda bbox: bbox[1])

    x_threshold = normalize_thresholds_in_x_axis(threshold=5, page_width=page_width)
    y_threshold = normalize_thresholds_in_y_axis(threshold=5, page_height=page_height)

    removed_bboxes = []
    i = 0
    while i < len(sorted_bboxes) - 1:
        bbox_upper = sorted_bboxes[i]
        found = False
        xmin_box_upper, ymin_box_upper, xmax_box_upper, ymax_box_upper = bbox_upper

        for ind, bbox_lower in enumerate(sorted_bboxes[i + 1 :]):
            xmin_box_lower, ymin_box_lower, xmax_box_lower, ymax_box_lower = bbox_lower
            # Check the conditions for merging
            if (
                abs(xmin_box_upper - xmin_box_lower) < x_threshold
                and abs(xmax_box_upper - xmax_box_lower) < x_threshold
                and abs(ymax_box_upper - ymin_box_lower) < y_threshold
            ):
                # Merge the bounding boxes
                merged_bbox = (
                    min(xmin_box_upper, xmin_box_lower),
                    min(ymin_box_upper, ymin_box_lower),
                    max(xmax_box_upper, xmax_box_lower),
                    max(ymax_box_upper, ymax_box_lower),
                )
                new_bboxes.append(sorted_bboxes[i])
                new_bboxes.append(bbox_lower)
                new_bboxes.append(merged_bbox)
                removed_bboxes.append(sorted_bboxes[i])
                # Replace the original bounding boxes with the merged one
                sorted_bboxes[i] = merged_bbox
                # Remove the merged bounding box from the list
                removed_bboxes.append(sorted_bboxes.pop(ind + i + 1))
                sorted_bboxes = sorted(sorted_bboxes, key=lambda bbox: bbox[1])
                found = True
                break
        if found:
            i = 0
        else:
            i += 1

    return new_bboxes + sorted_bboxes


def expand_bboxes(bboxes, expansion_value_for_y=7, expansion_value_for_x=7):
    expanded_bboxes = []
    for bbox in bboxes:
        xmin, ymin, xmax, ymax = bbox

        # Expand each coordinate by the specified value
        expanded_bbox = (
            xmin - expansion_value_for_x,
            ymin - expansion_value_for_y,
            xmax + expansion_value_for_x,
            ymax + expansion_value_for_y,
        )

        expanded_bboxes.append(expanded_bbox)

    return expanded_bboxes


def merge_coordinates(coord1, coord2):
    xmin1, ymin1, xmax1, ymax1 = coord1
    xmin2, ymin2, xmax2, ymax2 = coord2

    if xmax1 == xmin2:
        # Koordinatları birleştir
        merged_coord = [xmin1, ymin1, xmax2, ymax1]
        return merged_coord
    else:
        # Birleştirme gerekmiyor
        return None


def merge_overlapping_coordinates(coord_list):
    merged_list = []

    for i in range(len(coord_list)):
        current_coord = coord_list[i]

        for j in range(i + 1, len(coord_list)):
            next_coord = coord_list[j]
            merged_coord = merge_coordinates(current_coord, next_coord)

            if merged_coord:
                merged_list.append(merged_coord)

    return merged_list


def arrange_horizontal_lines_in_same_y_axis(horizontal_line_dict):
    for key, horizontal_lines in horizontal_line_dict.items():
        horizontal_lines = sorted(horizontal_lines, key=lambda x: (x[0][0], x[0][2]))
        coordinates = [coord[0] for coord in horizontal_lines]
        merged_coordinates = merge_overlapping_coordinates(coordinates)

        for coord in merged_coordinates:
            if not any(np.array_equal(coord, sublist) for sublist in coordinates):
                horizontal_lines.append([coord])

        horizontal_lines = sorted(horizontal_lines, key=lambda x: (x[0][1], x[0][0]))
        horizontal_line_dict[key] = horizontal_lines

    return horizontal_line_dict


def arrange_horizontal_line_coordinates(
    horizontal_lines, vertical_line_pairs, page_width, page_height
):
    new_lines = []
    horizontal_line_dict = horizontal_line_store_wrt_y_axis(
        horizontal_lines, threshold=1
    )
    horizontal_line_dict = arrange_horizontal_lines_in_same_y_axis(horizontal_line_dict)

    x_threshold_1 = normalize_thresholds_in_x_axis(threshold=7, page_width=page_width)
    y_threshold_1 = normalize_thresholds_in_y_axis(
        threshold=10, page_height=page_height
    )
    y_threshold_2 = normalize_thresholds_in_y_axis(
        threshold=20, page_height=page_height
    )
    y_threshold_3 = normalize_thresholds_in_y_axis(threshold=7, page_height=page_height)

    for vertical_line_pair in vertical_line_pairs:
        left_vertical, right_vertical = vertical_line_pair
        (
            xmin_left_vertical,
            ymin_left_vertical,
            xmax_left_vertical,
            ymax_left_vertical,
        ) = left_vertical
        (
            xmin_right_vertical,
            ymin_right_vertical,
            xmax_right_vertical,
            ymax_right_vertical,
        ) = right_vertical

        for horizontal_line_list in horizontal_line_dict.values():
            candidates = []
            if len(horizontal_line_list) > 1:
                for line in horizontal_line_list:
                    (
                        xmin_horizontal,
                        ymin_horizontal,
                        xmax_horizontal,
                        ymax_horizontal,
                    ) = line[0]

                    if ymin_horizontal + y_threshold_1 < ymin_left_vertical:
                        continue
                    elif ymin_horizontal > ymax_left_vertical + y_threshold_2:
                        break

                    if (
                        abs(xmin_left_vertical - xmin_horizontal) <= x_threshold_1
                        or abs(xmin_right_vertical - xmax_horizontal) <= x_threshold_1
                        and (
                            (
                                abs(ymin_left_vertical - ymin_horizontal)
                                <= y_threshold_3
                                and abs(ymax_left_vertical - ymin_horizontal)
                                <= y_threshold_3
                            )
                            or ymin_left_vertical
                            <= ymin_horizontal
                            <= ymax_left_vertical
                        )
                    ):
                        candidates.append(line)

                if len(candidates) > 1:
                    candidates = sorted(candidates, key=lambda x: (x[0][0], x[0][1]))

                    first_line = candidates[0]
                    last_line = candidates[-1]

                    left_most_x = first_line[0][0]
                    left_most_y = first_line[0][1]
                    right_most_x = last_line[0][2]

                    if (
                        abs(left_most_x - xmin_left_vertical) <= x_threshold_1
                        and abs(right_most_x - xmax_right_vertical) <= x_threshold_1
                    ):
                        new_lines.append(
                            np.asarray(
                                [
                                    xmin_left_vertical,
                                    left_most_y,
                                    xmax_right_vertical,
                                    left_most_y,
                                ]
                            ).reshape(1, 4)
                        )

    horizontal_lines = [
        item for sublist in horizontal_line_dict.values() for item in sublist
    ]

    return filter_horizontal_lines_for_text_sorting(horizontal_lines + new_lines)


def search_bbox_v2(horizontal_pairs, vertical_pairs, page_width, page_height):
    vertical_pairs = [
        sorted(sublist, key=lambda line: line[0]) for sublist in vertical_pairs
    ]
    horizontal_pairs = [
        sorted(sublist, key=lambda line: line[0][1]) for sublist in horizontal_pairs
    ]

    bboxes = dict()
    for vertical_line_pair in vertical_pairs:
        left_vertical, right_vertical = vertical_line_pair

        for horizontal_line_pair in horizontal_pairs:
            upper_horizontal, lower_horizontal = horizontal_line_pair
            bbox_coordinates = find_bbox_from_lines(
                left_vertical,
                upper_horizontal,
                right_vertical,
                lower_horizontal,
                page_width,
                page_height,
            )
            if bbox_coordinates != None:
                if len(bboxes) == 0:
                    bboxes[bbox_coordinates] = 0
                else:
                    # Check if bbox_coordinates is completely contained within another bbox
                    is_contained = any(
                        (
                            bbox_coordinates[0] <= xmin <= bbox_coordinates[2]
                            and bbox_coordinates[1] <= ymin <= bbox_coordinates[3]
                            and bbox_coordinates[0] <= xmax <= bbox_coordinates[2]
                            and bbox_coordinates[1] <= ymax <= bbox_coordinates[3]
                        )
                        for xmin, ymin, xmax, ymax in bboxes.keys()
                    )

                    if not is_contained:
                        bboxes[bbox_coordinates] = 0

    bboxes = list(bboxes.keys())
    bboxes = find_smallest_bboxes(bboxes)
    bboxes = merge_neighbor_bboxes(bboxes, page_width, page_height)

    return bboxes


def filter_bboxes_wtr_area(bboxes, page_width, page_height, threshold=2000000):
    threshold = normalize_page_area(
        threshold=threshold, page_width=page_width, page_height=page_height
    )
    return [
        bbox
        for bbox in bboxes
        if (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) <= threshold
    ]


def sort_text_with_indexes(my_dict, deleted_indexes, new_text):
    merged_index = deleted_indexes[0]
    deleted_indexes.pop(0)
    my_dict[merged_index].text = " ".join(new_text)

    for ind in deleted_indexes:
        del my_dict[ind]

    my_dict = {index: value for index, (key, value) in enumerate(my_dict.items())}

    return my_dict


def sort_text_inside_bboxes(
    my_dict,
    bboxes,
    page_width,
    page_height,
    expansion_value_for_x=7,
    expansion_value_for_y=7,
):
    expansion_value_for_x = normalize_thresholds_in_x_axis(
        threshold=expansion_value_for_x, page_width=page_width
    )
    expansion_value_for_y = normalize_thresholds_in_y_axis(
        threshold=expansion_value_for_y, page_height=page_height
    )
    bboxes = expand_bboxes(
        bboxes,
        expansion_value_for_x=expansion_value_for_x,
        expansion_value_for_y=expansion_value_for_y,
    )
    for ind, bbox in enumerate(bboxes):
        xmin_box, ymin_box, xmax_box, ymax_box = bbox
        deleted_indexes = []
        new_text = []
        for index, item in my_dict.items():
            xmin_text, xmax_text, ymin_text, ymax_text = (
                item.box.xmin,
                item.box.xmax,
                item.box.ymin,
                item.box.ymax,
            )
            text = item.text

            if xmin_box <= xmin_text <= xmax_box and xmin_box <= xmax_text <= xmax_box:
                if (
                    ymin_box <= ymin_text <= ymax_box
                    and ymin_box <= ymax_text <= ymax_box
                ):
                    deleted_indexes.append(index)
                    new_text.append((xmin_text, text))

        if len(deleted_indexes) > 0:
            new_text = [item[1] for item in new_text]

            my_dict = sort_text_with_indexes(my_dict, deleted_indexes, new_text)

    my_dict = {index: value for index, (key, value) in enumerate(my_dict.items())}

    return my_dict


def delete_bboxes_lines(
    horizontal_lines, vertical_lines, bboxes, page_width, page_height
):
    x_threshold = normalize_thresholds_in_x_axis(threshold=5, page_width=page_width)
    y_threshold = normalize_thresholds_in_y_axis(threshold=5, page_height=page_height)
    for bbox in bboxes:
        filtered_horizontal_lines = []
        filtered_vertical_lines = []
        xmin_box, ymin_box, xmax_box, ymax_box = bbox
        for ind, line in enumerate(horizontal_lines):
            xmin_horizontal, ymin_horizontal, xmax_horizontal, ymax_horizontal = line[0]

            if (
                abs(xmin_box - xmin_horizontal) <= x_threshold
                and abs(ymin_box - ymin_horizontal) <= y_threshold
                and abs(xmax_box - xmax_horizontal) <= x_threshold
            ) or (
                abs(xmin_box - xmin_horizontal) <= x_threshold
                and abs(ymax_box - ymin_horizontal) <= y_threshold
                and abs(xmax_box - xmax_horizontal) <= x_threshold
            ):
                # draw_img(line)
                filtered_horizontal_lines.append(ind)

        for ind, line in enumerate(vertical_lines):
            xmin_vertical, ymin_vertical, xmax_vertical, ymax_vertical = line[0]
            if (
                abs(xmin_box - xmin_vertical) <= x_threshold
                and abs(ymin_vertical - ymin_box) <= y_threshold
                and abs(ymax_box - ymax_vertical) <= y_threshold
            ) or (
                abs(xmax_box - xmin_vertical) <= x_threshold
                and abs(ymin_box - ymin_vertical) <= y_threshold
                and abs(ymax_box - ymax_vertical) <= y_threshold
            ):
                # All elements are the same, continue
                filtered_vertical_lines.append(ind)

        horizontal_lines = [
            value
            for index, value in enumerate(horizontal_lines)
            if index not in set(filtered_horizontal_lines)
        ]

        vertical_lines = [
            value
            for index, value in enumerate(vertical_lines)
            if index not in set(filtered_vertical_lines)
        ]

    return horizontal_lines, vertical_lines


def merge_vertical_bboxes(bboxes, page_width, page_height):
    x_threshold = normalize_thresholds_in_x_axis(threshold=8, page_width=page_width)
    y_threshold = normalize_thresholds_in_y_axis(threshold=8, page_height=page_height)

    def vertical_intersection(bbox1, bbox2):
        return (
            abs(bbox1[2] - bbox2[2]) < x_threshold
            and abs(bbox1[0] - bbox2[0]) < x_threshold
            and abs(bbox1[3] - bbox2[1]) < y_threshold
        )

    merged_bboxes = list(bboxes)  # Create a copy of the original list
    merged = True
    while merged:
        merged = False
        for i in range(len(merged_bboxes)):
            for j in range(i + 1, len(merged_bboxes)):
                bbox_up = merged_bboxes[i]
                bbox_down = merged_bboxes[j]

                if vertical_intersection(bbox_up, bbox_down):
                    # Merge the bounding boxes
                    merged_bbox = (
                        min(bbox_up[0], bbox_down[0]),
                        min(bbox_up[1], bbox_down[1]),
                        max(bbox_up[2], bbox_down[2]),
                        max(bbox_up[3], bbox_down[3]),
                    )
                    # Replace the original boxes with the merged one
                    merged_bboxes[i] = merged_bbox
                    del merged_bboxes[j]
                    merged = True
                    break  # Break out of the inner loop and restart the merging process

    return merged_bboxes


def merge_open_neighbor_bboxes(sorted_bboxes, page_width, page_height):
    x_threshold = normalize_thresholds_in_x_axis(threshold=8, page_width=page_width)
    y_threshold = normalize_thresholds_in_y_axis(threshold=8, page_height=page_height)
    new_bboxes = []
    i = 0
    len_sorted_bbox = len(sorted_bboxes)
    while i < len_sorted_bbox - 1:
        bbox_left = sorted_bboxes[i]
        found = False
        xmin_box_left, ymin_box_left, xmax_box_left, ymax_box_left = bbox_left

        for ind, bbox_right in enumerate(sorted_bboxes[i + 1 :]):
            xmin_box_right, ymin_box_right, xmax_box_right, ymax_box_right = bbox_right
            # Check the conditions for merging
            if (
                abs(xmin_box_right - xmax_box_left) < x_threshold
                and abs(ymin_box_right - ymin_box_left) < y_threshold
                and abs(ymax_box_right - ymax_box_left) < y_threshold
            ):
                # Merge the bounding boxes
                merged_bbox = (
                    xmin_box_left,
                    min(ymin_box_left, ymin_box_right),
                    xmax_box_right,
                    max(ymax_box_left, ymax_box_right),
                )
                sorted_bboxes.append(merged_bbox)
                new_bboxes.append(merged_bbox)
                break

        i += 1
        len_sorted_bbox = len(sorted_bboxes)

    vertical_merge = merge_vertical_bboxes(new_bboxes, page_width, page_height)
    vertical_merge = sorted(vertical_merge, key=lambda bbox: (bbox[1], bbox[3]))

    return sorted_bboxes + vertical_merge


def find_open_bboxes(horizontal_line_pair, vertical_lines, page_width, page_height):
    vertical_lines = sorted(vertical_lines, key=lambda x: (x[0][1], x[0][0]))
    x_threshold_1 = normalize_thresholds_in_x_axis(threshold=7, page_width=page_width)
    x_threshold_2 = normalize_thresholds_in_x_axis(threshold=5, page_width=page_width)
    y_threshold_1 = normalize_thresholds_in_y_axis(threshold=7, page_height=page_height)
    y_threshold_2 = normalize_thresholds_in_y_axis(threshold=5, page_height=page_height)
    checked_bboxes = []
    for ind, vertical_line_left in enumerate(vertical_lines):
        [
            [
                xmin_upper_horizontal,
                ymin_upper_horizontal,
                xmax_upper_horizontal,
                ymax_upper_horizontal,
            ]
        ] = horizontal_line_pair[0]
        [
            [
                xmin_lower_horizontal,
                ymin_lower_horizontal,
                xmax_lower_horizontal,
                ymax_lower_horizontal,
            ]
        ] = horizontal_line_pair[1]
        [
            xmin_left_vertical,
            ymin_left_vertical,
            xmax_left_vertical,
            ymax_left_vertical,
        ] = vertical_line_left[0]

        if (
            abs(xmin_left_vertical - xmin_lower_horizontal) <= x_threshold_1
            and (
                (
                    abs(ymin_left_vertical - ymin_upper_horizontal) <= y_threshold_1
                    and ymin_upper_horizontal <= ymax_left_vertical
                )
                or ymin_left_vertical <= ymin_upper_horizontal <= ymax_left_vertical
            )
            and (
                (
                    abs(ymax_left_vertical - ymin_lower_horizontal) <= y_threshold_1
                    and ymin_left_vertical <= ymin_lower_horizontal
                )
                or ymin_left_vertical <= ymin_lower_horizontal <= ymax_left_vertical
            )
        ):
            found = False
            for vertical_line_right in vertical_lines[ind + 1 :]:
                [
                    xmin_right_vertical,
                    ymin_right_vertical,
                    xmax_right_vertical,
                    ymax_right_vertical,
                ] = vertical_line_right[0]

                bbox_x1 = min(xmin_upper_horizontal, xmin_lower_horizontal)
                bbox_y1 = ymin_upper_horizontal
                bbox_x2 = max(xmax_upper_horizontal, xmax_lower_horizontal)
                bbox_y2 = ymax_lower_horizontal
                bbox_coordinates = (bbox_x1, bbox_y1, bbox_x2, bbox_y2)

                if (
                    abs(xmin_right_vertical - xmax_lower_horizontal) <= x_threshold_1
                    and (
                        (
                            abs(ymin_right_vertical - ymin_upper_horizontal)
                            <= y_threshold_1
                            and ymin_upper_horizontal <= ymax_right_vertical
                        )
                        or ymin_right_vertical
                        <= ymin_upper_horizontal
                        <= ymax_right_vertical
                    )
                    and (
                        (
                            abs(ymax_right_vertical - ymin_lower_horizontal)
                            <= y_threshold_1
                            and ymin_right_vertical <= ymin_lower_horizontal
                        )
                        or ymin_right_vertical
                        <= ymin_lower_horizontal
                        <= ymax_right_vertical
                    )
                ):
                    found = True
                    checked_bboxes.append(bbox_coordinates)
                    break

            if not found:
                contains_target = any(
                    abs(bbox_coordinates[0] - xmin) <= x_threshold_2
                    and abs(bbox_coordinates[1] - ymin) <= y_threshold_2
                    and abs(bbox_coordinates[2] - xmax) <= x_threshold_2
                    and abs(bbox_coordinates[3] - ymax) <= y_threshold_2
                    for xmin, ymin, xmax, ymax in checked_bboxes
                )

                if not contains_target:
                    # Calculate the bounding box coordinates
                    bbox_x1 = min(xmin_upper_horizontal, xmin_lower_horizontal)
                    bbox_y1 = ymin_upper_horizontal
                    bbox_x2 = max(xmax_upper_horizontal, xmax_lower_horizontal)
                    bbox_y2 = ymax_lower_horizontal

                    return (bbox_x1, bbox_y1, bbox_x2, bbox_y2)

        if (
            abs(xmin_left_vertical - xmax_lower_horizontal) <= x_threshold_1
            and (
                (
                    abs(ymin_left_vertical - ymin_upper_horizontal) <= y_threshold_1
                    and ymin_upper_horizontal <= ymax_left_vertical
                )
                or ymin_left_vertical <= ymin_upper_horizontal <= ymax_left_vertical
            )
            and (
                (
                    abs(ymax_left_vertical - ymin_lower_horizontal) <= y_threshold_1
                    and ymin_left_vertical <= ymin_lower_horizontal
                )
                or ymin_left_vertical <= ymin_lower_horizontal <= ymax_left_vertical
            )
        ):
            found = False
            for vertical_line_right in vertical_lines[:ind]:
                [
                    xmin_right_vertical,
                    ymin_right_vertical,
                    xmax_right_vertical,
                    ymax_right_vertical,
                ] = vertical_line_right[0]

                bbox_x1 = min(xmin_upper_horizontal, xmin_lower_horizontal)
                bbox_y1 = ymin_upper_horizontal
                bbox_x2 = max(xmax_upper_horizontal, xmax_lower_horizontal)
                bbox_y2 = ymax_lower_horizontal
                bbox_coordinates = (bbox_x1, bbox_y1, bbox_x2, bbox_y2)

                if (
                    abs(xmin_right_vertical - xmin_lower_horizontal) <= x_threshold_1
                    and (
                        (
                            abs(ymin_right_vertical - ymin_upper_horizontal)
                            <= y_threshold_1
                            and ymin_upper_horizontal <= ymax_right_vertical
                        )
                        or ymin_right_vertical
                        <= ymin_upper_horizontal
                        <= ymax_right_vertical
                    )
                    and (
                        (
                            abs(ymax_right_vertical - ymin_lower_horizontal)
                            <= y_threshold_1
                            and ymin_right_vertical <= ymin_lower_horizontal
                        )
                        or ymin_right_vertical
                        <= ymin_lower_horizontal
                        <= ymax_right_vertical
                    )
                ):
                    found = True
                    checked_bboxes.append(bbox_coordinates)
                    break

            if not found:
                contains_target = any(
                    abs(bbox_coordinates[0] - xmin) <= x_threshold_2
                    and abs(bbox_coordinates[1] - ymin) <= y_threshold_2
                    and abs(bbox_coordinates[2] - xmax) <= x_threshold_2
                    and abs(bbox_coordinates[3] - ymax) <= y_threshold_2
                    for xmin, ymin, xmax, ymax in checked_bboxes
                )

                if not contains_target:
                    # Calculate the bounding box coordinates
                    bbox_x1 = min(xmin_upper_horizontal, xmin_lower_horizontal)
                    bbox_y1 = ymin_upper_horizontal
                    bbox_x2 = max(xmax_upper_horizontal, xmax_lower_horizontal)
                    bbox_y2 = ymax_lower_horizontal

                    return (bbox_x1, bbox_y1, bbox_x2, bbox_y2)

    return None


def calculate_bbox_area(upper_bbox, lower_bbox):
    # Extracting coordinates from the upper and lower lines
    xmin_upper, ymin_upper, xmax_upper, ymax_upper = upper_bbox[0]
    xmin_lower, ymin_lower, xmax_lower, ymax_lower = lower_bbox[0]

    # Calculating the area between upper and lower lines
    area = (xmax_upper - xmin_upper) * (ymax_lower - ymin_upper)
    return area


def search_open_bboxes(vertical_lines, horizontal_pairs, page_width, page_height):
    x_threshold_1 = normalize_thresholds_in_x_axis(threshold=5, page_width=page_width)
    y_threshold_1 = normalize_thresholds_in_y_axis(threshold=5, page_height=page_height)
    bboxes = []
    for ind, horizontal_line_pair in enumerate(horizontal_pairs):
        bbox_coordinates = find_open_bboxes(
            horizontal_line_pair, vertical_lines, page_width, page_height
        )
        if bbox_coordinates:
            contains_target = any(
                abs(bbox_coordinates[0] - xmin) <= x_threshold_1
                and abs(bbox_coordinates[1] - ymin) <= y_threshold_1
                and abs(bbox_coordinates[2] - xmax) <= x_threshold_1
                for xmin, ymin, xmax, ymax in bboxes
            )

            if not contains_target:
                bboxes.append(bbox_coordinates)

    # bboxes = sorted(bboxes, key=lambda bbox: (bbox[1], bbox[2]))
    bboxes = sorted(
        bboxes,
        key=lambda bbox: (bbox[1], bbox[2], (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])),
    )
    # for box in bboxes:
    #    draw_bboxes([box])

    bboxes = merge_open_neighbor_bboxes(bboxes, page_width, page_height)
    return bboxes


def search_parallel_range(
    parallel_horizontal_lines, page_width, page_height, threshold=100
):
    new_lines = []
    for line_list in parallel_horizontal_lines:
        if len(line_list) > 1:
            left = 0
            ind = 0

            while ind < len(line_list) - 1:
                xmin_upper, ymin_upper, xmax_upper, ymax_upper = line_list[ind][0]
                xmin_lower, ymin_lower, xmax_lower, ymax_lower = line_list[ind + 1][0]

                if abs(ymax_upper - ymax_lower) < normalize_thresholds_in_y_axis(
                    threshold=390, page_height=page_height
                ):
                    ind += 1

                else:
                    new_lines.append(line_list[left : ind + 1])
                    ind += 1
                    left = ind

            new_lines.append(line_list[left : ind + 1])
            ind += 1
            left = ind

    return new_lines


def arrange_horizontal_parallel_line_coordinates(
    horizontal_lines, page_width, page_height
):
    new_list = []
    while len(horizontal_lines) > 0:
        upper_line = horizontal_lines[0]
        xmin_upper, ymin_upper, xmax_upper, ymax_upper = upper_line[0]

        found = False
        candidates = []
        candidate_inds = []
        candidates.append(upper_line)
        candidate_inds.append(0)
        for ind, lower_line in enumerate(horizontal_lines):
            xmin_lower, ymin_lower, xmax_lower, ymax_lower = lower_line[0]

            if (
                abs(xmin_upper - xmin_lower) <= 7
                and abs(xmax_upper - xmax_lower) <= 7
                and abs(ymax_upper - ymax_lower) > 10
            ):
                found = True
                candidates.append(lower_line)
                candidate_inds.append(ind)

        if found:
            xmin_values = [coord[0][0] for coord in candidates]
            xmax_values = [coord[0][2] for coord in candidates]
            mean_xmin = int(np.mean(xmin_values))
            mean_xmax = int(np.mean(xmax_values))

            candidates = [
                [[mean_xmin, coord[0][1], mean_xmax, coord[0][3]]]
                for coord in candidates
            ]
            new_list.append(candidates)

            horizontal_lines = [
                value
                for index, value in enumerate(horizontal_lines)
                if index not in candidate_inds
            ]

        else:
            new_list.append(candidates)
            horizontal_lines.pop(0)

    new_list = search_parallel_range(new_list, page_width, page_height, threshold=100)

    return new_list


def create_bbox_for_parallel_lines(parallel_horizontal_lines):
    parallel_horizontal_patterns = dict()
    for patterns in parallel_horizontal_lines:
        if len(patterns) > 1:
            upper_most = patterns[0][0]
            lowest_most = patterns[-1][0]

            bbox = (upper_most[0], upper_most[1], upper_most[2], lowest_most[3])
            parallel_horizontal_patterns[bbox] = patterns

    return parallel_horizontal_patterns


def search_parallel_line_paterns(
    horizontal_lines, vertical_lines, page_width, page_height
):
    horizontal_lines = sorted(horizontal_lines, key=lambda x: (x[0][1], x[0][0]))
    parallel_horizontal_lines = arrange_horizontal_parallel_line_coordinates(
        horizontal_lines, page_width, page_height
    )
    parallel_horizontal_lines = create_bbox_for_parallel_lines(
        parallel_horizontal_lines
    )

    return parallel_horizontal_lines


def eliminate_parallel_line_bboxes(
    parallel_horizontal_lines, my_dict, page_width, page_height
):
    x_threshold_1 = normalize_thresholds_in_x_axis(threshold=10, page_width=page_width)
    bbox_list = list(parallel_horizontal_lines.keys())
    bbox_list = sorted(bbox_list, key=lambda x: (x[1], x[0]))
    eliminated_box = set()
    for ind_item, item in my_dict.items():
        xmin_text, xmax_text, ymin_text, ymax_text = (
            item.box.xmin,
            item.box.xmax,
            item.box.ymin,
            item.box.ymax,
        )
        item_text = item.text

        found = False
        for ind, box in enumerate(bbox_list):
            xmin_box, ymin_box, xmax_box, ymax_box = box

            if ymin_box <= ymin_text <= ymax_box and ymin_box <= ymax_text <= ymax_box:
                # if xmin_text > xmax_box or xmin_text + 10 < xmin_box:
                if xmin_text + x_threshold_1 < xmin_box and (
                    xmax_text > xmax_box or xmin_box <= xmax_text <= xmax_box
                ):
                    found = True
                    for right_box in bbox_list:
                        (
                            xmin_right_box,
                            ymin_right_box,
                            xmax_right_box,
                            ymax_right_box,
                        ) = right_box

                        if all(a != b for a, b in zip(box, right_box)):
                            if (
                                ymin_right_box <= ymin_text <= ymax_right_box
                                and ymin_right_box <= ymax_text <= ymax_right_box
                            ):
                                if (
                                    xmin_right_box <= xmin_text <= xmax_right_box
                                    and xmin_right_box <= xmax_text <= xmax_right_box
                                ):
                                    found = False
                                    break

            if found:
                eliminated_box.add(ind)

    for ind in eliminated_box:
        del parallel_horizontal_lines[bbox_list[ind]]

    parallel_horizontal_lines = {
        key: value for (key, value) in parallel_horizontal_lines.items()
    }

    return parallel_horizontal_lines


def sort_text_inside_parallel_line_bbox(bbox, my_dict, page_width, page_height):
    y_threshold_1 = normalize_thresholds_in_y_axis(
        threshold=10, page_height=page_height
    )
    xmin_box, ymin_box, xmax_box, ymax_box = bbox
    new_text = ""
    merged_index = []
    # draw_bboxes([bbox])
    for ind_item, item in my_dict.items():
        xmin_text, xmax_text, ymin_text, ymax_text = (
            item.box.xmin,
            item.box.xmax,
            item.box.ymin,
            item.box.ymax,
        )
        item_text = item.text

        if (
            (abs(ymax_text - ymax_box) < y_threshold_1 or ymax_text < ymax_box)
            and (abs(ymin_text - ymin_box) < y_threshold_1 or ymin_text > ymin_box)
            and ymax_text > ymin_box
            and ymin_text < ymax_box
        ):
            if xmin_box <= xmin_text <= xmax_text <= xmax_box:
                new_text = new_text + " " + item_text
                merged_index.append(ind_item)
    if len(merged_index) > 0:
        my_dict[merged_index[0]].text = new_text
        for index in merged_index[1:]:
            del my_dict[index]
        my_dict = {index: value for index, (key, value) in enumerate(my_dict.items())}

    return my_dict


def sort_text_between_parallel_lines(
    parallel_horizontal_lines, my_dict, page_width, page_height
):
    x_threshold_1 = normalize_thresholds_in_x_axis(threshold=15, page_width=page_width)
    y_threshold_2 = normalize_thresholds_in_y_axis(
        threshold=10, page_height=page_height
    )
    for bbox, horizontal_line_list in parallel_horizontal_lines.items():
        ind = 0
        while ind < len(horizontal_line_list) - 1:
            xmin_up, ymin_up, xmax_up, ymax_up = horizontal_line_list[ind][0]
            xmin_down, ymin_down, xmax_down, ymax_down = horizontal_line_list[ind + 1][
                0
            ]
            xmin_up -= x_threshold_1
            xmax_up += x_threshold_1

            xmin_down -= x_threshold_1
            xmax_down += x_threshold_1

            new_text = ""
            merged_index = []

            for ind_item, item in my_dict.items():
                xmin_text, xmax_text, ymin_text, ymax_text = (
                    item.box.xmin,
                    item.box.xmax,
                    item.box.ymin,
                    item.box.ymax,
                )
                item_text = item.text

                if (
                    (
                        abs(ymax_text - ymin_down) < y_threshold_2
                        or ymax_text < ymin_down
                    )
                    and (
                        abs(ymin_text - ymin_up) < y_threshold_2 or ymin_text > ymin_up
                    )
                    and ymax_text > ymin_up
                    and ymin_text < ymin_down
                ):
                    if (
                        xmin_up <= xmin_text <= xmax_text <= xmax_up
                        and xmin_down <= xmin_text <= xmax_text <= xmax_down
                    ):
                        new_text = new_text + " " + item_text
                        merged_index.append(ind_item)

            if len(merged_index) > 0:
                my_dict[merged_index[0]].text = new_text
                for index in merged_index[1:]:
                    del my_dict[index]
                my_dict = {
                    index: value for index, (key, value) in enumerate(my_dict.items())
                }

            ind += 1

        my_dict = sort_text_inside_parallel_line_bbox(
            bbox, my_dict, page_width, page_height
        )

    return my_dict


def sort_text_for_parallel_line_patterns(
    parallel_horizontal_lines, my_dict, page_width, page_height
):
    x_threshold_1 = normalize_thresholds_in_x_axis(threshold=25, page_width=page_width)
    y_threshold_1 = normalize_thresholds_in_y_axis(
        threshold=25, page_height=page_height
    )
    bbox_list = list(parallel_horizontal_lines.keys())
    for bbox in bbox_list:
        new_bbox = expand_bboxes(
            [bbox],
            expansion_value_for_x=x_threshold_1,
            expansion_value_for_y=y_threshold_1,
        )
        parallel_horizontal_lines[new_bbox[0]] = parallel_horizontal_lines[bbox]
        del parallel_horizontal_lines[bbox]

    # for box in parallel_horizontal_lines:
    #    draw_bboxes([box])

    parallel_horizontal_lines = eliminate_parallel_line_bboxes(
        parallel_horizontal_lines, my_dict, page_width, page_height
    )
    my_dict = sort_text_between_parallel_lines(
        parallel_horizontal_lines, my_dict, page_width, page_height
    )

    return my_dict


def preprocess_string(input_string):
    # Convert the string to lowercase
    lowercase_string = input_string.lower()

    # Remove leading and trailing whitespaces
    text = lowercase_string.strip()

    # Replace new lines with a space
    text = text.replace("\n", " ")

    text = text.replace("\t", " ")

    # Replace multiple whitespaces with a single space
    text = re.sub(r"\s+", " ", text)

    # Remove punctuation
    without_punctuation = text.translate(str.maketrans("", "", string.punctuation))

    return without_punctuation


def arrange_x_coordinates_of_horizontal_lines(horizontal_lines):
    horizontal_line_dict = horizontal_line_store_wrt_y_axis(horizontal_lines)
    new_lines = []

    for horizontal_line_list in horizontal_line_dict.values():
        horizontal_line_list = sorted(
            horizontal_line_list, key=lambda x: (x[0][0], x[0][1])
        )
        for ind, line_1 in enumerate(horizontal_line_list):
            # draw_img(line_1)
            xmin_1, ymin_1, xmax_1, ymax_1 = line_1[0]
            found = False
            deleted_inds = []
            for ind_2, line_2 in enumerate(new_lines):
                xmin_2, ymin_2, xmax_2, ymax_2 = line_2[0]
                if abs(xmax_2 - xmin_1) <= 20:
                    found = True
                    if any(np.array_equal(line_2, item) for item in new_lines):
                        deleted_inds.append(
                            next(
                                i
                                for i, line in enumerate(new_lines)
                                if np.array_equal(line, line_2)
                            )
                        )
                    if any(np.array_equal(line_1, item) for item in new_lines):
                        deleted_inds.append(
                            next(
                                i
                                for i, line in enumerate(new_lines)
                                if np.array_equal(line, line_1)
                            )
                        )
                    break

            if not found:
                new_lines.append(
                    np.asarray(
                        [int(xmin_1), int(ymin_1), int(xmax_1), int(ymax_1)]
                    ).reshape(1, 4)
                )

            if found:
                new_lines.append(
                    np.asarray(
                        [
                            int(xmin_2),
                            int(np.mean([ymin_1, ymin_2])),
                            int(xmax_1),
                            int(np.mean([ymin_1, ymin_2])),
                        ]
                    ).reshape(1, 4)
                )
                new_lines = [
                    element
                    for i, element in enumerate(new_lines)
                    if i not in deleted_inds
                ]

    return new_lines


def find_bbox_on_line(line, bboxes, item, page_width, page_height):
    y_threshold_1 = normalize_thresholds_in_y_axis(threshold=7, page_height=page_height)
    xmin_text, xmax_text, ymin_text, ymax_text = (
        item.box.xmin,
        item.box.xmax,
        item.box.ymin,
        item.box.ymax,
    )
    xmin_line, ymin_line, xmax_line, ymax_line = line[0]
    for bbox in bboxes:
        xmin_box, ymin_box, xmax_box, ymax_box = bbox

        if (
            xmin_line <= xmin_box <= xmax_box <= xmax_line
            and abs(ymax_box - ymax_line) < y_threshold_1
        ):
            if (
                xmin_box <= xmin_text <= xmax_text <= xmax_box
                and ymin_box <= ymin_text <= ymax_text <= ymax_box
            ):
                return True

    return False


def sort_down_and_up_items(candidates_up, candidates_down, ind_up, ind_down):
    new_candidates_up = {}
    new_candidates_down = {}
    copy_down = candidates_down.copy()
    copy_up = candidates_up.copy()
    copy_ind_up = ind_up.copy()
    copy_ind_down = ind_down.copy()
    if len(copy_down) >= len(copy_up):
        for ind_up, item_up in enumerate(copy_up):
            text_up, x_coord_up = item_up
            sorting_array = []
            for ind, item_down in enumerate(copy_down):
                text_down, x_coord_down = item_down
                sorting_array.append((abs(x_coord_up - x_coord_down), text_down, ind))

            sorting_array = sorted(sorting_array, key=lambda x: x[0])
            new_candidates_up[x_coord_up] = [
                (
                    text_up,
                    sorting_array[0][1],
                    copy_ind_up[ind_up],
                    copy_ind_down[sorting_array[0][2]],
                )
            ]
            del copy_ind_down[sorting_array[0][2]]
            del copy_down[sorting_array[0][2]]

        for ind, item_down in enumerate(copy_down):
            text_down, x_coord_down = item_down
            new_candidates_up[x_coord_down] = [
                (" ", text_down, copy_ind_down[ind], copy_ind_down[ind])
            ]

        new_candidates_up = dict(sorted(new_candidates_up.items()))
        copy_down = []
        copy_up = []
        copy_ind_up = []
        copy_ind_down = []
        for key, value in new_candidates_up.items():
            text_up, text_down, inds_up, inds_down = value[0]
            if inds_up != None:
                copy_up.append(text_up)
                copy_ind_up.append(inds_up)
            if inds_down != None:
                copy_down.append(text_down)
                copy_ind_down.append(inds_down)

        return copy_up, copy_ind_up, copy_down, copy_ind_down

    else:
        for index_down, item_down in enumerate(candidates_down):
            text_down, x_coord_down = item_down
            sorting_array = []
            for ind, item_up in enumerate(candidates_up):
                text_up, x_coord_up = item_up
                sorting_array.append((abs(x_coord_up - x_coord_up), text_up, ind))

            sorting_array = sorted(sorting_array, key=lambda x: x[0])
            new_candidates_down[x_coord_down] = [
                (
                    text_down,
                    sorting_array[0][1],
                    ind_down[index_down],
                    ind_up[sorting_array[0][2]],
                )
            ]
            del ind_up[sorting_array[0][2]]
            del candidates_up[sorting_array[0][2]]

        for ind, item_up in enumerate(candidates_up):
            text_up, x_coord_up = item_up
            new_candidates_down[x_coord_up] = [(" ", text_up, ind_up[ind], ind_up[ind])]

        new_candidates_down = dict(sorted(new_candidates_down.items()))
        copy_down = []
        copy_up = []
        copy_ind_up = []
        copy_ind_down = []

        for key, value in new_candidates_down.items():
            text_down, text_up, inds_down, inds_up = value[0]
            if inds_up != None:
                copy_up.append(text_up)
                copy_ind_up.append(inds_up)
            if inds_down != None:
                copy_down.append(text_down)
                copy_ind_down.append(inds_down)

        return copy_up, copy_ind_up, copy_down, copy_ind_down


def merge_close_horizontal_lines(data, page_width):
    if len(data) < 2:
        return data
    # Convert data to a more usable format
    data = [item[0] for item in data]
    data = sorted(data, key=lambda x: x[0])
    # Combine lists where abs(xmin - xmax) < 10 for consecutive lists
    combined_data = []
    index = 0
    line1 = data[0]
    while index < len(data) - 1:
        line2 = data[index + 1]
        line1_xmin, line1_ymin, line1_xmax, line1_ymax = line1
        line2_xmin, line2_ymin, line2_xmax, line2_ymax = line2
        if (
            abs(line1_xmax - line2_xmin)
            < normalize_thresholds_in_x_axis(threshold=10, page_width=page_width)
            or line1_xmin <= line2_xmin <= line1_xmax <= line2_xmax
        ):
            line1 = [line1_xmin, line1_ymin, line2_xmax, line1_ymin]
            index += 1
            combined_data.append([line1])
            if len(combined_data) > 1:
                combined_data.pop(len(combined_data) - 2)
        elif line1_xmin <= line2_xmin <= line2_xmax <= line1_xmax:
            line1 = [line1_xmin, line1_ymin, line1_xmax, line1_ymax]
            index += 1
            combined_data.append([line1])
            if len(combined_data) > 1:
                combined_data.pop(len(combined_data) - 2)
        else:
            combined_data.append([line1])
            combined_data.append([line2])
            index += 1
            line1 = data[index]
            if len(combined_data) > 2:
                combined_data.pop(len(combined_data) - 2)

    return combined_data


def key_value_pair_horizontal_line_order(
    horizontal_lines, my_dict, page_width, page_height
):
    y_up, y_bottom = None, None
    for key, info in my_dict.items():
        if preprocess_string("Other Broker Firm") in preprocess_string(info.text):
            y_up, y_bottom = info.box.ymin, info.box.ymax
            break
    if y_up is None or y_bottom is None:
        return horizontal_lines

    y_up -= normalize_thresholds_in_y_axis(threshold=15, page_height=page_height)
    y_bottom += normalize_thresholds_in_y_axis(threshold=15, page_height=page_height)

    possible_keys = ["Other Broker Firm", "License No", "Listing Broker Firm"]
    keys_coordinates = {}
    for key, info in my_dict.items():
        for possible_key in possible_keys:
            if preprocess_string(possible_key) in preprocess_string(info.text):
                text_up, text_bottom = info.box.ymin, info.box.ymax
                if y_up <= text_up <= text_bottom <= y_bottom:
                    keys_coordinates[info.box.xmin] = info
                    break
        if len(keys_coordinates) == 4:
            break

    if len(keys_coordinates) != 4:
        return horizontal_lines

    sorted_dict = dict(sorted(keys_coordinates.items()))
    sorted_values = list(sorted_dict.values())
    left_line_xmin = sorted_values[0].box.xmin
    left_line_xmax = sorted_values[1].box.xmax
    right_line_xmin = sorted_values[2].box.xmin
    right_line_xmax = sorted_values[3].box.xmax

    horizontal_line_dict = horizontal_line_store_wrt_y_axis(
        horizontal_lines,
        threshold=normalize_thresholds_in_y_axis(threshold=5, page_height=page_height),
    )
    new_horizontal_lines = []
    for keys, lines in horizontal_line_dict.items():
        horizontal_line_dict[keys] = merge_close_horizontal_lines(lines, page_width)
        right_found = False
        left_found = False
        for line in horizontal_line_dict[keys]:
            xmin, ymin, xmax, ymax = line[0]
            if left_line_xmin <= xmin <= xmax <= left_line_xmax:
                if not left_found:
                    new_horizontal_lines.append(
                        [
                            [
                                left_line_xmin
                                - normalize_thresholds_in_x_axis(
                                    threshold=20, page_width=page_width
                                ),
                                ymin,
                                left_line_xmax
                                + normalize_thresholds_in_x_axis(
                                    threshold=20, page_width=page_width
                                ),
                                ymin,
                            ]
                        ]
                    )
                    left_found = True
            elif right_line_xmin <= xmin <= xmax <= right_line_xmax:
                if not right_found:
                    new_horizontal_lines.append(
                        [
                            [
                                right_line_xmin
                                - normalize_thresholds_in_x_axis(
                                    threshold=20, page_width=page_width
                                ),
                                ymin,
                                right_line_xmax
                                + normalize_thresholds_in_x_axis(
                                    threshold=20, page_width=page_width
                                ),
                                ymin,
                            ]
                        ]
                    )
                    right_found = True
            else:
                new_horizontal_lines.append([[xmin, ymin, xmax, ymax]])
    return new_horizontal_lines


def find_key_value_pairs(horizontal_lines, bboxes, my_dict, page_width, page_height):
    x_threshold_1 = normalize_thresholds_in_x_axis(threshold=5, page_width=page_width)
    horizontal_lines = key_value_pair_horizontal_line_order(
        horizontal_lines, my_dict, page_width, page_height
    )
    horizontal_lines = filter_horizontal_lines(
        horizontal_lines, threshold=x_threshold_1
    )
    horizontal_lines = arrange_x_coordinates_of_horizontal_lines(horizontal_lines)
    horizontal_lines = filter_horizontal_lines(
        horizontal_lines, threshold=x_threshold_1
    )
    key_values = constants.KEY_VALUES_FOR_PARALLEL_LINES
    preprocessed_key_values = [preprocess_string(text) for text in key_values]

    x_threshold_2 = normalize_thresholds_in_x_axis(threshold=40, page_width=page_width)
    y_threshold_1 = normalize_thresholds_in_y_axis(
        threshold=31, page_height=page_height
    )
    y_threshold_2 = normalize_thresholds_in_y_axis(threshold=7, page_height=page_height)
    for line in horizontal_lines:
        # draw_img(line)
        xmin_line, ymin_line, xmax_line, ymax_line = line[0]
        xmin_line -= x_threshold_2
        # ymin_line -= 5
        xmax_line += x_threshold_2
        # ymax_line += 20
        new_texts_dict = dict()
        candidates_up = []
        inds_up = []
        candidates_down = []
        inds_down = []
        preprocessed_candidates_up = []
        preprocessed_candidates_down = []
        for ind_item, item in my_dict.items():
            xmin_text, xmax_text, ymin_text, ymax_text = (
                item.box.xmin,
                item.box.xmax,
                item.box.ymin,
                item.box.ymax,
            )
            item_text = item.text

            if (
                xmin_line <= xmin_text <= xmax_line
                and xmin_line <= xmax_text <= xmax_line
            ):
                if (
                    0 <= ymin_line - ymax_text < y_threshold_1
                    or abs(ymax_text - ymin_line) < y_threshold_2
                    or find_bbox_on_line(line, bboxes, item, page_width, page_height)
                ):
                    candidates_up.append((item_text, (xmin_text + xmax_text) / 2))
                    inds_up.append(ind_item)
                elif (
                    0 <= ymin_text - ymin_line < y_threshold_1
                    or abs(ymin_text - ymin_line) < y_threshold_2
                ):
                    candidates_down.append((item_text, (xmin_text + xmax_text) / 2))
                    inds_down.append(ind_item)

        candidates_up, inds_up, candidates_down, inds_down = sort_down_and_up_items(
            candidates_up, candidates_down, inds_up, inds_down
        )
        if len(candidates_up) > 0:
            preprocessed_candidates_up = [
                preprocess_string(text) for text in candidates_up
            ]
        if len(candidates_down) > 0:
            preprocessed_candidates_down = [
                preprocess_string(text) for text in candidates_down
            ]

        if any(
            string2 in preprocessed_key_values
            for string2 in preprocessed_candidates_down
        ):
            new_text = ""
            merged_ind = -999
            for ind, item in enumerate(candidates_down):
                if ind < len(candidates_up):
                    new_text = item + ": " + candidates_up[ind]
                    merged_ind = inds_up[ind]
                    deleted_ind = inds_down[ind]

                    new_texts_dict[(merged_ind, deleted_ind)] = new_text

                else:
                    if len(inds_up) > 0:
                        merged_ind = inds_up[-1]
                    else:
                        merged_ind = inds_down[0]
                    new_text = new_text + " " + item
                    deleted_ind = inds_down[ind]
                    new_texts_dict[(merged_ind, deleted_ind)] = new_text

            if len(candidates_up) > len(candidates_down):
                for ind, item in enumerate(candidates_up[len(candidates_down) :]):
                    new_text = new_text + " " + item
                    deleted_ind = inds_up[len(candidates_down) :][ind]
                    new_texts_dict[(merged_ind, deleted_ind)] = new_text

        elif any(
            string2 in preprocessed_key_values for string2 in preprocessed_candidates_up
        ):
            new_text = ""
            merged_ind = -999
            for ind, item in enumerate(candidates_up):
                if ind < len(candidates_down):
                    new_text = item + ": " + candidates_down[ind]
                    merged_ind = inds_down[ind]
                    deleted_ind = inds_up[ind]

                    new_texts_dict[(merged_ind, deleted_ind)] = new_text

                else:
                    if len(inds_down) > 0:
                        merged_ind = inds_down[-1]
                    else:
                        merged_ind = inds_up[0]
                    new_text = new_text + " " + item
                    deleted_ind = inds_up[ind]
                    new_texts_dict[(merged_ind, deleted_ind)] = new_text

            if len(candidates_down) > len(candidates_up):
                for ind, item in enumerate(candidates_down[len(candidates_up) :]):
                    new_text = new_text + " " + item
                    deleted_ind = inds_down[len(candidates_up) :][ind]
                    new_texts_dict[(merged_ind, deleted_ind)] = new_text

        for inds, texts in new_texts_dict.items():
            merged_ind, deleted_ind = inds
            if merged_ind != deleted_ind:
                my_dict[merged_ind].text = texts
                del my_dict[deleted_ind]

    my_dict = {index: value for index, (key, value) in enumerate(my_dict.items())}

    return my_dict


def get_sorted_text_with_detected_lines(page, image=None):
    if (
        page.horizontal_lines
        and page.vertical_lines
        and page.non_filtered_horizontal_lines
    ):
        # Take Lines with Default Parameters and Inverse Normalize
        horizontal_lines = inverse_normalize_coordinates(
            page.horizontal_lines, page.width, page.height
        )
        vertical_lines = inverse_normalize_coordinates(
            page.vertical_lines, page.width, page.height
        )
        non_filtered_horizontal_lines = inverse_normalize_coordinates(
            page.non_filtered_horizontal_lines, page.width, page.height
        )
    elif image:
        from . import visual_line

        # Detect Lines with Default Parameters
        horizontal_lines, vertical_lines, non_filtered_horizontal_lines = (
            visual_line.detect_lines_for_text_sorting(image)
        )
        # Inverse Normalize
        horizontal_lines = inverse_normalize_coordinates(
            horizontal_lines, page.width, page.height
        )
        vertical_lines = inverse_normalize_coordinates(
            vertical_lines, page.width, page.height
        )
        non_filtered_horizontal_lines = inverse_normalize_coordinates(
            non_filtered_horizontal_lines, page.width, page.height
        )
    else:
        return ""

    text_dict = page.get_sorted_lines_dict()
    vertical_lines = sorted(vertical_lines, key=lambda x: (x[0][1], x[0][0]))
    horizontal_lines = sorted(horizontal_lines, key=lambda x: (x[0][1], x[0][0]))
    non_filtered_horizontal_lines = sorted(
        non_filtered_horizontal_lines, key=lambda x: (x[0][1], x[0][0])
    )

    vertical_pairs = find_vertical_line_pairs(vertical_lines)
    arranged_non_filtered_horizontal_lines = arrange_horizontal_line_coordinates(
        non_filtered_horizontal_lines, vertical_pairs, page.width, page.height
    )
    arranged_non_filtered_horizontal_lines = sorted(
        arranged_non_filtered_horizontal_lines, key=lambda x: (x[0][1], x[0][0])
    )
    all_horizontal_pairs = find_horizontal_line_pairs_with_filtering(
        arranged_non_filtered_horizontal_lines, page.width, page.height
    )
    # print("all_horizontal_pairs", all_horizontal_pairs)

    open_bboxes = search_open_bboxes(
        vertical_lines, all_horizontal_pairs, page.width, page.height
    )
    open_bboxes = filter_bboxes_wtr_area(
        open_bboxes, page.width, page.height, threshold=1000000
    )
    text_dict = sort_text_inside_bboxes(text_dict, open_bboxes, page.width, page.height)

    closed_bboxes = search_bbox_v2(
        all_horizontal_pairs, vertical_pairs, page.width, page.height
    )
    closed_bboxes = filter_bboxes_wtr_area(
        closed_bboxes, page.width, page.height, threshold=1000000
    )
    # print("closed_bboxes", closed_bboxes)
    text_dict = sort_text_inside_bboxes(
        text_dict, closed_bboxes, page.width, page.height
    )

    text_dict = find_key_value_pairs(
        non_filtered_horizontal_lines, closed_bboxes, text_dict, page.width, page.height
    )

    horizontal_lines, vertical_lines = delete_bboxes_lines(
        horizontal_lines, vertical_lines, closed_bboxes, page.width, page.height
    )
    horizontal_lines, vertical_lines = delete_bboxes_lines(
        horizontal_lines, vertical_lines, open_bboxes, page.width, page.height
    )

    parallel_line_bboxes = search_parallel_line_paterns(
        horizontal_lines, vertical_lines, page.width, page.height
    )
    text_dict = sort_text_for_parallel_line_patterns(
        parallel_line_bboxes, text_dict, page.width, page.height
    )

    sorted_text = ""
    for ind, item in text_dict.items():
        if ind == 0:
            sorted_text = text_dict[0].text
            continue
        sorted_text = sorted_text + "\n" + item.text

    return sorted_text
