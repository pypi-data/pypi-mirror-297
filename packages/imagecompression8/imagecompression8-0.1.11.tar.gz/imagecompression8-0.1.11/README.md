# Image Compression

It is an image compression Python package based on Singular Value Decomposition (SVD) technology. This tool offers an efficient block-based image compression method, reducing the storage requirements of images by dividing them into blocks and applying SVD, while retaining as much visual information as possible.

## Installation

```bash
pip install .
```

## Usage

```
#%% package
from imagecompression8 import compress_image_with_svd
import os
from PIL import ImageFilter

#%% path
image_path = 'YOUR_IMAGE_PATH.jpg'

#%% mkdir --> exist?
output_dir = 'THE_FOLDER_YOU_WANT_TO_PLACE'
os.makedirs(output_dir, exist_ok = True)

#%% block & rank
block_size = # YOU CAN USE 16, 32, 64, 128...
rank = # YOU CAN SET `RANK = NONE` TO AUTOMATICALLY SELECT THE NUMBER OF SINGULAR VALUES. YOU CAN ALSO SET IT MANUALLY; THE SMALLER THE VALUE OF `RANK`, THE STRONGER THE COMPRESSION BUT LESS INFORMATION IS RETAINED. THE LARGER THE VALUE, THE WEAKER THE COMPRESSION BUT MORE INFORMATION IS PRESERVED.

#%% compression & sharp
compressed_image = compress_image_with_svd(image_path, 
                                           block_size = block_size, 
                                           rank = rank)
compressed_image = compressed_image.filter(ImageFilter.SHARPEN)

#%% save
compressed_image.save(os.path.join(output_dir, 'THE_IMAGE_NAME_YOU_WANT_TO_ACCESS.jpg')) # SUPPORTS INPUT AND OUTPUT IN MULTIPLE IMAGE FORMATS, SUCH AS JPEG, PNG, BMP, SUITABLE FOR DIFFERENT APPLICATION SCENARIOS.

```
