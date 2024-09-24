# Contains classes and methods representing the YOLO data model.
# binaexperts/schema/yolo.py
import zipfile
from typing import List, Optional


class YOLOAnnotation:
    def __init__(self, class_id: int, cx: float, cy: float, width: float, height: float):
        """
        Represents a single YOLO annotation (bounding box).

        :param class_id: ID of the class (object category).
        :param cx: X coordinate of the center of the bounding box, normalized (0 to 1).
        :param cy: Y coordinate of the center of the bounding box, normalized (0 to 1).
        :param width: Width of the bounding box, normalized (0 to 1).
        :param height: Height of the bounding box, normalized (0 to 1).
        """
        self.class_id = class_id
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height


class YOLOImage:
    def __init__(self, file_name: str, annotations: List[YOLOAnnotation], split: str,
                 source_zip: Optional[zipfile.ZipFile] = None, image_content: Optional[bytes] = None):
        """
        Represents a single YOLO image and its associated annotations.

        :param file_name: Filename of the image.
        :param annotations: List of YOLO annotations for this image.
        :param split: Data split (train, valid, or test).
        :param source_zip: Zip file source if image is stored inside a zip archive (optional).
        :param image_content: In-memory image content (optional).
        """

        self.file_name = file_name
        self.annotations = annotations
        self.split = split
        self.source_zip = source_zip  # Optional zip source
        self.image_content = image_content  # In-memory image content


class YOLODataset:
    def __init__(self, images: List[YOLOImage], class_names: List[str]):
        """
        Represents a YOLO dataset.

        :param images: List of YOLO images in the dataset.
        :param class_names: List of class names (object categories).
        """
        self.images = images
        self.class_names = class_names
        self.nc = len(class_names)  # Number of classes is the length of the class_names list

