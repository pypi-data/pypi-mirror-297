import copy
import math
import re
import string
from enum import Enum

import jsonpickle
import Levenshtein
from google.cloud import vision
from google.cloud.vision import (
    types as vision_types,  # TODO: Edited. Is this due to google vision versioning?
)

from . import constants

debug = False
IGNORED_SYMBOLS = ["|"]  # Confused with the table borders
MIN_CONFIDENCE = 0.1

BREAKS = vision.enums.TextAnnotation.DetectedBreak.BreakType


class TextLocation(Enum):
    NONE = 0
    LEFT = 1  # located at the left of the page
    RIGHT = 2  # located at the right of the page
    UP = 3  # located at the upper part of the page
    DOWN = 4  # located at the lower part of the page
    DOWN_LEFT = 5  # located at the lower left of the page
    DOWN_RIGHT = 6  # located at the lower right of the page
    UP_LEFT = 7  # located at the upper left part of the page
    UP_RIGHT = 8  # located at the upper right part of the page
    FOOTER = 9  # footer information
    HEADER = 10  # header information
    MID_LEFT = 11  # located at the lower left of the page
    MID_RIGHT = 12  # located at the lower right of the page
    BOTTOM = 13  # bottom information
    TITLE = 14  # 0.3 in the top. Otherwise title score drops down significantly


class TextOrientation(Enum):
    NONE = 0
    U2D = 1  # text is oriented from up to down
    D2U = 2  # text is oriented from down to up
    L2R = 3  # text is from left to right
    R2L = 4  # text is from right to left


class Lettering(
    Enum
):  # order is important -> key matches are looked for higher valued entries
    SINGLE = 0  # a         -> single letter
    LOWERCASE = 1  # word
    CAPITALIZED = 2  # Word
    UPPERCASE = 4  # WORD


def get_text_lettering(txt):
    regex = re.compile("[%s]" % re.escape(string.punctuation + " " + string.digits))
    text = regex.sub("", txt)
    if len(text) == 0:
        return Lettering.SINGLE
    if len(text) < 2:
        if text[0].isupper():
            return Lettering.UPPERCASE
        else:
            return Lettering.SINGLE
    if text[0].isupper() and not text[1].isupper():
        return Lettering.CAPITALIZED
    upper_count = 0
    for c in text:
        if c.isupper():
            upper_count += 1
    if upper_count > 0.5 * len(text):
        return Lettering.UPPERCASE
    else:
        return Lettering.LOWERCASE


def estimate_font_size(symbol_boxes):
    if len(symbol_boxes) < 1:
        return 1
    else:
        dxs = []
        dys = []
        for b in symbol_boxes:
            dxs.append(b.dx())
            dys.append(b.dy())
        dxs = sorted(dxs)
        dys = sorted(dys)
        n = int(len(dxs) / 2)
        return max(dxs[n], dys[n])


#
# bounding box class
# Box is real coordinate points (not normalized percentages)
class Box:
    def __init__(self, xmin=0, ymin=0, xmax=0, ymax=0):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def init(self, x0, y0, x1, y1):
        self.xmin = min(x0, x1)
        self.ymin = min(y0, y1)
        self.xmax = max(x0, x1)
        self.ymax = max(y0, y1)
        return self

    def center_x(self):
        return int(0.5 * (self.xmin + self.xmax))

    def center_y(self):
        return int(0.5 * (self.ymin + self.ymax))

    def width(self):
        return abs(self.xmax - self.xmin)

    def height(self):
        return abs(self.ymax - self.ymin)

    def dx(self):
        return abs(self.xmax - self.xmin)

    def dy(self):
        return abs(self.ymax - self.ymin)

    def in_tuple(self):
        return self.xmin, self.ymin, self.xmax, self.ymax

    def in_x_y_width_height_percentages(self, width, height):
        return (
            round(self.xmin / width, 3),
            round(self.ymin / height, 3),
            round((self.xmax - self.xmin) / width, 3),
            round((self.ymax - self.ymin) / height, 3),
        )

    def is_it_near_box(self, box_of_interest, w_margin=0.1, h_margin=0.1):
        boi = box_of_interest
        if self.xmax > (
            boi.center_x() - boi.dx() * (1 + w_margin) // 2
        ) and self.xmin < (boi.center_x() + boi.dx() * (1 + w_margin) // 2):
            if self.ymax > (
                boi.center_y() - boi.dy() * (1 + h_margin) // 2
            ) and self.ymin < (boi.center_y() + boi.dy() * (1 + h_margin) // 2):
                return True
        return False

    def is_it_in_box(self, box_of_interest, w_margin=0.1, h_margin=0.1):
        boi = box_of_interest
        x_delta = max(boi.dx() * (1 + w_margin) // 2, round(boi.dx() / 2, 0) + 1)
        if self.xmin >= (boi.center_x() - x_delta) and self.xmax <= (
            boi.center_x() + x_delta
        ):
            y_delta = max(boi.dy() * (1 + h_margin) // 2, round(boi.dy() / 2, 0) + 1)
            # print("here", self.ymin, (boi.center_y() - y_delta), self.ymax, (boi.center_y() + y_delta))
            if self.ymin >= (boi.center_y() - y_delta) and self.ymax <= (
                boi.center_y() + y_delta
            ):
                return True
        return False

    def is_box_in_self(self, box_of_interest, margin=5):
        box_of_interest_tuple = (
            box_of_interest.xmin,
            box_of_interest.ymin,
            box_of_interest.xmax,
            box_of_interest.ymax,
        )
        return self.is_box_tuple_in_self(box_of_interest_tuple, margin=margin)

    def is_box_tuple_in_self(self, box_of_interest_tuple, margin=5):
        xmin, ymin, xmax, ymax = box_of_interest_tuple
        if (
            self.xmin - margin <= xmin
            and self.xmax + margin >= xmax
            and self.ymin - margin <= ymin
            and self.ymax + margin >= ymax
        ):
            print("is_box_tuple_in_self: TRUE") if debug else None
            return True
        print("is_box_tuple_in_self: FALSE") if debug else None
        return False

    def is_box_tuple_in_same_vertical(self, box_of_interest_tuple):
        xmin, ymin, xmax, ymax = box_of_interest_tuple
        margin = 5
        if self.ymin - margin <= ymin and self.ymax + margin >= ymax:
            print("is_box_tuple_in_same_vertical: TRUE") if debug else None
            return True
        print("is_box_tuple_in_same_vertical: FALSE") if debug else None
        return False

    def get_right_box(self, page_size, width_limit=1):
        page_width, page_height = page_size
        right_box = Box(
            self.xmax,
            max(self.ymin, 0),
            min(self.xmax + int(page_width * width_limit), page_width),
            min(self.ymax, page_height),
        )
        return right_box

    def get_left_box(self, page_size, width_limit=1):
        page_width, page_height = page_size
        left_box = Box(
            max(0, int(self.xmin - page_width * width_limit)),
            max(self.ymin, 0),
            self.xmin,
            min(self.ymax, page_height),
        )
        return left_box

    def get_down_box(self, page_size, height_limit=1):
        page_width, page_height = page_size
        down_box = Box(
            max(0, self.xmin),
            self.ymax,
            min(self.xmax, page_width),
            min(self.ymax + int(page_height * height_limit), page_height),
        )
        return down_box

    def get_top_box(self, page_size, height_limit=1):
        page_width, page_height = page_size
        top_box = Box(
            max(0, self.xmin),
            max(int(self.ymin - page_height * height_limit), 0),
            min(self.xmax, page_width),
            self.ymin,
        )
        return top_box

    def get_intersection_with_box(self, box_of_interest):
        boi = box_of_interest
        if (
            boi.xmin >= self.xmax
            or self.xmin >= boi.xmax
            or self.ymax <= boi.ymin
            or boi.ymax <= self.ymin
        ):
            return None
        inter_xmin = max(self.xmin, boi.xmin)
        inter_ymin = max(self.ymin, boi.ymin)
        inter_xmax = min(self.xmax, boi.xmax)
        inter_ymax = min(self.ymax, boi.ymax)
        return Box(inter_xmin, inter_ymin, inter_xmax, inter_ymax)

    def get_combination_with_box(self, box_of_interest):
        comb_xmin = min(self.xmin, box_of_interest.xmin)
        comb_ymin = min(self.ymin, box_of_interest.ymin)
        comb_xmax = max(self.xmax, box_of_interest.xmax)
        comb_ymax = max(self.ymax, box_of_interest.ymax)
        return Box(comb_xmin, comb_ymin, comb_xmax, comb_ymax)

    def combine_with_other_box(self, box_of_interest):
        combined_box = self.get_combination_with_box(box_of_interest)
        self.xmin = combined_box.xmin
        self.ymin = combined_box.ymin
        self.xmax = combined_box.xmax
        self.ymax = combined_box.ymax
        return self

    def vertical_abs_distance_from_box(self, reference_tuple):
        r_xmin, r_ymin, r_xmax, r_ymax = (
            reference_box.xmin,
            reference_box.ymin,
            reference_box.xmax,
            reference_box.ymax,
        )
        if self.ymin <= r_ymin <= self.ymax or self.ymin <= r_ymax <= self.ymax:
            return 0
        if r_ymin <= self.ymin <= r_ymax or r_ymin <= self.ymax <= r_ymax:
            return 0
        if self.ymin >= r_ymax:
            return self.ymin - r_ymax
        if r_ymin >= self.ymax:
            return r_ymin - self.ymax
        return abs(self.ymax - r_ymax)

    def horizontal_abs_distance_from_box(self, reference_box):
        r_xmin, r_ymin, r_xmax, r_ymax = (
            reference_box.xmin,
            reference_box.ymin,
            reference_box.xmax,
            reference_box.ymax,
        )
        if self.xmin <= r_xmin <= self.xmax or self.xmin <= r_xmax <= self.xmax:
            return 0
        if r_xmin <= self.xmin <= r_xmax or r_xmin <= self.xmax <= r_xmax:
            return 0
        if self.xmin >= r_xmax:
            return self.xmin - r_xmax
        if r_xmin >= self.xmax:
            return r_xmin - self.xmax
        return abs(self.xmax - r_xmax)

    def __str__(self):
        return "(%d,%d):(%d,%d)" % (self.xmin, self.ymin, self.xmax, self.ymax)


# import from google-box definition
def get_xmin_ymin_xmax_ymax(bounding_box, page_size_tuple=(724, 1024), size_multiple=1):
    # NOTE: Sometimes you need these dimensions just for sorting. In that case, we are giving generic dimensions for the size of the page
    vertices = bounding_box.vertices or denormalize_vertices(
        bounding_box.normalized_vertices, (page_size_tuple[0], page_size_tuple[1])
    )

    if vertices:
        xs = [vertices[0].x, vertices[1].x, vertices[2].x, vertices[3].x]
        ys = [vertices[0].y, vertices[1].y, vertices[2].y, vertices[3].y]
        xmin = round(min(xs) / size_multiple)
        xmax = round(max(xs) / size_multiple)
        ymin = min(ys)
        ymax = max(ys)
        return xmin, ymin, xmax, ymax
    else:
        return None, None, None, None


# import from google-box definition
def init_bounding_box(bounding_box, page, size_multiple=1):
    xmin, ymin, xmax, ymax = get_xmin_ymin_xmax_ymax(
        bounding_box,
        page_size_tuple=(page.width, page.height),
        size_multiple=size_multiple,
    )

    box = Box()
    if xmin and ymin and xmax and ymax:
        box.xmin = xmin
        box.xmax = xmax
        box.ymin = ymin
        box.ymax = ymax
    return box


def denormalize_vertices(vertices, pg_size):
    pg_width, pg_height = pg_size
    # print("denormalize_vertices", pg_width, pg_height)
    return [
        vision_types.Vertex(
            x=round(pg_width * v.x), y=round(pg_height * v.y)
        )  # TODO: Edited. Is this due to google vision versioning?
        for v in vertices
    ]


def estimate_word_orientation_and_line_with_bounding_box(bounding_box, page_size):
    # The bounding box for the block. The vertices are in the order of top-left, top-right, bottom-right, bottom-left.
    # When a rotation of the bounding box is detected the rotation is represented as around the top-left corner
    # as defined when the text is read in the 'natural' orientation.
    vertices = bounding_box.vertices or denormalize_vertices(
        bounding_box.normalized_vertices, page_size
    )
    if len(vertices) != 4:
        return None

    top_left = vertices[0]
    top_right = vertices[1]
    bottom_right = vertices[2]
    bottom_left = vertices[3]
    top_center = ((top_left.x + top_right.x) / 2, (top_left.y + top_right.y) / 2)
    bottom_center = (
        (bottom_left.x + bottom_right.x) / 2,
        (bottom_left.y + bottom_right.y) / 2,
    )
    left_center = ((top_left.x + bottom_left.x) / 2, (top_left.y + bottom_left.y) / 2)
    right_center = (
        (top_right.x + bottom_right.x) / 2,
        (top_right.y + bottom_right.y) / 2,
    )

    if (
        min(
            abs(right_center[0] - left_center[0]), abs(right_center[1] - left_center[1])
        )
        < 8
    ):
        line, slope, intercept, lsize = None, 0, 0, 0
    else:
        line = [left_center[0], left_center[1], right_center[0], right_center[1]]
        slope = (right_center[1] - left_center[1]) / (right_center[0] - left_center[0])
        intercept = left_center[1] - left_center[0] * slope
        lsize = max(
            abs(right_center[0] - left_center[0]), abs(right_center[1] - left_center[1])
        )

    if abs(top_center[0] - bottom_center[0]) < 4:
        if top_center[1] <= bottom_center[1]:
            rotation_angle = 0
        elif top_center[1] > bottom_center[1]:
            rotation_angle = 180
    elif abs(top_center[1] - bottom_center[1]) < 4:
        if top_center[0] >= bottom_center[0]:
            rotation_angle = 90
        elif top_center[0] < bottom_center[0]:
            rotation_angle = 270
    else:
        tangent_ratio = (top_center[0] - bottom_center[0]) / (
            bottom_center[1] - top_center[1]
        )
        # print("estimate_text_orientation_from_word_bounding_box tangent_ratio ", tangent_ratio)
        rotation_angle = int(math.degrees(math.atan(tangent_ratio)))
        if top_center[1] > bottom_center[1]:
            rotation_angle = rotation_angle + 180
        if rotation_angle < 0:
            rotation_angle = rotation_angle + 360

    print(
        "estimate_word_orientation_with_bounding_box in degrees ", rotation_angle
    ) if debug else None

    delta_angle = 30
    if rotation_angle > (360 - delta_angle) or rotation_angle < delta_angle:
        return rotation_angle, TextOrientation.L2R, line, slope, intercept, lsize
    if (90 - delta_angle) < rotation_angle < (90 + delta_angle):
        return rotation_angle, TextOrientation.U2D, line, slope, intercept, lsize
    if (180 - delta_angle) < rotation_angle < (180 + delta_angle):
        return rotation_angle, TextOrientation.R2L, line, slope, intercept, lsize
    if (270 - delta_angle) < rotation_angle < (270 + delta_angle):
        return rotation_angle, TextOrientation.D2U, line, slope, intercept, lsize

    return rotation_angle, TextOrientation.L2R, line, slope, intercept, lsize


def check_for_line_end(line_text, sym, xmin, ymin, xmax, ymax):
    if sym.property.detected_break.type in [BREAKS.EOL_SURE_SPACE, BREAKS.LINE_BREAK]:
        print(
            line_text.strip(),
            "|",
            xmin,
            ymin,
            xmax,
            ymax,
            "|",
            "detected_break:%d" % sym.property.detected_break.type,
            "|",
            "Symbol text:",
            sym.text,
            "--",
        ) if debug else None
        line_obj = Lines(line_text.strip(), xmin, ymin, xmax, ymax)
        # line_text = ''
        return line_obj
    else:
        None


def check_for_space(sym):
    if sym.property.detected_break.type in [BREAKS.SPACE, BREAKS.SURE_SPACE]:
        # line_text += ' '
        return " "
    return ""


#
#
#
class Word:
    def __init__(self):
        self.box = Box()  # bounding box in the original image
        self.locator = ""  # 1_2_4 block #, paragraph #, line #
        self.index = 0  # word index
        self.text = ""  # original text
        self.cleaned_text = ""  # cleaned text
        self.font_size = 0  # word y-size in pixels
        self.lettering = Lettering.LOWERCASE  #
        self.confidence = 0.0  #
        self.x_percentage = (
            0.0  # x position percentage on page     - modified wrt page orientation
        )
        self.y_percentage = (
            0.0  # y position percentage on page     - modified wrt page orientation
        )
        self.dx_percentage = (
            0.0  # word x-size in percentage on page - modified wrt page orientation
        )
        self.dy_percentage = (
            0.0  # word y-size in percentage on page - modified wrt page orientation
        )
        self.is_bold = False  # is it written in bold
        self.fbr = 0.0  # average foreground/bacground signal ratio
        self.orientation_angle = 0  # orientation angle of the word on page
        self.orientation = TextOrientation.NONE  # orientation of the word on page
        self.line = None
        self.slope = 0
        self.intercept = 0
        self.line_size = 0
        self.paragraph_text = ""  # Used for debugging in printing

    def self_string(self):
        self_string_text = (
            "%3d [% 5d % 5d % 5d % 5d] [FS % 4d] [C %f] [Pos % 4.2f % 4.2f] Lettering [% 11s] O[% 5s] B[%d] Text[% 20s] Cleaned[% 20s] %s Pgrh[% 30s]"
            % (
                self.index,
                self.box.xmin,
                self.box.ymin,
                self.box.xmax,
                self.box.ymax,
                self.font_size,
                self.confidence,
                self.x_percentage,
                self.y_percentage,
                self.lettering.name,
                self.orientation.name,
                self.is_bold,
                self.text,
                self.cleaned_text,
                " " * 56,
                self.paragraph_text.strip()[:30],
            )
        )
        return self_string_text

    def print(self):
        print(
            "%3d [% 5d % 5d % 5d % 5d] [FS % 4d] [C %f] [Pos % 4.2f % 4.2f] Lettering [% 11s] O[% 5s] B[%d] Text[% 20s] Cleaned[% 20s] %s Pgrh[% 30s]"
            % (
                self.index,
                self.box.xmin,
                self.box.ymin,
                self.box.xmax,
                self.box.ymax,
                self.font_size,
                self.confidence,
                self.x_percentage,
                self.y_percentage,
                self.lettering.name,
                self.orientation.name,
                self.is_bold,
                self.text,
                self.cleaned_text,
                " " * 61,
                self.paragraph_text.strip()[:30],
            )
        )

    def print_text(self, separator, endl):
        print("%s%s" % (self.text, separator), end=endl)

    def is_exact_match(self, txt):
        return self.cleaned_text == txt

    def is_similar_match(self, txt, distance=2):
        dist = Levenshtein.distance(self.cleaned_text, txt)
        return bool(dist <= distance), dist


class Signature(Word):
    def __init__(self, xp, yp, wp, hp):
        Word.__init__(self)
        self.box = Box()  # bounding box in the original image  #
        self.x_percentage = (
            xp  # x position percentage on page     - modified wrt page orientation
        )
        self.y_percentage = (
            yp  # y position percentage on page     - modified wrt page orientation
        )
        self.dx_percentage = (
            wp  # word x-size in percentage on page - modified wrt page orientation
        )
        self.dy_percentage = (
            hp  # word y-size in percentage on page - modified wrt page orientation
        )
        self.words = []  # words around
        self.text = []  # original words around
        self.cleaned_text = []  # cleaned words around
        self.confidence = 0.0

    def print(self):
        print(
            "Signature Object: [XMIN:%-5d XMAX:%-5d YMIN:%-5d YMAX:%-5d] [C %f] [Pos % 4.2f % 4.2f] Text[% 20s] Cleaned[% 20s]"
            % (
                self.box.xmin,
                self.box.xmax,
                self.box.ymin,
                self.box.ymax,
                self.confidence,
                self.x_percentage,
                self.y_percentage,
                " ".join(self.text),
                " ".join(self.cleaned_text),
            )
        )


class Marker(Word):
    def __init__(self, xp, yp, wp, hp):
        Word.__init__(self)
        self.box = Box()  # bounding box in the original image  #
        self.x_percentage = (
            xp  # x position percentage on page     - modified wrt page orientation
        )
        self.y_percentage = (
            yp  # y position percentage on page     - modified wrt page orientation
        )
        self.dx_percentage = (
            wp  # word x-size in percentage on page - modified wrt page orientation
        )
        self.dy_percentage = (
            hp  # word y-size in percentage on page - modified wrt page orientation
        )
        self.words = []  # words around
        self.text = []  # original words around
        self.cleaned_text = []  # cleaned words around
        self.confidence = 0.0

    def print(self):
        print(
            "Marker Object: [% 5d % 5d % 5d % 5d] [C %f] [Pos % 4.2f % 4.2f] Text[% 20s] Cleaned[% 20s]"
            % (
                self.box.xmin,
                self.box.xmax,
                self.box.ymin,
                self.box.ymax,
                self.confidence,
                self.x_percentage,
                self.y_percentage,
                " ".join(self.text),
                " ".join(self.cleaned_text),
            )
        )


class Visual_Line(Word):
    def __init__(self, xp, yp, wp, hp):
        Word.__init__(self)
        self.box = Box()  # bounding box in the original image  #
        self.x_percentage = (
            xp  # x position percentage on page     - modified wrt page orientation
        )
        self.y_percentage = (
            yp  # y position percentage on page     - modified wrt page orientation
        )
        self.dx_percentage = (
            wp  # word x-size in percentage on page - modified wrt page orientation
        )
        self.dy_percentage = (
            hp  # word y-size in percentage on page - modified wrt page orientation
        )
        self.words = []  # words around
        self.text = []  # original words around
        self.cleaned_text = []  # cleaned words around
        self.confidence = 0.0

    def print(self):
        print(
            "Visual Line Object: [% 5d % 5d % 5d % 5d] [C %f] [Pos % 4.2f % 4.2f] Text[% 20s] Cleaned[% 20s]"
            % (
                self.box.xmin,
                self.box.xmax,
                self.box.ymin,
                self.box.ymax,
                self.confidence,
                self.x_percentage,
                self.y_percentage,
                " ".join(self.text),
                " ".join(self.cleaned_text),
            )
        )


class Lines(object):
    def __init__(self, text, xmin, ymin, xmax, ymax):
        self.text = (text or "").strip()
        self.box = Box(xmin, ymin, xmax, ymax)
        self.words = []

    def __str__(self):
        return "Text:%s, box:%d,%d,%d,%d center:%d,%d" % (
            self.text,
            self.box.xmin,
            self.box.ymin,
            self.box.xmax,
            self.box.ymax,
            self.box.center_x(),
            self.box.center_y(),
        )

    def print_words(self):
        if hasattr(self, "words"):
            for w in self.words:
                w.print()


class Paragraph:
    def __init__(self):
        self.lines = []
        self.box = Box()


class Block:
    def __init__(self):
        self.paragraphs = []
        self.box = Box()


class Page:
    def __init__(self):
        self.image = None
        self.language_code = "en"
        self.blocks = []
        self.signatures = ["Not Scanned"]
        self.markers = ["Not Scanned"]
        self.visual_lines = ["Not Scanned"]
        self.aws_tables = {}
        self.aws_block_map = {}
        self.file_name = ""
        self.page_number = 0
        self.height = 0
        self.width = 0
        self.max_font_size = 0
        self.median_font_size = 0
        self.mean_font_size = 0
        self.max_lettering = Lettering.SINGLE
        self.top_location = 1.0
        self.cleaned_words = []  # Sorted Words
        self.text = ""  # Sorted Line Text
        self.text_type = ""  # sorted, sorted_with_detected_lines, bulk
        self.text_dict = {}  # sorted Line information (Text, coordinates)
        self.non_filtered_vertical_lines = []  # non filtered vertical lines coordinates on page
        self.non_filtered_horizontal_lines = []  # non filtered horizontal lines coordinates on page
        self.horizontal_lines = []  # horizontal lines coordinates on page
        self.vertical_lines = []  # vertical lines coordinates on page

    def init(self, file_name, page_number):
        self.file_name = file_name
        self.page_number = page_number

    def n_cleaned_words(self):
        return len(self.cleaned_words)

    def get_cleaned_word(self, wid):
        if wid < len(self.cleaned_words):
            return self.cleaned_words[wid]
        return None

    def get_lines_for_block(self, block_number, combined_lines=False):
        if not (0 <= block_number < len(self.blocks)):
            return []
        block = self.blocks[block_number]
        lines = []
        for p in block.paragraphs:
            lines.extend(p.lines)
        if combined_lines:
            combined_lines = []
            line = None
            for i, l in enumerate(lines):
                n_l = lines[i + 1] if i + 1 < len(lines) else None
                if not line:
                    line = copy.deepcopy(l)
                    line.box = copy.deepcopy(l.box)
                else:
                    line.text = line.text + "\n" + l.text
                    line.box.combine_with_other_box(l.box)
                    line.words.extend(l.words) if line.words and l.words else []
                if not n_l:
                    combined_lines.append(line)
                else:
                    number_bullet = False
                    if n_l and n_l.text and len(n_l.text.split()[0]) <= 3:
                        number_bullet_pattern = r"^[a-zA-Z\d] ?[\.\)\-]"
                        if re.search(number_bullet_pattern, n_l.text.split()[0]):
                            number_bullet = True
                    if l.text and (l.text[-1] in [".", ":"] or number_bullet):
                        combined_lines.append(line)
                        line = None
            lines = combined_lines
        return lines

    def get_paragraphs_for_block(self, block_number):
        if not (0 <= block_number < len(self.blocks)):
            return []
        block = self.blocks[block_number]
        paragraphs = []
        for p in block.paragraphs:
            if p.lines:
                fl = p.lines[0]
                line = copy.deepcopy(fl)
                line.box = copy.deepcopy(fl.box)
                if len(p.lines) > 1:
                    for l in p.lines[1:]:
                        line.text = line.text + "\n" + l.text
                        line.box.combine_with_other_box(l.box)
                        line.words.extend(l.words) if line.words and l.words else []
                paragraphs.append(line)
        return paragraphs

    def get_blockline_for_block(self, block_number):
        if not (0 <= block_number < len(self.blocks)):
            return []
        block = self.blocks[block_number]
        block_line = None
        for p in block.paragraphs:
            if p.lines:
                i = 0
                if not block_line:
                    fl = p.lines[0]
                    block_line = copy.deepcopy(fl)
                    block_line.box = copy.deepcopy(fl.box)
                    i = 1
                for l in p.lines[i:]:
                    block_line.text = block_line.text + "\n" + l.text
                    block_line.box.combine_with_other_box(l.box)
                    block_line.words.extend(
                        l.words
                    ) if block_line.words and l.words else []
        return [block_line]

    def get_text_for_locator(self, locator, locator_selection="line"):
        local_debug = False
        # wrd.locator = "%d_%d_%d" % (block_counter, paragraph_counter, line_counter)
        # TYPE OPTIONS ARE "block", "paragraph", "line"
        locator = [int(n) for n in locator.split("_")]
        if not len(locator):
            return ""
        block_number = (
            locator[0] if len(locator) and isinstance(locator[0], int) else None
        )
        paragraph_number = (
            locator[1] if len(locator) > 1 and isinstance(locator[1], int) else None
        )
        line_number = (
            locator[2] if len(locator) > 2 and isinstance(locator[2], int) else None
        )
        print(
            "block_number",
            type(block_number),
            block_number,
            "paragraph_number",
            type(paragraph_number),
            paragraph_number,
            "line_number",
            type(line_number),
            line_number,
        ) if local_debug else None
        if block_number is None or block_number > len(self.blocks):
            return ""
        b = self.blocks[block_number]
        if (
            paragraph_number is None
            or paragraph_number > len(b.paragraphs)
            or (locator_selection and locator_selection == "block")
        ):
            print(
                "Returning all paragraphs of the block for locator:", locator
            ) if local_debug else None
            texts = []
            for p in b.paragraphs:
                for line in p.lines:
                    texts.append(line.text)
            return "\n".join(texts)
        p = b.paragraphs[paragraph_number]
        if (
            line_number is None
            or line_number > len(p.lines)
            or (locator_selection and locator_selection == "paragraph")
        ):
            print(
                "Returning all lines of the paragraph for locator:", locator
            ) if local_debug else None
            texts = []
            for line in p.lines:
                texts.append(line.text)
            return "\n".join(texts)
        print("Returning a single line for locator:", locator) if local_debug else None
        line = p.lines[line_number]
        return line.text

    def get_line(self, lid):
        page_lines = self.get_lines()
        return page_lines[lid]

    def get_lines(self, sorted=True, combined_lines=False):
        page_lines = []
        for block_number, block in enumerate(self.blocks):
            page_lines.extend(
                self.get_lines_for_block(block_number, combined_lines=combined_lines)
            )
        if sorted:
            page_lines = sort_description_boxes(page_lines)
        return page_lines

    def get_paragraphs(self, sorted=True):
        page_paragraph_lines = []
        for block_number, block in enumerate(self.blocks):
            paragraphs = self.get_paragraphs_for_block(block_number)
            page_paragraph_lines.extend(paragraphs)
        if sorted:
            page_paragraph_lines = sort_description_boxes(page_paragraph_lines)
        return page_paragraph_lines

    def get_bulk_text(self, sorted=True):
        if sorted:
            blocks = sort_description_boxes(self.blocks)
        else:
            blocks = self.blocks
        texts = []
        for b in blocks:
            for p in b.paragraphs:
                for line in p.lines:
                    texts.append(line.text)
        return "\n".join(texts)

    def get_sorted_lines_text(self):
        if not hasattr(self, "text"):
            setattr(self, "text", "")
        if self.text and self.text_type == "sorted":
            return self.text
        sorted_lines = self.get_lines(sorted=True)
        sorted_lines_texts = []
        for line in sorted_lines:
            sorted_lines_texts.append(line.text)
        sorted_lines_text = "\n".join(sorted_lines_texts)
        self.text = sorted_lines_text
        self.text_type = "sorted"
        return sorted_lines_text

    def get_sorted_lines_dict(self):
        page_lines = []
        for block_number, block in enumerate(self.blocks):
            page_lines.extend(self.get_lines_for_block(block_number))
        return sort_description_boxes_as_dict(page_lines)

    def get_sorted_text_with_detected_lines(self):
        if not hasattr(self, "text"):
            setattr(self, "text", "")
        if self.text and self.text_type == "sorted_with_detected_lines":
            return self.text

        if not (
            self.horizontal_lines
            or self.non_filtered_horizontal_lines
            or self.vertical_lines
        ):
            from . import visual_line

            # default: def detect_lines_for_text_sorting(image, horizontal_line_width_threshold=35, vertical_line_length_threshold=55):
            horizontal_lines, vertical_lines, non_filtered_horizontal_lines = (
                visual_line.detect_lines_for_text_sorting(self.image)
            )
            self.horizontal_lines = horizontal_lines
            self.vertical_lines = vertical_lines
            self.non_filtered_horizontal_lines = non_filtered_horizontal_lines

        from . import description_sorting

        sorted_text_with_detected_lines = (
            description_sorting.get_sorted_text_with_detected_lines(page=self)
        )

        if sorted_text_with_detected_lines:
            self.text = sorted_text_with_detected_lines
            self.text_type = "sorted_with_detected_lines"
            return sorted_text_with_detected_lines
        else:
            return self.get_sorted_lines_text()

    def get_words(self, sorted=True):
        page_words = []
        sorted_paragraphlines = self.get_paragraphs(sorted=sorted)
        for pl in sorted_paragraphlines:
            page_words.extend(pl.words)
        return page_words

    def get_line_under_box(
        self,
        box_of_interest,
        w_margin=0.9,
        h_margin=2,
        ycenter_under=False,
        get_all_text_under_full_box_width=False,
    ):
        local_debug = False
        sorted_lines = self.get_lines()
        candidates = []
        print(
            "<> get_line_under_box, box_of_interest", box_of_interest
        ) if local_debug else None
        all_lines_under = []
        for sl in sorted_lines:
            if ycenter_under:
                print("get_line_under_box", sl.text, sl.box) if local_debug else None
                if (
                    box_of_interest.center_y()
                    <= sl.box.ymin
                    <= box_of_interest.ymax + box_of_interest.height() * h_margin
                ):  # Get one line height as the acceptaple distance
                    print(
                        "--1 get_line_under_box", sl.text, sl.box
                    ) if local_debug else None
                    if (
                        box_of_interest.center_x()
                        - box_of_interest.width() * w_margin / 2
                        <= sl.box.center_x()
                        <= box_of_interest.center_x()
                        + box_of_interest.width() * w_margin / 2
                    ):
                        print(
                            "--2 get_line_under_box", sl.text, sl.box
                        ) if local_debug else None
                        if not get_all_text_under_full_box_width:
                            return sl
                        else:
                            all_lines_under.append(sl)
            else:
                # print("get_line_under_box", sl.text, sl.box) if local_debug else None
                if (
                    box_of_interest.ymax
                    < sl.box.ymin
                    < box_of_interest.ymax + sl.box.height() * h_margin
                ):  # Get one line height as the acceptaple distance
                    print(
                        "--1 get_line_under_box", sl.text, sl.box
                    ) if local_debug else None
                    if (
                        box_of_interest.center_x()
                        - box_of_interest.width() * w_margin / 2
                        < sl.box.center_x()
                        < box_of_interest.center_x()
                        + box_of_interest.width() * w_margin / 2
                    ):
                        print(
                            "--2 get_line_under_box", sl.text, sl.box
                        ) if local_debug else None
                        if not get_all_text_under_full_box_width:
                            return sl
                        else:
                            all_lines_under.append(sl)
        if all_lines_under:
            line = None
            for i, l in enumerate(all_lines_under):
                if not line:
                    line = copy.deepcopy(l)
                    line.box = copy.deepcopy(l.box)
                else:
                    line.text = line.text + "\n" + l.text
                    line.box.combine_with_other_box(l.box)
                    line.words.extend(l.words) if line.words and l.words else []
            return line

    def get_lines_inside_box(
        self,
        box_of_interest,
        w_margin=0.9,
        h_margin=2,
        get_all_text_under_full_box_width=False,
    ):
        sorted_lines = self.get_lines()
        all_lines_under = []
        for sl in sorted_lines:
            if (
                box_of_interest.ymin
                < sl.box.ymin
                < box_of_interest.ymax + sl.box.height() * h_margin
            ):  # Get one line height as the acceptaple distance
                if (
                    box_of_interest.center_x() - box_of_interest.width() * w_margin / 2
                    < sl.box.center_x()
                    < box_of_interest.center_x()
                    + box_of_interest.width() * w_margin / 2
                ):
                    if not get_all_text_under_full_box_width:
                        return sl
                    else:
                        all_lines_under.append(sl)
        if all_lines_under:
            line = None
            for i, l in enumerate(all_lines_under):
                if not line:
                    line = copy.deepcopy(l)
                    line.box = copy.deepcopy(l.box)
                else:
                    line.text = line.text + "\n" + l.text
                    line.box.combine_with_other_box(l.box)
                    line.words.extend(l.words) if line.words and l.words else []
            return line

    def get_words_in_same_vertical(
        self, box_of_interest, w_margin=0.2, h_margin=2, only_words_following=True
    ):
        return None

    def get_words_near_box(
        self,
        box_of_interest,
        w_margin=0.2,
        h_margin=2,
        sorted_by_horizantal_distance=False,
    ):
        # NOTE THAT: This function ignores if the box_of_interest is inside the word box!
        local_debug = False
        words_near = []
        print(
            "\nbox_of_interest",
            box_of_interest.xmin,
            box_of_interest.ymin,
            box_of_interest.xmax,
            box_of_interest.ymax,
        ) if local_debug else None
        page_words = self.get_words()
        for word in page_words:
            if word.box.is_it_near_box(
                box_of_interest, w_margin=w_margin, h_margin=h_margin
            ):
                if word.box.is_box_in_self(box_of_interest, margin=-1):
                    return (
                        None,
                        None,
                        None,
                    )  # Not a valid marker. For example text detected as a marker by mistake
                print(
                    str(self.page_number), word.self_string()
                ) if local_debug else None
                if sorted_by_horizantal_distance:
                    distance_to_marker = word.box.horizontal_abs_distance_from_box(
                        box_of_interest
                    )
                else:
                    distance_to_marker = abs(
                        box_of_interest.center_x() - word.box.center_x()
                    ) + abs(box_of_interest.center_y() - word.box.center_y())
                print(
                    "distance_to_marker", "%-15s" % word.text, distance_to_marker
                ) if local_debug else None
                words_near.append((word, distance_to_marker))
        words_near.sort(key=lambda x: x[1])
        words = []
        texts_near = []
        cleaned_texts_near = []
        for w in words_near:
            words.append(w[0])
            texts_near.append(w[0].text)
            cleaned_texts_near.append(w[0].cleaned_text)
        return words, texts_near, cleaned_texts_near

    def find_similar_words(self, text, distance=1, location=None):
        words_considered = self.cleaned_words
        found_words = []
        for i, word in enumerate(words_considered):
            if word.cleaned_text == text:
                found_words.append([i, 0])
            # Levenshtein Distance SLOWS DOWN
            # rv, dist = word.is_similar_match(text, distance=distance)
            # if rv is True:
            #   found_words.append([i, dist])
        return found_words

    def extract_word_stats(self):
        max_font_size = 0
        word_sizes = []
        max_lettering = Lettering.SINGLE.value
        top_location = 1.0
        for wrd in self.cleaned_words:
            word_sizes.append(wrd.font_size)
            max_font_size = max(max_font_size, wrd.font_size)
            top_location = min(top_location, wrd.y_percentage)
            max_lettering = max(max_lettering, wrd.lettering.value)
        self.max_font_size = max_font_size
        sorted_word_sizes = sorted(word_sizes)
        word_index = int(round(len(sorted_word_sizes) / 2, 0))
        if word_index >= len(sorted_word_sizes):
            print(
                "ERROR INVALID MEDIAN WORD SIZE!! extract_word_stats() %s %s"
                % (word_index, len(sorted_word_sizes))
            )
            self.median_font_size = (
                sorted_word_sizes[-1]
                if len(sorted_word_sizes) >= 1
                else self.max_font_size
            )
        else:
            try:
                self.median_font_size = sorted_word_sizes[word_index]
            except Exception as e:
                print(
                    "EXCEPTION INVALID MEDIAN WORD SIZE!! extract_word_stats() %s %s"
                    % (word_index, str(e))
                )

        self.mean_font_size = (
            round(sum(word_sizes) / len(word_sizes), 0) if len(word_sizes) > 0 else 0
        )  # Commented out to reduce processing
        self.max_lettering = Lettering(max_lettering)
        self.top_location = top_location

    def print(self):
        txt = ""
        page_words = self.cleaned_words
        for wrd in page_words:
            paragraph_text = self.get_text_for_locator(
                wrd.locator, locator_selection="paragraph"
            )
            wrd.paragraph_text = paragraph_text.replace("\n", " ")
            wrd.print()
            txt += wrd.cleaned_text + " "
        print("text          : ", txt)
        print("file name     : %s" % self.file_name)
        print("page number   : %d" % self.page_number)
        print(
            "width height  : %d %d" % (self.width, self.height),
            "    --- Google annotation width and height",
        )
        print("max font size : %d" % self.max_font_size)
        print("max lettering : %s" % self.max_lettering.name)
        print("top location  : %f" % self.top_location)
        print("language code : %s" % self.language_code)

    def add_words_attribute_on_page_description(self, deepcopy=False):
        if deepcopy:
            cloned_page_description = copy.deepcopy(self)
        else:
            cloned_page_description = self
        if cloned_page_description:
            if hasattr(cloned_page_description, "blocks"):
                for block in cloned_page_description.blocks:
                    for paragraph in block.paragraphs:
                        for line in paragraph.lines:
                            new_word_list = []
                            if hasattr(line, "words"):
                                for word in line.words:
                                    if (
                                        isinstance(word, tuple)
                                        and len(word) == 5
                                        and isinstance(word[0], str)
                                        and isinstance(word[1], int)
                                        and isinstance(word[2], int)
                                        and isinstance(word[3], int)
                                        and isinstance(word[4], int)
                                    ):
                                        word_text = word[0]
                                        word_box_xmin = word[1]
                                        word_box_ymin = word[2]
                                        word_box_xmax = word[3]
                                        word_box_ymax = word[4]
                                        box_ = Box(
                                            word_box_xmin,
                                            word_box_ymin,
                                            word_box_xmax,
                                            word_box_ymax,
                                        )
                                        wrd = Word()
                                        wrd.box = box_
                                        wrd.text = word_text
                                        # Get a list of attributes to delete
                                        attributes_to_delete = [
                                            attr
                                            for attr in wrd.__dict__
                                            if attr not in ("text", "box")
                                        ]
                                        # Delete each attribute in the list
                                        for attr in attributes_to_delete:
                                            delattr(wrd, attr)
                                        new_word_list.append(wrd)
                                    else:
                                        return cloned_page_description
                                line.words = new_word_list
                            else:
                                return None
        return cloned_page_description


class Document:
    def __init__(self):
        self.version = 1
        self.file_path = ""
        self.pages = []

    def n_pages(self):
        return len(self.pages)

    def page(self, idx):
        assert idx < self.n_pages()
        return self.pages[idx]

    def add_page(self, p):
        self.pages.append(p)

    def print(self):
        print("file_path: [%s]" % self.file_path)
        for p in self.pages:
            p.print()


def clean_page_description(page_description, deepcopy=False):
    if deepcopy:
        cleaned_page_description = copy.deepcopy(page_description)
    else:
        cleaned_page_description = page_description
    if cleaned_page_description:
        if hasattr(cleaned_page_description, "image"):
            del cleaned_page_description.image
        if hasattr(cleaned_page_description, "aws_tables"):
            del cleaned_page_description.aws_tables
        if hasattr(cleaned_page_description, "aws_block_map"):
            del cleaned_page_description.aws_block_map
        if hasattr(cleaned_page_description, "cleaned_words"):
            del cleaned_page_description.cleaned_words
        if hasattr(cleaned_page_description, "text"):
            cleaned_page_description.text = ""
        if not hasattr(cleaned_page_description, "text"):
            setattr(cleaned_page_description, "text", "")

        if hasattr(cleaned_page_description, "blocks"):
            for block in cleaned_page_description.blocks:
                # block_xmin = block.box.xmin
                # block_xmax = block.box.xmax
                # block_ymin = block.box.ymin
                # block_ymax = block.box.ymax
                # block.box = [block_xmin, block_ymin, block_xmax, block_ymax]

                for paragraph in block.paragraphs:
                    # paragraph_xmin = paragraph.box.xmin
                    # paragraph_xmax = paragraph.box.xmax
                    # paragraph_ymin = paragraph.box.ymin
                    # paragraph_ymax = paragraph.box.ymax
                    # paragraph.box = [paragraph_xmin, paragraph_ymin, paragraph_xmax, paragraph_ymax]
                    for line in paragraph.lines:
                        # line_xmin = line.box.xmin
                        # line_xmax = line.box.xmax
                        # line_ymin = line.box.ymin
                        # line_ymax = line.box.ymax
                        # line.box = [line_xmin, line_ymin, line_xmax, line_ymax]
                        new_word_list = []
                        for word in line.words:
                            if "box" in list(word.__dict__.keys()) and "text" in list(
                                word.__dict__.keys()
                            ):
                                new_word_list.append(
                                    (
                                        word.text,
                                        word.box.xmin,
                                        word.box.ymin,
                                        word.box.xmax,
                                        word.box.ymax,
                                    )
                                )
                        line.words = new_word_list
    return cleaned_page_description


def save_document_to_json(file_name, doc):
    jobj = jsonpickle.encode(doc)
    with open(file_name, "w") as f:
        f.write(jobj)
        f.close()


def load_document_from_json(file_name):
    with open(file_name, "r") as f:
        jobj = f.read()
        f.close()
        doc = jsonpickle.decode(jobj)
        if not isinstance(doc, Document):
            raise Exception("Document type is not correct")
        return doc


def sort_description_boxes(items):
    # Item could be any Descriptions object with Box() class.
    local_debug = False
    y_indexed_items = {}
    for item in items:
        xmin = item.box.xmin
        xmax = item.box.xmax
        ymin = item.box.ymin
        ymax = item.box.ymax
        combined = (ymin / 2 + ymax / 2, xmin / 2 + xmax / 2, item)  # USING AVERAGE
        print(
            "item", combined[0], combined[1], combined[2].text
        ) if local_debug and combined[0] < 100 else None
        y_index_found = False
        for y_index, y_index_list in y_indexed_items.items():
            if local_debug:
                line_text = ""
                for yin in y_index_list:
                    line_text = line_text + " " + yin[1].text
                print(">>", y_index, yin[0], line_text) if combined[0] < 100 else None

            # Y_INDEX IS CENTER, X_INDEX IS MAX
            if abs(combined[0] - y_index) < 4:
                y_index_list.append((combined[1], combined[2]))
                y_index_list.sort(key=lambda x: x[0])
                y_indexed_items[y_index] = y_index_list
                y_index_found = True
                break
        if not y_index_found:
            y_indexed_items[combined[0]] = [(combined[1], combined[2])]

    sorted_items = []
    # y_indexed_items is like {y_index:[(x_index_1, item_1), (x_index_2, item_2)]}
    y_indexed_items_sorted_in_tuples = sorted(y_indexed_items.items())
    for indexed_item in y_indexed_items_sorted_in_tuples:
        y_index, x_index_word_tuples_list = indexed_item
        # x_index_word_tuples_list.sort(key=lambda x: x[0])  # This is done above
        for x_index_word_tuple in x_index_word_tuples_list:
            sorted_items.append(x_index_word_tuple[1])
    return sorted_items


def sort_description_boxes_as_dict(items):
    # Item could be any Descriptions object with Box() class.
    local_debug = False
    y_indexed_items = {}
    for item in items:
        xmin = item.box.xmin
        xmax = item.box.xmax
        ymin = item.box.ymin
        ymax = item.box.ymax
        combined = (ymin / 2 + ymax / 2, xmin / 2 + xmax / 2, item)  # USING AVERAGE
        print(
            "item", combined[0], combined[1], combined[2].text
        ) if local_debug and combined[0] < 100 else None
        y_index_found = False
        for y_index, y_index_list in y_indexed_items.items():
            if local_debug:
                line_text = ""
                for yin in y_index_list:
                    line_text = line_text + " " + yin[1].text
                print(">>", y_index, yin[0], line_text) if combined[0] < 100 else None

            # Y_INDEX IS CENTER, X_INDEX IS MAX
            if abs(combined[0] - y_index) < 4:
                y_index_list.append((combined[1], combined[2]))
                y_index_list.sort(key=lambda x: x[0])
                y_indexed_items[y_index] = y_index_list
                y_index_found = True
                break
        if not y_index_found:
            y_indexed_items[combined[0]] = [(combined[1], combined[2])]

    sorted_items = []
    sorted_items_dict = {}
    ind = 0
    # y_indexed_items is like {y_index:[(x_index_1, item_1), (x_index_2, item_2)]}
    y_indexed_items_sorted_in_tuples = sorted(y_indexed_items.items())
    for indexed_item in y_indexed_items_sorted_in_tuples:
        y_index, x_index_word_tuples_list = indexed_item
        # x_index_word_tuples_list.sort(key=lambda x: x[0])  # This is done above
        for x_index_word_tuple in x_index_word_tuples_list:
            sorted_items.append(x_index_word_tuple[1])
            sorted_items_dict[ind] = x_index_word_tuple[1]
            ind += 1
    return sorted_items_dict


def parse_google_document_for_page(google_document):
    if len(google_document.pages) == 0:
        return None
    if len(google_document.pages) != 1:
        raise Exception(
            "This function is for running on a single page - Google Document object contains multiple pages"
        )

    p = Page()
    for gp in google_document.pages:
        p.language_code = (
            gp.property.detected_languages[0].language_code
            if gp.property.detected_languages
            else "en"
        )
        p.width = gp.width
        p.height = gp.height
        print("Page Width :", p.width) if debug else debug
        print("Page Height :", p.height) if debug else debug
        block_counter = 0
        for block in gp.blocks:
            b = Block()
            b.box = init_bounding_box(block.bounding_box, p)
            paragraph_counter = 0
            for paragraph in block.paragraphs:
                # prg_text = ''
                prg_objects = []
                par = Paragraph()

                par.box = init_bounding_box(paragraph.bounding_box, p)

                ##### LINE DETECTION SECTION #####
                line_counter = 0
                lines = []
                line_words = []
                line_text = ""
                xmin, ymin, xmax, ymax = 0, 0, 0, 0
                ##################################

                for w_count, word in enumerate(paragraph.words):
                    wrd = Word()
                    wrd.box = init_bounding_box(word.bounding_box, p)
                    wrd.confidence = word.confidence
                    wrd.text = ""
                    symbol_boxes = []
                    add_word_for_apostrophe_s = False

                    ##### LINE DETECTION SECTION #####
                    w_x, w_y, w_xx, w_yy = get_xmin_ymin_xmax_ymax(
                        word.bounding_box, (p.width, p.height)
                    )
                    xmax, ymax = max(w_xx, xmax), max(w_yy, ymax)
                    if not xmin:  # New Line
                        xmin, ymin = w_x, w_y
                    else:
                        xmin, ymin = min(xmin, w_x), min(ymin, w_y)
                    ##################################
                    length_check = True
                    if len(word.symbols) > 30:
                        entire_text_array = [
                            sym.text
                            for sym in word.symbols
                            if sym.confidence >= MIN_CONFIDENCE
                        ]
                        entire_text_set = set(entire_text_array)
                        entire_text = "".join(entire_text_array)
                        entire_text = entire_text.strip()
                        email_signs = constants.EMAIL_SIGNS
                        if "." in entire_text_set and "@" in entire_text_set:
                            email_end = entire_text.split(".")[-1]
                            if email_end in set(email_signs):
                                length_check = (
                                    False  # Emails might have more than 30 letters
                                )

                    for i, sym in enumerate(word.symbols):
                        ##### LINE DETECTION SECTION #####
                        if (
                            sym.confidence < MIN_CONFIDENCE
                            or sym.text in IGNORED_SYMBOLS
                            or (
                                length_check and len(word.symbols) > 30
                            )  # To avoid cases like 04203DJKEKDEKJD4230424234034023943943224234nj0000000
                        ):
                            sym.text = ""
                        line_text += sym.text
                        ##################################

                        # FIX: Post Google's OCR Changes on 5.2020, This Code Does not Recognize Homeowner's as Two Words Anymore like  "homeowner s" but Rather "homeowner's". The code below fixes that
                        if (
                            i == len(word.symbols) - 2
                            and (sym.text + word.symbols[-1].text).lower() == "'s"
                        ):
                            add_word_for_apostrophe_s = True
                            line_text += word.symbols[-1].text
                            line_text += check_for_space(word.symbols[-1])
                            line_obj = check_for_line_end(
                                line_text, word.symbols[-1], xmin, ymin, xmax, ymax
                            )
                            break

                        ##### LINE DETECTION SECTION #####
                        line_text += check_for_space(sym)
                        line_obj = check_for_line_end(
                            line_text, sym, xmin, ymin, xmax, ymax
                        )
                        # if sym.property.detected_break.type in [BREAKS.SPACE, BREAKS.SURE_SPACE]:
                        #    line_text += ' '
                        ##################################

                        sym_bb = sym.bounding_box
                        if sym_bb.vertices or sym_bb.normalized_vertices:
                            sym_box = init_bounding_box(sym_bb, p, 1)
                            # print("Symbol has vertices", sym_box.center_x())
                        else:
                            sym_box = init_bounding_box(
                                word.bounding_box, p, len(word.symbols)
                            )
                            # print("NO symbols vertices. Wordbox center:", sym_box.center_x())
                        wrd.text += sym.text
                        # prg_text += sym.text
                        wrd.font_size = max(
                            wrd.font_size, max(sym_box.dx(), sym_box.dy())
                        )
                        symbol_boxes.append(sym_box)

                    wrd.locator = "%d_%d_%d" % (
                        block_counter,
                        paragraph_counter,
                        line_counter,
                    )
                    wrd.x_percentage = float(wrd.box.center_x()) / p.width
                    wrd.y_percentage = float(wrd.box.center_y()) / p.height
                    wrd.dx_percentage = float(wrd.box.dx()) / p.width
                    wrd.dy_percentage = float(wrd.box.dy()) / p.height
                    wrd.lettering = get_text_lettering(wrd.text)
                    wrd.font_size = estimate_font_size(symbol_boxes)
                    (
                        orientation_angle,
                        orientation,
                        line,
                        slope,
                        intercept,
                        lsize,
                    ) = estimate_word_orientation_and_line_with_bounding_box(
                        word.bounding_box, (p.width, p.height)
                    )
                    wrd.orientation_angle = orientation_angle
                    wrd.orientation = orientation
                    wrd.line, wrd.slope, wrd.intercept, wrd.line_size = (
                        line,
                        slope,
                        intercept,
                        lsize,
                    )
                    line_words.append(wrd)
                    prg_objects.append(wrd)  # Just paragraph

                    if add_word_for_apostrophe_s:
                        s_wrd = copy.deepcopy(wrd)
                        s_wrd.text = "S"
                        prg_objects.append(s_wrd)  # Just paragraph
                        line_words.append(s_wrd)

                    if line_obj is not None:
                        line_obj.words = line_words
                        par.lines.append(line_obj)
                        xmax = 0
                        ymax = 0
                        xmin = None
                        ymin = None
                        line_counter += 1
                        line_words = []
                        line_text = ""
                b.paragraphs.append(par)
                paragraph_counter += 1
            p.blocks.append(b)
            block_counter += 1
    return p
