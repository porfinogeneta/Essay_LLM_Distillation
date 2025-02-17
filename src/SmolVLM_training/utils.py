import os
import pandas as pd
import re
from datasets import Dataset, Features, Image, Value
from huggingface_hub import login
from Logger.logger import setup_logger
# from .system_message import system_message
from datasets import load_dataset

logger = setup_logger()



"""
    Extract raw essay output from an essay structure.
"""
def process_essay(text: str):

    raw_content = re.findall(r'"([^"]*)"', text)
    if raw_content:
        return "\n\n".join(con.strip() for con in raw_content if con.strip())

    paragraphs = text.replace('"', '').replace("'", '').split("\n")
    text_lst = [p.strip().strip('"') for p in paragraphs if len(p) > 70]

    return "\n\n".join(line for line in text_lst)

"""
    Given structured outputs proccess them and output decent essay.
"""
def unstructure_essays(base_path="/Volumes/T7/smolvlm_dataset", pew_essay_path="essays_pew", statista_essay_path="essays_statista"):
    pew_full_path = os.path.join(base_path, pew_essay_path)
    statista_full_path = os.path.join(base_path, statista_essay_path)

    
    raw_pew = os.path.join(base_path, "raw_essays_pew")
    os.makedirs(raw_pew, exist_ok=True)
    raw_statista = os.path.join(base_path, "raw_essays_statista")
    os.makedirs(raw_statista, exist_ok=True)

    essay_paths = [pew_full_path, statista_full_path]
    raw_paths = [raw_pew, raw_statista]

    for path, raw_path in zip(essay_paths, raw_paths):
        essay_files = [f for f in os.listdir(path) if f.endswith('.txt') and not f.startswith('._')]
        for file in essay_files:
            try:
                with open(os.path.join(path, file), 'r') as f:
                    essay = f.read()                

                with open(os.path.join(raw_path, file), 'w') as f:
                    processed_essay = process_essay(essay)
                    f.write(processed_essay)
            except Exception as e:
                logger.error(e)



def collect_data(base_path="/root", pew_essay_path="essays_pew", statista_essay_path="essays_statista"):
    data = {
        'image_path': [],
        'title': [],
        'essay': [],
        'source': [],
        'filename': []
    }
    
    paths = {
        'pew': {
            'essays': os.path.join(base_path, pew_essay_path),
            'imgs': os.path.join(base_path, "imgs_pew"),
            'titles': os.path.join(base_path, "titles_pew")
        },
        'statista': {
            'essays': os.path.join(base_path, statista_essay_path),
            'imgs': os.path.join(base_path, "imgs_statista"),
            'titles': os.path.join(base_path, "titles_statista")
        }
    }

    for source, path_dict in paths.items():
        essay_files = [f for f in os.listdir(path_dict['essays']) if f.endswith('.txt') and not f.startswith("._")]
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


def push_data_to_huggingface(base_path, pew_path, statista_path, repo_id: str):
    dataset = collect_data(base_path=base_path, pew_essay_path=pew_path, statista_essay_path=statista_path)

    # logger.debug(f"Dataset size: {len(dataset)}")
    # logger.debug("First sample:", dataset[0])

    login() 

    dataset.push_to_hub(
        repo_id=repo_id,
        private=False
    )

def load_data_huggingface(repo_id: str="szymmon/SmolVLM_Essay_Structured"):
    dataset = load_dataset(repo_id)

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
    # print(process_essay("""1. <Describe a graph>: "The bar chart illustrates South Korea's budget balance as a percentage of GDP from 2015 to 2025, with actual data from 2015 to 2019 and projections from 2020 to 2025." 2. <Find the key points, trends and compare data>: Paragraph 1: "From 2015 to 2019, South Korea experienced a positive budget balance, peaking at 2.56% of GDP in 2018. The budget balance started at 0.52% in 2015 and gradually increased, reaching its zenith in 2018 before slightly declining to 0.37% in 2019." Paragraph 2: "In contrast, the projections from 2020 to 2025 indicate a negative budget balance, with a significant downturn in 2020 at -3.24%. The deficit is expected to narrow gradually, but it remains negative, with projections showing -2.33% in 2021, -2.66% in 2022, -2.69% in 2023, and stabilizing at -2.54% from 2024 to 2025." 3. <Write a summary of presented data>: "Overall, South Korea's budget balance shifted from a surplus to a deficit over the decade. The period from 2015 to 2019 saw a positive trend, peaking in 2018. However, the projections from 2020 onwards indicate a persistent budget deficit, with a significant drop in 2020 and a gradual narrowing of the deficit in subsequent years." """))
    # unstructure_essays()
    push_data_to_huggingface("/Volumes/T7/smolvlm_dataset", "raw_essays_pew", "raw_essays_statista", repo_id="szymmon/SmolVLM_Essay_Database")