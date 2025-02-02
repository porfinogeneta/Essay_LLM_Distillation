import os
import pandas as pd
import cv2
from datasets import Dataset, Features, Image, Value
from Logger.logger import setup_logger
from system_message import system_message

logger = setup_logger()



def collect_data(base_path="/Volumes/T7/smolvlm_dataset"):
    data = {
        'image_path': [],
        'title': [],
        'essay': [],
        'source': [],
        'filename': []
    }
    
    paths = {
        'pew': {
            'essays': os.path.join(base_path, "essays_pew"),
            'imgs': os.path.join(base_path, "imgs_pew"),
            'titles': os.path.join(base_path, "titles_pew")
        },
        'statista': {
            'essays': os.path.join(base_path, "essays_statista"),
            'imgs': os.path.join(base_path, "imgs_statista"),
            'titles': os.path.join(base_path, "titles_statista")
        }
    }

    for source, path_dict in paths.items():
        essay_files = [f for f in os.listdir(path_dict['essays']) if f.endswith('.txt')]
        for file in essay_files:
            filename = file.split(".")[0]
            
            # Read essay
            with open(os.path.join(path_dict['essays'], file), 'r') as f:
                essay = f.read()
            
            # Store image path instead of loading the image
            img_path = os.path.join(path_dict['imgs'], f"{filename}.png")
            if os.path.exists(img_path):
                data['image_path'].append(img_path)
            else:
                continue  # Skip if image doesn't exist
            
            # Read corresponding title
            title_path = os.path.join(path_dict['titles'], f"{filename}.txt")
            title = None
            if os.path.exists(title_path):
                with open(title_path, 'r') as f:
                    title = f.read()
            
            data['title'].append(title)
            data['essay'].append(essay)
            data['source'].append(source)
            data['filename'].append(filename)
    
    # Create HuggingFace dataset
    features = Features({
        'image': Image(),  # This will load images on-the-fly
        'title': Value('string'),
        'essay': Value('string'),
        'source': Value('string'),
        'filename': Value('string')
    })

    # Convert image paths to actual images in the dataset
    dataset_dict = {
        'image': data['image_path'],  # Dataset will handle image loading
        'title': data['title'],
        'essay': data['essay'],
        'source': data['source'],
        'filename': data['filename']
    }
    
    return Dataset.from_dict(dataset_dict, features=features)


def cleanup_unused_images(base_path="/Volumes/T7/smolvlm_dataset"):
    """
    Remove images that are not referenced in the dataset.
    This function should be called after collect_data().
    """
    # First collect the dataset to know which files are actually used
    dataset = collect_data(base_path)
    used_filenames = set(dataset['filename'])
    
    paths = {
        'statista': os.path.join(base_path, "imgs_statista")
    }
    
    deleted_files = []
    
    # Check each directory
    for source, img_dir in paths.items():
        if not os.path.exists(img_dir):
            print(f"Warning: Directory {img_dir} does not exist")
            continue
            
        # Get all PNG files in the directory
        all_images = [os.path.join(img_dir, f) for f in os.listdir(img_dir) 
                     if f.endswith('.png')]
        
        # Find and delete unused images
        for img_path in all_images:
            try:
                # Extract filename without extension and convert to int
                filename_int = int(os.path.splitext(os.path.basename(img_path))[0])
                if filename_int not in used_filenames:
                    os.remove(img_path)
                    deleted_files.append(img_path)
            except OSError as e:
                print(f"Error deleting {img_path}: {e}")
    
    # Print summary
    print(f"Deleted {len(deleted_files)} unused images")
    if deleted_files:
        print("Deleted files:")
        for f in deleted_files:
            print(f"  - {f}")
            
    return deleted_files


def format_data(sample):
    return [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": system_message
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": sample["image"],
                },
                {
                    "type": "text",
                    "text": sample['title'],
                }
            ],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": sample["essay"]
                }
            ],
        },
    ]

if __name__ == "__main__":
    cleanup_unused_images()