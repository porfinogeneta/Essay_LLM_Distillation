import os
import pandas as pd
from datasets import Dataset, Features, Image, Value
from huggingface_hub import login
# from .Logger.logger import setup_logger
from .system_message import system_message
from datasets import load_dataset


# logger = setup_logger()



def collect_data(base_path="/root"):
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
        }
        # 'statista': {
        #     'essays': os.path.join(base_path, "essays_statista"),
        #     'imgs': os.path.join(base_path, "imgs_statista"),
        #     'titles': os.path.join(base_path, "titles_statista")
        # }
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
                continue
            
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
        'image': data['image_path'],
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
       'pew': {
            'imgs': os.path.join(base_path, "imgs_pew"),
            'titles': os.path.join(base_path, "titles_pew")
        },
        'statista': {
            'imgs': os.path.join(base_path, "imgs_statista"),
            'titles': os.path.join(base_path, "titles_statista")
        }
    }
    
    deleted_imgs = []
    deleted_titles = []
    
    # Check each directory
    for source in paths:

        img_dir = paths[source]["imgs"]
        titles_dir = paths[source]["titles"]

        if not os.path.exists(img_dir):
            print(f"Warning: Directory {img_dir} does not exist")
            continue
            
        # Get all PNG files in the directory
        all_images = [os.path.join(img_dir, f) for f in os.listdir(img_dir) 
                     if f.endswith('.png')]
        
        # Get all txt in titles directory
        all_texts = [os.path.join(titles_dir, f) for f in os.listdir(titles_dir) if f.endswith('.txt')]
        
        # Find and delete unused images
        for img_path in all_images:
            try:
                filename_int = os.path.splitext(os.path.basename(img_path))[0]
                if filename_int not in used_filenames:
                    os.remove(img_path)
                    deleted_imgs.append(img_path)
            except OSError as e:
                print(f"Error deleting {img_path}: {e}")

        # delete unused titles
        for title_path in all_texts:
            try:
                filename_int = os.path.splitext(os.path.basename(title_path))[0]
                if filename_int not in used_filenames:
                    os.remove(title_path)
                    deleted_titles.append(title_path)
            except OSError as e:
                print(f"Error deleting {title_path}: {e}")
    
    # Print summary
    print(f"Deleted {len(deleted_imgs)} unused images")
    print(f"Deleted {len(deleted_titles)} unused titles")
    # if deleted_files:
    #     print("Deleted files:")
    #     for f in deleted_files:
    #         print(f"  - {f}")
            
    # return deleted_files


def push_data_to_huggingface():
    dataset = collect_data()

    # logger.debug(f"Dataset size: {len(dataset)}")
    # logger.debug("First sample:", dataset[0])

    login() 

    dataset.push_to_hub(
        repo_id="szymmon/SmolVLM_Essay_Structured",
        private=False   
    )

def load_data_huggingface():
    dataset = load_dataset("szymmon/SmolVLM_Essay_Structured")

    shuffled_dataset = dataset['train'].shuffle(seed=42)

    # Simple 70-15-15 split
    total_size = len(shuffled_dataset)
    train_dataset, test_dataset, eval_dataset = shuffled_dataset.select(range(int(0.7*total_size))), shuffled_dataset.select(range(int(0.7*total_size), int(0.85*total_size))), shuffled_dataset.select(range(int(0.85*total_size), total_size))
    return train_dataset, test_dataset, eval_dataset

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
    # cleanup_unused_images()
    push_data_to_huggingface()