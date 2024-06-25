# https://youtu.be/NYeJvxe5nYw
"""
This code automates the conversion of binary masks representing different 
object categories into the COCO (Common Objects in Context) JSON format. 

The code is based on the following folder structure for training and validation
images and masks. You need to change the code based on your folder structure 
or organize your data to the format below.

EM-platelet-multi/   #Primary data folder for the project
├── input/           #All input data is stored here. 
│   ├── train_images/
│   │   ├── image01.png
│   │   ├── image02.png
│   │   └── ...
│   ├── train_masks/        #All binary masks organized in respective sub-directories.
│   │   ├── Alpha/
│   │   │   ├── image01.png
│   │   │   ├── image02.png
│   │   │   └── ...
│   │   ├── Cells/
│   │   │   ├── image01.png
│   │   │   ├── image02.png
│   │   │   └── ...
│   │   ├── Mito/
│   │   │   ├── image01.png
│   │   │   ├── image02.png
│   │   │   └── ...
│   │   └── Vessels/
│   │       ├── image01.png
│   │       ├── image02.png
│   │       └── ...
│   ├── val_images/
│   │   ├── image05.png
│   │   ├── image06.png
│   │   └── ...
│   └── val_masks/
│       ├── Alpha/
│       │   ├── image05.png
│       │   ├── image06.png
│       │   └── ...
│       ├── Cells/
│       │   ├── image05.png
│       │   ├── image06.png
│       │   └── ...
│       ├── Mito/
│       │   ├── image05.png
│       │   ├── image06.png
│       │   └── ...
│       └── Vessels/
│           ├── image05.png
│           ├── image06.png
│           └── ...
└── ...


For each binary mask, the code extracts contours using OpenCV. 
These contours represent the boundaries of objects within the images.This is a key
step in converting binary masks to polygon-like annotations. 

Convert the contours into annotations, including 
bounding boxes, area, and segmentation information. Each annotation is 
associated with an image ID, category ID, and other properties required by the COCO format.

The code also creates an images section containing 
metadata about the images, such as their filenames, widths, and heights.
In my example, I have used exactly the same file names for all images and masks
so that a given mask can be easily mapped to the image. 

All the annotations, images, and categories are 
assembled into a dictionary that follows the COCO JSON format. 
This includes sections for "info," "licenses," "images," "categories," and "annotations."

Finally, the assembled COCO JSON data is saved to a file, 
making it ready to be used with tools and frameworks that support the COCO data format.


"""

import glob
import json
import os
import cv2

# Label IDs of the dataset representing different categories
category_ids = {
    "Tubulitis": 1
}

MASK_EXT = 'png'
ORIGINAL_EXT = 'png'
image_id = 0
annotation_id = 0


def images_annotations_info(maskpath):
    """
    Process the binary masks and generate images and annotations information.

    :param maskpath: Path to the directory containing binary masks
    :return: Tuple containing images info, annotations info, and annotation count
    """
    global image_id, annotation_id
    annotations = []
    images = []

    # Iterate through categories and corresponding masks
    for category in category_ids.keys():
        for mask_image in glob.glob(os.path.join(maskpath, category, f'*.{MASK_EXT}')):
            original_file_name = f'{os.path.basename(mask_image).split(".")[0]}.{ORIGINAL_EXT}'
            mask_image_open = cv2.imread(mask_image)
            
            # Get image dimensions
            height, width, _ = mask_image_open.shape

            # Create or find existing image annotation
            if original_file_name not in map(lambda img: img['file_name'], images):
                image = {
                    "id": image_id + 1,
                    "width": width,
                    "height": height,
                    "file_name": original_file_name,
                }
                images.append(image)
                image_id += 1
            else:
                image = [element for element in images if element['file_name'] == original_file_name][0]

            # Find contours in the mask image
            blurred = cv2.GaussianBlur(mask_image_open, (5, 5), 0)
            gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
            thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,1)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


            # Create annotation for each contour
            for contour in contours:
                bbox = cv2.boundingRect(contour)
                area = cv2.contourArea(contour)


                segmentation = contour.flatten().tolist()
                # Пропустить контуры с площадью ниже порога
                


                annotation = {
                    "iscrowd": 0,
                    "id": annotation_id,
                    "image_id": image['id'],
                    "category_id": category_ids[category],
                    "bbox": bbox,
                    "area": area,
                    "segmentation": [segmentation],
                }
                #print(segmentation)
                # Add annotation if area is greater than zero
                if area < 10000:
                    annotations.append(annotation)
                    annotation_id += 1

    return images, annotations, annotation_id


def process_masks(mask_path, dest_json):
    global image_id, annotation_id
    image_id = 0
    annotation_id = 0

    # Initialize the COCO JSON format with categories
    coco_format = {
        "info": {},
        "licenses": [],
        "images": [],
        "categories": [{"id": value, "name": key, "supercategory": key} for key, value in category_ids.items()],
        "annotations": [],
    }

    # Create images and annotations sections
    coco_format["images"], coco_format["annotations"], annotation_cnt = images_annotations_info(mask_path)

    # Save the COCO JSON to a file
    with open(dest_json, "w") as outfile:
        json.dump(coco_format, outfile, sort_keys=True, indent=4)

    print("Created %d annotations for images in folder: %s" % (annotation_cnt, mask_path))

if __name__ == "__main__":
    train_mask_path = "C:\\Users\\minik\\Desktop\\final\\Tubules\\train\\masks"
    train_json_path = "C:\\Users\\minik\\Desktop\\final\\Tubules\\train\\images\\train.json"
    process_masks(train_mask_path, train_json_path)

    test_mask_path = "C:\\Users\\minik\\Desktop\\final\\Tubules\\test\\masks"
    test_json_path = "C:\\Users\\minik\\Desktop\\final\\Tubules\\test\\images\\test.json"
    process_masks(test_mask_path, test_json_path)

    val_mask_path = "C:\\Users\\minik\\Desktop\\final\\Tubules\\val\\masks"
    val_json_path = "C:\\Users\\minik\\Desktop\\final\\Tubules\\val\\images\\val.json"
    process_masks(val_mask_path, val_json_path)


    #aug_mask_path = "C:\\Users\\minik\\Desktop\\datasets\\MNL\\train_aug\\masks\\"
    #aug_json_path = "C:\\Users\\minik\\Desktop\\datasets\\MNL\\train_aug\\images\\train_aug.json"
    #process_masks(aug_mask_path, aug_json_path)