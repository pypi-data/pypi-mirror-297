# Contains an abstract base class, BaseConvertor,
# that defines the common interface for all convertors.
# This class could have abstract methods like convert_to_normalizer and convert_from_normalizer.

# binaexperts/convertors/base.py

from abc import ABC, abstractmethod
from re import split
from typing import Any, IO
from binaexperts.schema.normalizer import NormalizedDataset
import json
# binaexperts/convertors/format_convertor.py

import os
import shutil
import zipfile
from zipfile import ZipFile, ZIP_DEFLATED

import yaml
from typing import Any, Union, IO
import io
from binaexperts.schema.coco import COCODataset, COCOImage, COCOAnnotation, COCOCategory
from binaexperts.schema.yolo import YOLODataset, YOLOImage, YOLOAnnotation
from binaexperts.schema.normalizer import NormalizedDataset, NormalizedImage, NormalizedAnnotation, NormalizedCategory

from binaexperts.convertors import const
import logging

# Configure logging at the beginning of your script or module
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseConvertor(ABC):

    def __init__(self):
        self.extract_dir = None

    # @abstractmethod
    # def initialize_paths(self, source: str):
    #
    #     """Set paths needed by the specific format. To be overridden by subclasses."""
    #     msg = '?'
    #     raise NotImplementedError(msg)

    @abstractmethod
    def load(self, source:  Union[str, IO[bytes]]) -> Any:
        """
         Load the data from the source format.

        :param source: File-like object representing the source dataset.
        :return: Loaded data in the source format.
        """
        msg = "The 'load' method must be overridden by subclasses."
        raise NotImplementedError(msg)

    @abstractmethod
    def normalize(self, data: Any) -> NormalizedDataset:
        """
        Convert the source format data to the normalized format.

        :param data: Loaded data in the source format.
        :return: Data converted to the normalized format.
        """
        msg = "The 'normalize' method must be overridden by subclasses."
        raise NotImplementedError(msg)

    @abstractmethod
    def convert(self, normalized_data: NormalizedDataset, destination:  Union[str, IO[bytes]]) -> None:
        """
        Convert the normalized format data to the target format.

        :param normalized_data: Data in the normalized format.
        :param destination: File-like object representing the target dataset.
        """
        msg = "The 'convert' method must be overridden by subclasses."
        raise NotImplementedError(msg)

    @abstractmethod
    def save(self, data: Any, destination:  Union[str, IO[bytes]]) -> None:
        """
        Save the data in the target format.

        :param data: Data in the target format.
        :param destination: File-like object to save the target dataset.
        """
        msg = "The 'save' method must be overridden by subclasses."
        raise NotImplementedError(msg)

class COCOConvertor(BaseConvertor):

    def __init__(self):
        super().__init__()

    def load(self, source: Union[str, IO[bytes]]) -> COCODataset:

        """
             Load COCO dataset from a zip file.

             :param source: File-like object (e.g., a BytesIO object) containing the zip archive with COCO data.
             :return: YOLODataset object populated with the data.
             """
        subdirs = ['train', 'test', 'valid']
        dataset = COCODataset(
            info={},
            images=[],
            annotations=[],
            categories=[]
        )

        if isinstance(source, str):
            if zipfile.is_zipfile(source):
                with ZipFile(source, 'r') as zip_file:
                    for subdir in subdirs:
                        annotation_path = f"{subdir}/_annotations.coco.json"

                        if annotation_path not in zip_file.namelist():
                            raise FileNotFoundError(f"Annotation file not found in {subdir}")

                        with zip_file.open(annotation_path) as file:
                            coco_data = json.load(file)

                        # Load categories (only once)
                        if not dataset.categories:
                            for cat in coco_data['categories']:
                                category = COCOCategory(
                                    id=cat['id'],
                                    name=cat['name'],
                                    supercategory=cat.get('supercategory', 'none')
                                )
                                dataset.categories.append(category)

                        # Load images
                        for img in coco_data['images']:
                            unique_image_id = f"{subdir}_{img['id']}"  # Prefix with split
                            image = COCOImage(
                                id=unique_image_id,  # Use unique string ID
                                file_name=img['file_name'],
                                width=img.get('width', 0),
                                height=img.get('height', 0),
                                split=subdir,
                                source_zip=zip_file,
                                image_content=None  # To be handled if needed
                            )
                            dataset.images.append(image)

                        # Load annotations **outside** the images loop
                        for ann in coco_data['annotations']:
                            unique_image_id = f"{subdir}_{ann['image_id']}"  # Ensure mapping to unique image ID
                            annotation = COCOAnnotation(
                                id=ann['id'],
                                image_id=unique_image_id,
                                category_id=ann['category_id'],
                                bbox=ann['bbox'],
                                segmentation=ann.get('segmentation', []),
                                area=ann.get('area', 0.0),
                                iscrowd=ann.get('iscrowd', 0)
                            )
                            dataset.annotations.append(annotation)

            else:
                # Case 2: If the source is a directory path
                for subdir in subdirs:
                    annotation_file = os.path.join(source, subdir, '_annotations.coco.json')

                    if not os.path.isfile(annotation_file):
                        raise FileNotFoundError(f"Annotation file not found in {os.path.join(source, subdir)}")

                    with open(annotation_file, 'r') as file:
                        coco_data = json.load(file)

                    # Load categories (only once)
                    if not dataset.categories:
                        for cat in coco_data['categories']:
                            category = COCOCategory(
                                id=cat['id'],
                                name=cat['name'],
                                supercategory=cat.get('supercategory', 'none')
                            )
                            dataset.categories.append(category)

                    # Load images
                    for img in coco_data['images']:
                        unique_image_id = f"{subdir}_{img['id']}"  # Prefix with split
                        image = COCOImage(
                            id=unique_image_id,  # Use unique string ID
                            file_name=img['file_name'],
                            width=img.get('width', 0),
                            height=img.get('height', 0),
                            split=subdir
                        )
                        dataset.images.append(image)

                    # Load annotations **outside** the images loop
                    for ann in coco_data['annotations']:
                        unique_image_id = f"{subdir}_{ann['image_id']}"  # Ensure mapping to unique image ID
                        annotation = COCOAnnotation(
                            id=ann['id'],
                            image_id=unique_image_id,
                            category_id=ann['category_id'],
                            bbox=ann['bbox'],
                            segmentation=ann.get('segmentation', []),
                            area=ann.get('area', 0.0),
                            iscrowd=ann.get('iscrowd', 0)
                        )
                        dataset.annotations.append(annotation)

        elif isinstance(source, ZipFile):
            # Handle opened zip file case
            for subdir in subdirs:
                annotation_path = f"{subdir}/_annotations.coco.json"

                if annotation_path not in source.namelist():
                    raise FileNotFoundError(f"Annotation file not found in {subdir}")

                with source.open(annotation_path) as file:
                    coco_data = json.load(file)

                # Load categories (only once)
                if not dataset.categories:
                    for cat in coco_data['categories']:
                        category = COCOCategory(
                            id=cat['id'],
                            name=cat['name'],
                            supercategory=cat.get('supercategory', 'none')
                        )
                        dataset.categories.append(category)

                # Load images
                for img in coco_data['images']:
                    unique_image_id = f"{subdir}_{img['id']}"  # Prefix with split
                    image_file_name = img['file_name']
                    image_path = f"{subdir}/{image_file_name}"

                    if image_path in source.namelist():
                        with source.open(image_path) as img_file:
                            image_content = img_file.read()  # Read image content in memory
                    else:
                        image_content = None
                        print(f"Warning: Image file {image_path} not found in zip archive.")

                    image = COCOImage(
                        id=unique_image_id,  # Use unique string ID
                        file_name=image_file_name,
                        width=img.get('width', 0),
                        height=img.get('height', 0),
                        split=subdir,
                        source_zip=source,
                        image_content=image_content
                    )
                    dataset.images.append(image)

                # Load annotations **outside** the images loop
                for ann in coco_data['annotations']:
                    unique_image_id = f"{subdir}_{ann['image_id']}"  # Ensure mapping to unique image ID
                    annotation = COCOAnnotation(
                        id=ann['id'],
                        image_id=unique_image_id,
                        category_id=ann['category_id'],
                        bbox=ann['bbox'],
                        segmentation=ann.get('segmentation', []),
                        area=ann.get('area', 0.0),
                        iscrowd=ann.get('iscrowd', 0)
                    )
                    dataset.annotations.append(annotation)

                # Load categories (only once)
                if not dataset.categories:
                    for cat in coco_data['categories']:
                        category = COCOCategory(
                            id=cat['id'],
                            name=cat['name'],
                            supercategory=cat.get('supercategory', 'none')
                        )
                        dataset.categories.append(category)
        else:
            raise ValueError("Source must be either a directory path or a file-like object.")

        return dataset

    def normalize(self, data: COCODataset) -> NormalizedDataset:
        """
        Convert COCODataset to NormalizedDataset, excluding certain categories.

        :param data: COCODataset object.
        :return: NormalizedDataset object.
        """
        # Define categories to exclude (e.g., supercategories or unwanted classes)
        excluded_category_ids = {0}  # Excluding "expiry-date"

        # Filter out excluded categories
        included_categories = [cat for cat in data.categories if cat.id not in excluded_category_ids]

        normalized_dataset = NormalizedDataset(
            description="Converted from COCO",
            dataset_name="COCO Dataset",
            dataset_type="Object Detection",
            splits={},  # Add split information if necessary
            nc=len(included_categories),
            names=[cat.name for cat in included_categories]
        )

        # Zero-based indexing for included categories
        category_id_map = {cat.id: idx for idx, cat in enumerate(included_categories)}

        # Map image IDs to normalized IDs
        image_id_map = {image.id: idx for idx, image in enumerate(data.images)}

        annotation_id = 1  # Initialize annotation ID

        print("=== Image ID Map ===")
        for k, v in image_id_map.items():
            print(f"Image ID: {k} → Normalized ID: {v}")
        print("====================\n")

        print("=== Category ID Map ===")
        for k, v in category_id_map.items():
            print(f"Category ID: {k} → Class ID: {v}")
        print("========================\n")

        # Convert and add images
        for image in data.images:
            normalized_image = NormalizedImage(
                id=image_id_map[image.id],
                file_name=image.file_name,
                width=image.width,
                height=image.height,
                split=image.split,
                source_zip=image.source_zip,
                image_content=image.image_content
            )
            normalized_dataset.add_image(normalized_image)
            print(f"Normalized Image: {normalized_image.file_name}, ID: {normalized_image.id}")

        # Convert and add annotations
        for ann in data.annotations:
            if ann.category_id in excluded_category_ids:
                continue  # Skip excluded categories

            if ann.category_id not in category_id_map:
                raise ValueError(f"Annotation with unknown category_id: {ann.category_id}")

            normalized_annotation = NormalizedAnnotation(
                id=annotation_id,
                image_id=image_id_map[ann.image_id],
                category_id=category_id_map[ann.category_id],
                bbox=ann.bbox,
                segmentation=ann.segmentation,
                area=ann.area,
                iscrowd=ann.iscrowd,
                bbox_format='xywh'  # COCO uses xywh format
            )
            normalized_dataset.add_annotation(normalized_annotation)
            print(
                f"Normalized Annotation ID: {normalized_annotation.id}, Image ID: {normalized_annotation.image_id}, Class ID: {normalized_annotation.category_id}, BBox: {normalized_annotation.bbox}")
            annotation_id += 1

        # Convert and add categories
        for cat in included_categories:
            normalized_category = NormalizedCategory(
                id=category_id_map[cat.id],
                name=cat.name,
                supercategory=cat.supercategory
            )
            normalized_dataset.add_category(normalized_category)
            print(f"Normalized Category: {normalized_category.name}, Class ID: {normalized_category.id}")

        return normalized_dataset

    def convert(self, normalized_data: NormalizedDataset, destination:  Union[str, IO[bytes]]) -> COCODataset:
        """
        Convert NormalizedDataset back to COCO format and write it to the destination.

        :param normalized_data: Data in the normalized format.
        :param destination: File-like object (e.g., zip file) to save the COCO dataset.
        :return: COCODataset object.
        """
        coco_dataset = COCODataset(
            info={
                "description": normalized_data.info["description"],
                "dataset_name": normalized_data.info["dataset_name"],
                "dataset_type": normalized_data.info["dataset_type"],
                "date_created": normalized_data.info["date_created"],
            },
            images=[],
            annotations=[],
            categories=[]
        )

        for normalized_image in normalized_data.images:
            coco_image = COCOImage(
                id=normalized_image.id,
                file_name=normalized_image.file_name,
                width=normalized_image.width,
                height=normalized_image.height,
                split = normalized_image.split,
                source_zip = normalized_image.source_zip,
                image_content = normalized_image.image_content
            )
            coco_dataset.images.append(coco_image)

        annotation_id = 1
        for normalized_annotation in normalized_data.annotations:
            coco_annotation = COCOAnnotation(
                id=annotation_id,
                image_id=normalized_annotation.image_id,
                category_id=normalized_annotation.category_id,
                bbox=normalized_annotation.bbox,
                segmentation=normalized_annotation.segmentation,
                area=normalized_annotation.area,
                iscrowd=normalized_annotation.iscrowd
            )
            coco_dataset.annotations.append(coco_annotation)
            annotation_id += 1

        for normalized_category in normalized_data.categories:
            coco_category = COCOCategory(
                id=normalized_category.id,
                name=normalized_category.name,
                supercategory=normalized_category.supercategory
            )
            coco_dataset.categories.append(coco_category)

        # Write the COCO format dataset to the destination
        self.save(coco_dataset, destination)

        return coco_dataset

    def save(self, data: COCODataset, destination:  Union[str, IO[bytes]]) -> None:
        """
        Save COCODataset to a zip file (in-memory or disk) in COCO format.

        :param data: COCODataset object.
        :param destination: File-like object (BytesIO) representing the destination zip file.
        """
        # Create a zip archive in the destination (which is an in-memory file or disk-based file)
        with ZipFile(destination, 'w', ZIP_DEFLATED) as zip_file:
            # Prepare the COCO JSON structure
            coco_dict = {
                "info": data.info,
                "images": [],
                "annotations": [],
                "categories": [vars(cat) for cat in data.categories]
            }

            # Handle images and annotations for each split
            for image in data.images:
                # Image path inside the zip (e.g., train/image.jpg)
                image_path_in_zip = os.path.join(image.split, image.file_name)
                annotation_file_name = os.path.join(image.split, '_annotations.coco.json')

                # Add the image to the zip file (assuming the file_name contains the correct path)
                with open(image.file_name, 'rb') as img_file:
                    zip_file.writestr(image_path_in_zip, img_file.read())

                # Add image info to the COCO dict
                coco_dict["images"].append(vars(image))

                # Add annotations for the corresponding image
                for ann in data.annotations:
                    if ann.image_id == image.id:
                        coco_dict["annotations"].append(vars(ann))

                    # Write the annotation JSON to the zip file
                # zip_file.writestr(annotation_file_name, json.dumps(coco_dict, indent=2))

class YOLOConvertor(BaseConvertor):

    def __init__(self):
        super().__init__()

    def load(self, source) -> YOLODataset:
    # def load(self, source:  Union[str, IO[bytes]]) -> YOLODataset:
        """
        Load YOLO dataset from a zip file.

        :param source: File-like object (e.g., a BytesIO object) containing the zip archive with YOLO data.
        :return: YOLODataset object populated with the data.
        """
        dataset = YOLODataset(
            path=None,  # No need for the path when working with in-memory data
            train_path='',
            val_path='',
            test_path='',
            nc=0,
            names=[]
        )

        # Open the zip file from the in-memory source
        with zipfile.ZipFile(source, 'r') as zip_file:
            # Read and parse the data.yaml file
            with zip_file.open('data.yaml') as file:
                data_yaml = yaml.safe_load(file)

            # Update the dataset metadata from the yaml file
            dataset.train_path = data_yaml.get('train', '')
            dataset.val_path = data_yaml.get('val', '')
            dataset.test_path = data_yaml.get('test', '')
            dataset.nc = data_yaml.get('nc', 0)
            dataset.names = data_yaml.get('names', [])

            # Iterate over the splits (train, val, test) and load images and annotations
            for split in ['train', 'val', 'test']:
                image_dir = os.path.join(data_yaml.get(split, ''), 'images')
                label_dir = os.path.join(data_yaml.get(split, ''), 'labels')

                # Get the list of image files in the split's 'images' directory within the zip
                image_files = [f for f in zip_file.namelist() if
                               f.startswith(image_dir) and (f.endswith('.jpg') or f.endswith('.png'))]

                for img_file in image_files:
                    img_file_name = os.path.basename(img_file)
                    image = YOLOImage(file_name=img_file_name, split=split)

                    # Construct the corresponding label file path
                    label_file_name = img_file_name.replace('.jpg', '.txt').replace('.png', '.txt')
                    label_file_path = os.path.join(label_dir, label_file_name)

                    # Check if the label file exists in the zip archive
                    if label_file_path in zip_file.namelist():
                        with zip_file.open(label_file_path, 'r') as label_file:
                            for line in io.TextIOWrapper(label_file, encoding='utf-8'):
                                class_id, cx, cy, w, h = map(float, line.strip().split())
                                annotation = YOLOAnnotation(
                                    class_id=int(class_id),
                                    bbox=[cx, cy, w, h],
                                    bbox_format='cxcywh'
                                )
                                image.annotations.append(annotation)

                    # Add the image (with annotations) to the dataset
                    dataset.images.append(image)

        return dataset

    def normalize(self, data: YOLODataset) -> NormalizedDataset:
        """
        Convert YOLODataset to NormalizedDataset.

        :param data: YOLODataset object.
        :return: NormalizedDataset object.
        """
        normalized_dataset = NormalizedDataset(
            description="Converted from YOLO",
            dataset_name="YOLO Dataset",
            dataset_type="Object Detection",
            splits={
                'train': data.train_path,
                'val': data.val_path,
                'test': data.test_path
            },
            nc=data.nc,
            names=data.names
        )

        image_id = 1
        annotation_id = 1

        for image in data.images:
            normalized_image = NormalizedImage(
                id=image_id,
                file_name=image.file_name,
                width=0,  # YOLO format doesn't store width/height, must be inferred if needed
                height=0,  # YOLO format doesn't store width/height, must be inferred if needed
                split=image.split
            )

            for ann in image.annotations:
                normalized_annotation = NormalizedAnnotation(
                    id=annotation_id,
                    image_id=image_id,
                    category_id=ann.class_id,
                    bbox=ann.bbox,
                    bbox_format=ann.bbox_format
                )
                normalized_image.annotations.append(normalized_annotation)
                normalized_dataset.add_annotation(normalized_annotation)
                annotation_id += 1

            normalized_dataset.add_image(normalized_image)
            image_id += 1

        for idx, name in enumerate(data.names):
            normalized_category = NormalizedCategory(id=idx, name=name)
            normalized_dataset.add_category(normalized_category)

        return normalized_dataset

    def convert(self, normalized_data: NormalizedDataset, destination: Union[str, IO[bytes]]) -> YOLODataset:
        """
        Convert NormalizedDataset to YOLODataset and save to destination.

        :param normalized_data: NormalizedDataset object.
        :param destination: Path or BytesIO object where the zip archive will be written.
        :return: YOLODataset object.
        """
        # Initialize an empty list to store YOLO images
        yolo_images = []

        # Create a map from image ID to annotations
        image_to_annotations = {}
        for annotation in normalized_data.annotations:
            if annotation.image_id not in image_to_annotations:
                image_to_annotations[annotation.image_id] = []
            image_to_annotations[annotation.image_id].append(annotation)

        print(f"Total Images to Convert: {len(normalized_data.images)}")
        print(f"Total Annotations: {len(normalized_data.annotations)}\n")

        for normalized_image in normalized_data.images:
            # Get annotations for this image
            annotations = image_to_annotations.get(normalized_image.id, [])

            print(f"Processing Image: {normalized_image.file_name}, Annotations Count: {len(annotations)}")

            # Create a list of YOLO annotations for this image
            yolo_annotations = []
            for normalized_annotation in annotations:
                # Retrieve image dimensions
                img_width = normalized_image.width
                img_height = normalized_image.height

                if normalized_annotation.bbox_format == 'xywh':
                    x, y, w, h = normalized_annotation.bbox
                    # Convert from xywh to cxcywh and normalize
                    cx = (x + w / 2) / img_width
                    cy = (y + h / 2) / img_height
                    width = w / img_width
                    height = h / img_height
                elif normalized_annotation.bbox_format == 'cxcywh':
                    cx, cy, width, height = normalized_annotation.bbox
                    # Assuming they are in absolute terms, normalize them
                    cx /= img_width
                    cy /= img_height
                    width /= img_width
                    height /= img_height
                else:
                    raise ValueError(f"Unsupported bbox format: {normalized_annotation.bbox_format}")

                # Ensure values are between 0 and 1
                cx = min(max(cx, 0.0), 1.0)
                cy = min(max(cy, 0.0), 1.0)
                width = min(max(width, 0.0), 1.0)
                height = min(max(height, 0.0), 1.0)

                # Round the values to six decimal places for consistency
                cx = round(cx, 6)
                cy = round(cy, 6)
                width = round(width, 6)
                height = round(height, 6)

                # Debugging: Print class ID and bounding box
                print(
                    f"  Annotation Class ID: {normalized_annotation.category_id}, BBox: ({cx}, {cy}, {width}, {height})")

                yolo_annotation = YOLOAnnotation(
                    class_id=normalized_annotation.category_id,  # Already 0-based
                    cx=cx,
                    cy=cy,
                    width=width,
                    height=height
                )
                yolo_annotations.append(yolo_annotation)

            # Create a YOLOImage object and pass the 'split' argument
            yolo_image = YOLOImage(
                file_name=normalized_image.file_name,
                annotations=yolo_annotations,
                split=normalized_image.split,  # Pass the split attribute here
                source_zip=normalized_image.source_zip,
                image_content=normalized_image.image_content
            )

            yolo_images.append(yolo_image)

        # Create the YOLODataset object with the list of YOLO images and category names
        yolo_dataset = YOLODataset(
            images=yolo_images,
            class_names=[category.name for category in normalized_data.categories]
        )

        self.save(yolo_dataset, destination)
        return yolo_dataset

    def save(self, data: YOLODataset, destination: Union[str, IO[bytes]]):
        """
        Save YOLODataset to a zip file in-memory.

        :param data: YOLODataset object.
        :param destination: Path or BytesIO object where the zip archive will be written.
        """
        with zipfile.ZipFile(destination, 'w') as zip_file:
            # Save data.yaml file in-memory
            dataset_yaml = {
                'train': 'train/images',
                'val': 'valid/images',
                'test': 'test/images',
                'nc': len(data.class_names),
                'names': data.class_names
            }
            yaml_content = yaml.dump(dataset_yaml)
            zip_file.writestr('data.yaml', yaml_content)
            print("Saved data.yaml")

            # Save images and labels into respective directories within the zip file
            for image in data.images:
                split_dir = f"{image.split}/images/"
                labels_dir = f"{image.split}/labels/"

                # Ensure the image content is present
                if image.image_content:
                    zip_file.writestr(os.path.join(split_dir, image.file_name), image.image_content)
                    print(f"Saved image: {os.path.join(split_dir, image.file_name)}")
                else:
                    print(f"Warning: No image content found for {image.file_name}")

                # Create and add the label file to the zip archive
                label_file_name = os.path.splitext(image.file_name)[0] + '.txt'
                label_zip_path = os.path.join(labels_dir, label_file_name)
                label_content = ""
                for annotation in image.annotations:
                    # Format: class_id cx cy width height with 6 decimal places
                    label_content += f"{annotation.class_id} {annotation.cx:.6f} {annotation.cy:.6f} {annotation.width:.6f} {annotation.height:.6f}\n"
                zip_file.writestr(label_zip_path, label_content)
                print(f"Saved label file: {label_zip_path} with {len(image.annotations)} annotations")

