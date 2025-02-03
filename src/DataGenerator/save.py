# python packages
from typing import Generator, Dict, Any, Optional
import os
from tqdm import tqdm
from itertools import islice

# project imports
from DataGenerator.generation import GenerateData
from Logger.logger import setup_logger

logger = setup_logger()

def iter_paired_files(img_dir: str, titles_dir: str) -> Generator[Dict[str, str], None, None]:
    if not os.path.exists(img_dir) or not os.path.exists(titles_dir):
        raise ValueError(f"One or both directories don't exist: {img_dir}, {titles_dir}")
    
    
    for img_file in os.listdir(img_dir):
 
        if not img_file.endswith('.png'):
            continue
        

        title_path = os.path.join(titles_dir, f"{os.path.splitext(img_file)[0]}.txt")

        
        try:
            if os.path.exists(title_path):
                with open(title_path, 'r') as f:
                    title = f.read().strip()
                
                yield {
                    'title': title,
                    'path': os.path.join(img_dir, img_file)
                }
        except:
            logger.error(f"title path: {title_path}\nimage filename: {img_file}")
            continue


def save_essays(
        essays_generator: Generator[Dict[str, Any], None, None],
        output_dir: str,
        start_idx: int,
        max_elements: int = 1000
        ):
    """
    Helper function to save generated essays to files.
    """
    
    os.makedirs(output_dir, exist_ok=True)

    
    for i, result in tqdm(enumerate(islice(essays_generator, start_idx, None)), total=max_elements):
        if i >= max_elements:
            break
        if result['status'] == 'success':
            filename = os.path.join(output_dir, f"{os.path.basename(result['plot_name'])}.txt")
            logger.debug(filename)
            # with open(filename, 'w') as f:
            #     f.write(result['essay'])

if __name__ == "__main__":
    generator = GenerateData()
    
    # statista dataset
    img_dir = '/Volumes/T7/data_plots/Chart-to-text/statista_dataset/dataset/imgs'
    titles_dir = '/Volumes/T7/data_plots/Chart-to-text/statista_dataset/dataset/titles'
    # pew dataset
    # img_dir = '/Volumes/T7/smolvlm_dataset/imgs_pew'
    # titles_dir = '/Volumes/T7/smolvlm_dataset/titles_pew'

    output_dir = "/Users/szymon/Documents/projekciki/Essay_LMM_Distillation/smolVLM_data"

    # print(os.listdir("/Volumes/T7/data_plots/Chart-to-text/statista_dataset/dataset/imgs"))

    # for e in iter_paired_files(img_dir, titles_dir):
    #     print(e)
    
    plots_generator = iter_paired_files(img_dir, titles_dir)

    essays_generator = generator.essays_generator(plots_generator)
    
    save_essays(essays_generator,
                "/Volumes/T7/smolvlm_dataset/essays_statista",
                start_idx=1991,
                max_elements=5000
                )