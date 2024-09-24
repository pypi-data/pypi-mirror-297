
# BinaExperts SDK

This SDK provides tools for converting various dataset formats (COCO, YOLO, etc.) to and from the BinaExperts format. It is designed to be modular and extensible, allowing easy addition of new formats.

## Project Structure

```plaintext
binaexperts_sdk/
│
├── binaexperts/
│   ├── __init__.py
│   ├── convertors/
│   │   ├── __init__.py
│   │   ├── base.py        # Abstract base class for converters
│   │   ├── const.py        # COCO to/from BinaExperts converter
│   │   ├── convertor.py     # Factory class for creating converters
│   ├── schema/
│   │   ├── __init__.py
│   │   ├── coco.py                  # Schema for COCO format
│   │   ├── yolo.py                  # Schema for YOLO format
│   │   ├── binaexperts.py           # Schema for BinaExperts format
│   │   ├── normalizer.py           # Schema for Normalizer format
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_utils.py            # Utility functions for file operations
│   │   ├── validation_utils.py      # Utility functions for validating data 
│ 
│
├── setup.py                         # Setup script for packaging the SDK
├── README.md                        # Project documentation
└── requirements.txt                 # Python dependencies

```
## Installation

You can install the BinaExperts SDK directly from PyPI using `pip`:

```bash
pip install binaexperts
```
## Usage

Once you've installed the BinaExperts SDK, you can start converting datasets between different formats. Here's how to use the SDK:

### Basic Example

```python
from binaexperts.convertors.convertor import Convertor
convertor = Convertor()
# Convert COCO format to YOLO format
convertor.convert(
    source_path='path/to/input_coco.json', 
    target_path='path/to/output_yolo.txt',
    source_format='coco',
    target_format='yolo'
)
```
### Supported Formats

The BinaExperts SDK currently supports the following formats:

- COCO
- YOLO
- BinaExperts

## Contributing
Contributions are welcome!
To add support for more formats or improve the SDK, please refer to the Contributing section.
Please see the CONTRIBUTING.md for more details.

## License
This project is licensed under the MIT License - see the LICENSE file for details.