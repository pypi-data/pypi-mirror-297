# binaexperts/schema/normalizer.py
import io
import zipfile
from typing import List, Dict, Optional
from datetime import datetime

class NormalizedImage:
    def __init__(self, id: int, file_name: str, width: int, height: int, split: str, image_content: bytes, source_zip: zipfile.ZipFile):
        """
        :param id: Image ID.
        :param file_name: Image filename.
        :param width: Width of the image.
        :param height: Height of the image.
        :param split: Dataset split (train, val, test).
        """
        self.id = id
        self.file_name = file_name
        self.width = width
        self.height = height
        self.split = split  # 'train', 'val', or 'test'
        self.image_content = image_content
        self.source_zip = source_zip

class NormalizedAnnotation:
    def __init__(self,
                 id: int,
                 image_id: int,
                 category_id: int,
                 bbox: Optional[List[float]] = None,
                 segmentation: Optional[List[List[float]]] = None,
                 area: Optional[float] = None,
                 iscrowd: int = 0,
                 bbox_format: str = "xywh"):
        """
        :param id: Annotation ID.
        :param image_id: ID of the image this annotation belongs to.
        :param category_id: Category ID.
        :param bbox: Bounding box coordinates.
        :param segmentation: Segmentation mask (if applicable).
        :param area: Area of the bounding box or segmentation mask.
        :param iscrowd: Whether the annotation represents a crowd (COCO-specific).
        :param bbox_format: Format of bounding box ('xywh' for COCO, 'cxcywh' for YOLO).
        """
        self.id = id
        self.image_id = image_id
        self.category_id = category_id
        self.bbox = bbox if bbox is not None else []
        self.segmentation = segmentation if segmentation is not None else []
        self.area = area
        self.iscrowd = iscrowd
        self.bbox_format = bbox_format  # Supports 'xywh', 'cxcywh', etc.

class NormalizedCategory:
    def __init__(self, id: int, name: str, supercategory: Optional[str] = None):
        self.id = id
        self.name = name
        self.supercategory = supercategory if supercategory is not None else "none"

class NormalizedDataset:
    def __init__(self,
                 description: str = "Description",
                 organization: str = "Organization Name",
                 dataset_name: str = "Dataset Name",
                 dataset_type: str = "Dataset Type",
                 splits: Optional[Dict[str, str]] = None,
                 nc: int = 0,
                 names: Optional[List[str]] = None,
                 labels: Optional[List[Dict]] = None,
                 classifications: Optional[List[Dict]] = None,
                 augmentation_settings: Optional[Dict] = None,
                 tile_settings: Optional[Dict] = None,
                 false_positive: Optional[Dict] = None):
        """
        :param description: Description of the dataset.
        :param organization: Name of the organization.
        :param dataset_name: Name of the dataset.
        :param dataset_type: Type of the dataset.
        :param splits: Dictionary of dataset splits (train, val, test) with their paths.
        :param nc: Number of classes.
        :param names: List of class names.
        :param labels: Additional labels for BinaExperts.
        :param classifications: Classification data for BinaExperts.
        :param augmentation_settings: Augmentation settings for BinaExperts.
        :param tile_settings: Tile settings for BinaExperts.
        :param false_positive: False positive data for BinaExperts.
        """
        self.info = {
            "description": description,
            "organization": organization,
            "dataset_name": dataset_name,
            "dataset_type": dataset_type,
            "date_created": datetime.now().strftime('%Y-%m-%d')
        }
        self.images: List[NormalizedImage] = []
        self.annotations: List[NormalizedAnnotation] = []
        self.categories: List[NormalizedCategory] = []
        self.licenses: List[Dict] = [
            {
                "id": 1,
                "name": "Attribution-NonCommercial-ShareAlike License",
                "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
            }
        ]
        self.errors: List[str] = []
        self.splits = splits if splits is not None else {}  # e.g., {'train': '../train/images', 'val': '../valid/images'}
        self.nc = nc  # Number of classes
        self.names = names if names is not None else []  # List of class names
        self.labels = labels if labels is not None else []
        self.classifications = classifications if classifications is not None else []
        self.augmentation_settings = augmentation_settings if augmentation_settings is not None else {}
        self.tile_settings = tile_settings if tile_settings is not None else {}
        self.false_positive = false_positive if false_positive is not None else {}

    def add_image(self, image: NormalizedImage):
        self.images.append(image)

    def add_annotation(self, annotation: NormalizedAnnotation):
        self.annotations.append(annotation)

    def add_category(self, category: NormalizedCategory):
        self.categories.append(category)

    def add_error(self, error: str):
        self.errors.append(error)
