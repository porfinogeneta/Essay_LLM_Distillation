# python packages
from typing import Generator, Dict, Any, Optional
import os
from tqdm import tqdm

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
        max_elements: int = 1000
        ):
    """
    Helper function to save generated essays to files.
    """
    
    os.makedirs(output_dir, exist_ok=True)

    
    for i, result in tqdm(enumerate(essays_generator), total=max_elements):
        if i >= max_elements:
            break
        if result['status'] == 'success':
            filename = os.path.join(output_dir, f"{os.path.basename(result['plot_name'])}.txt")
            with open(filename, 'w') as f:
                f.write(result['essay'])

if __name__ == "__main__":
    generator = GenerateData()
    
    plots_to_process = [
        {'title': "Number of monthly active Facebook users worldwide as of 3rd quarter 2020 ( in millions )",
          'path': '/Volumes/T7/data_plots/Chart-to-text/statista_dataset/dataset/imgs/1.png'},
        {'title': "United States : estimated net worth of the 20 richest people as of March 2020 ( in billion U.S. dollars )",
          'path': '/Volumes/T7/data_plots/Chart-to-text/statista_dataset/dataset/imgs/2.png'},
        {'title': "Reported violent crime rate in the United States from 1990 to 2019", 
         'path': '/Volumes/T7/data_plots/Chart-to-text/statista_dataset/dataset/imgs/3.png'},
        {'title': "Number of new coronavirus ( COVID-19 ) deaths in Europe since February 2020 ( as of December 14 , 2020 ) , by date of report",
          'path': '/Volumes/T7/data_plots/Chart-to-text/statista_dataset/dataset/imgs/20.png'},
        {'title': "Distribution of coronavirus cases in Italy as of December 29 , 2020 , by age group",
          'path': '/Volumes/T7/data_plots/Chart-to-text/statista_dataset/dataset/imgs/110.png'},
        {'title': "Number of killed soldiers in U.S. wars since World War I as of October 2020",
          'path': '/Volumes/T7/data_plots/Chart-to-text/statista_dataset/dataset/imgs/407.png'},
        {'title': "Average annual player salary in the U.S. National Basketball Association in 2019/20 , by team ( in million U.S. dollars )",
          'path': '/Volumes/T7/data_plots/Chart-to-text/statista_dataset/dataset/imgs/1413.png'},
    ]

    # statista dataset
    # img_dir = '/Volumes/T7/smolvlm_dataset/imgs'
    # titles_dir = '/Volumes/T7/smolvlm_dataset/titles'
    # pew dataset
    img_dir = '/Volumes/T7/smolvlm_dataset/imgs_pew'
    titles_dir = '/Volumes/T7/smolvlm_dataset/titles_pew'

    output_dir = "/Users/szymon/Documents/projekciki/Essay_LMM_Distillation/smolVLM_data"

    # print(os.listdir("/Volumes/T7/data_plots/Chart-to-text/statista_dataset/dataset/imgs"))

    # for e in iter_paired_files(img_dir, titles_dir):
    #     print(e)
    
    plots_generator = iter_paired_files(img_dir, titles_dir)

    essays_generator = generator.essays_generator(plots_generator)
    
    save_essays(essays_generator,
                "/Volumes/T7/smolvlm_dataset/essays_pew",
                max_elements=5000
                )