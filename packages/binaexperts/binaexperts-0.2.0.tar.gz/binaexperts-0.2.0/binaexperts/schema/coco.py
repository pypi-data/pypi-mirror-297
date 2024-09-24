# Contains classes and methods representing the COCO data model,
# which might include classes like COCOImage, COCOAnnotation, etc.
import zipfile
# binaexperts/schema/coco.py

from typing import List, Dict, Optional, Any

class COCOInfo:
    def __init__(self, description: str, dataset_name: str, dataset_type: str, date_created: str):
        """
        :param description: Description of the dataset.
        :param dataset_name: Name of the dataset.
        :param dataset_type: Type of the dataset.
        :param date_created: Date the dataset was created.
        """
        self.description = description
        self.dataset_name = dataset_name
        self.dataset_type = dataset_type
        self.date_created = date_created

class COCOImage:
    def __init__(self, id: int, file_name: str, width: int, height: int, split: str,
                 source_zip: Optional[zipfile.ZipFile] = None, image_content: Optional[bytes] = None):
        """
        Represents a COCO image with its metadata.

        :param id: Image ID.
        :param file_name: Filename of the image.
        :param width: Width of the image.
        :param height: Height of the image.
        :param split: Dataset split (train/val/test).
        :param source_zip: Optional ZipFile from which the image is loaded.
        :param image_content: In-memory content of the image.
        """
        self.id = id
        self.file_name = file_name
        self.width = width
        self.height = height
        self.split = split
        self.source_zip = source_zip
        self.image_content = image_content

class COCOAnnotation:
    def __init__(self,
                 id: int,
                 image_id: int,
                 category_id: int,
                 bbox: List[float],
                 segmentation: Optional[List[Any]] = None,
                 area: Optional[float] = None,
                 iscrowd: int = 0):
        """
        :param id: Annotation ID.
        :param image_id: ID of the image this annotation belongs to.
        :param category_id: Category ID.
        :param bbox: Bounding box coordinates in 'xywh' format.
        :param segmentation: Segmentation mask (if applicable).
        :param area: Area of the bounding box or segmentation mask.
        :param iscrowd: Whether the annotation represents a crowd.
        """
        self.id = id
        self.image_id = image_id
        self.category_id = category_id
        self.bbox = bbox
        self.segmentation = segmentation if segmentation is not None else []
        self.area = area
        self.iscrowd = iscrowd

class COCOCategory:
    def __init__(self, id: int, name: str, supercategory: Optional[str] = None):
        """
        :param id: Category ID.
        :param name: Category name.
        :param supercategory: Supercategory of the category.
        """
        self.id = id
        self.name = name
        self.supercategory = supercategory if supercategory is not None else "none"

class COCOLicense:
    def __init__(self, id: int, name: str, url: str):
        """
        :param id: License ID.
        :param name: Name of the license.
        :param url: URL of the license.
        """
        self.id = id
        self.name = name
        self.url = url

class COCODataset:
    def __init__(self,
                 info: Dict[str, Any],
                 images: List[COCOImage],
                 annotations: List[COCOAnnotation],
                 categories: List[COCOCategory],
                 licenses: Optional[List[COCOLicense]] = None):
        """
        :param info: Dataset info metadata.
        :param images: List of COCOImage objects.
        :param annotations: List of COCOAnnotation objects.
        :param categories: List of COCOCategory objects.
        :param licenses: List of COCOLicense objects (optional).
        """
        self.info = info
        self.images = images
        self.annotations = annotations
        self.categories = categories
        self.licenses = licenses if licenses is not None else []

    def add_image(self, image: COCOImage):
        self.images.append(image)

    def add_annotation(self, annotation: COCOAnnotation):
        self.annotations.append(annotation)

    def add_category(self, category: COCOCategory):
        self.categories.append(category)

    def add_license(self, license: COCOLicense):
        self.licenses.append(license)

