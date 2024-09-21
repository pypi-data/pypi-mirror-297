# common-services
Areal Shared Services

Write all necessary tests


[https://docs.python.org/3/library/unittest.html](https://docs.python-guide.org/writing/tests/)

## Text Sorting Algorithm ##

Text Sorting:
The new text sorting algorithm has been integrated into [descriptsions.py](https://github.com/Arealai/common-services/blob/development/common_services/services/descriptions.py). 
Below, you can see how the old sorting algorithm works for any comparisons, how the new sorting algorithm works, and the operating principles of the new algorithm.

### Compile Sorting Algorithms :mage:	###

To execute both text sorting algorithms, you first need to convert the PDF to an Image, create a Document object using Google OCR. Afterward, this document should be transformed into a Page object using the ```parse_google_document_for_page``` function found in the description script.


```python
from google.cloud import vision
from common_services.services.descriptions import parse_google_document_for_page

with open(img_path, "rb") as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)

client = vision.ImageAnnotatorClient()
response = client.document_text_detection(image=image)
document = response.full_text_annotation

pages = parse_google_document_for_page(document)
```


After this step, if you want to use the old sorting algorithm, you can simply use the ```get_sorted_lines_text()``` function in description.py. This function is belongs to the page class and does not take any parameters.


If you want to use the new sorting algorithm, you should first import ```get_sorted_text_with_detected_lines()``` function. This function takes an __PIL image object and Page object__ as parameters.

```python
from PIL import Image
from common_services.services.descriptions import parse_google_document_for_page
from common_services.services.description_sorting import get_sorted_text_with_detected_lines

pages = parse_google_document_for_page(document)

# Old Sorting Algorithm
text = pages.get_sorted_lines_text()

image = Image.open(img_path)
# New Sorting Algorithm
text = get_sorted_text_with_detected_lines(pages, image)


```

__Entire script for new sorting algorithm:__

```python
from PIL import Image
from google.cloud import vision
from common_services.services.descriptions import parse_google_document_for_page
from common_services.services.description_sorting import get_sorted_text_with_detected_lines

with open(img_path, "rb") as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)

client = vision.ImageAnnotatorClient()
response = client.document_text_detection(image=image)
document = response.full_text_annotation

pages = parse_google_document_for_page(document)
image = Image.open(img_path)
text = get_sorted_text_with_detected_lines(pages, image)
```

## Working Schema of New Sorting Algorithm :scroll:	##

You can follow the working principle of the new sorting algorithm from the chart below. As you can see from the chart, the algorithm consists of five steps: Preprocess, Phase1, Phase2, Phase3, and Phase4.
![entire_schema](https://github.com/Arealai/common-services/assets/19657350/caad65e3-1362-4a00-aa46-b2eb110a498d)


### Pre-Process Part ###

![pre_processes](https://github.com/Arealai/common-services/assets/19657350/9fe0cb0e-e61d-4adb-8898-00a62e03cc2e)

The new sorting algorithm relies on two essential pieces of data. The first one is the text lines sorted by the old sorting algorithm. The second one is the horizontal and vertical lines detected on the image.

The crucial point here is the output provided by the old sorting algorithm. In this output, text is sorted from top to bottom and left to right. That is, the priority is given to text with smaller y-coordinates. If texts share the same y-coordinate, they are sorted from left to right. While sorting from left to right, the algorithm also considers the proximity of words to each other. If words are close, they are merged; if there is a certain gap, the text after that gap is considered as the next line.

For use in the new sorting algorithm, each line's information is stored in a dictionary in sequential order. The keys of the dictionary are indices starting from 0 and going up to the number of lines, while the values contain text information and coordinates.

### Phase 1: Open Boxes ###

![phase1](https://github.com/Arealai/common-services/assets/19657350/de9c9088-ecc0-458f-b7c1-e49274ca72a1)


Phase 1 involves detecting open-ended boxes. In fact, this means that two consecutive horizontal lines are intersected by only one vertical line.

To ensure semantic integrity in documents containing such shapes, the following rules have been followed:

- If the area of a detected box is greater than 1M, it is filtered out.
- The boxes formed by intersected horizontal lines should be sorted internally first.
- Then these boxes should be merged from left to right.
- Finally, merging should be done from top to bottom.

### Phase 2: Closed BBoxes ###

![phase2](https://github.com/Arealai/common-services/assets/19657350/1dd1bc3a-0e20-4913-8634-149843ecaf74)

Phase 2, also known as the detection of closed boxes (BBoxes) and the sorting of texts within them. These boxes are formed when two consecutive horizontal lines are intersected by 2 vertical lines.

To ensure semantic integrity in documents containing such shapes, the following rules have been followed:

- If the area of a detected box is greater than 1M, it is filtered out.
- Boxes are sorted from small to large based on their areas.
- Then, for each box, it is checked whether there is a BBox vertically aligned with it consecutively.
- If such a BBox is found, these three BBoxes are sorted consecutively.
- This process continues until all vertical merges are completed.
- Finally, the texts within each box are merged.

### Phase 3: Key-Value Pairs ###

![phase3](https://github.com/Arealai/common-services/assets/19657350/f422fbc9-faaf-4065-8191-72a193b39e85)

Phase 3 detects connected information entered near a horizontal line, both above and below it. The crucial point here is that this information (Phone Number, License No., etc.) is mostly the same across documents, and these pieces of information are stored in the [constants.py](https://github.com/Arealai/common-services/blob/development/common_services/services/constants.py) script.

>> __IMPORTANT NOTE: If new documents containing new keys are introduced, [constants.py](https://github.com/Arealai/common-services/blob/development/common_services/services/constants.py) must be updated!__ :skull_and_crossbones:	

To ensure semantic integrity in documents containing such information, the following rules have been followed:

- If there is a text close to the detected horizontal line and within the xmin-xmax range, it is selected.
- There must be text both above and below the line; otherwise, it is not considered.
- Keys are searched in the text above or below it.
- Preprocessing has been applied to these keys (removal of punctuation and conversion from uppercase to lowercase).
- If a match is found, a sorting is made based on the text coordinates.

### Phase 4: Horizontal Line Patterns###

![phase4](https://github.com/Arealai/common-services/assets/19657350/e5e10aca-757b-4069-b9f0-0f231430094f)

Phase 4 detects consecutive sequential horizontal lines and sorts the information between them.

To ensure semantic integrity in documents containing such shapes, the following rules have been followed:

- The perimeter of consecutive horizontal lines is taken as a BBox.
- If there are texts to the right or left of this box, the box is not processed.
- Otherwise, the texts within the box are merged within each horizontal line, and they are sorted from top to bottom.
