from openai import OpenAI
import base64
from typing import List, Generator, Dict, Any
from dotenv import load_dotenv
import os
import re
from Logger.logger import setup_logger

# prompts
from prompts.graph_type.graph_type import prompt as prompt_graph_type
from prompts.bar.bar import prompt as prompt_bar
from prompts.line.line import prompt as prompt_line
from prompts.pie.pie import prompt as prompt_pie
from prompts.table.table import prompt as prompt_table

logger = setup_logger()

class GenerateData:

    GRAPH_TYPES = {"PIE", "LINE", "BAR", "TABLE"}

    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv('API_KEY'),
            base_url="https://api.minimaxi.chat/v1",
        )

    def match_graph_type(self, text: str) -> str | None:
        if not text: return None
        pattern = '|'.join(self.GRAPH_TYPES)
        match = re.search(pattern, text.upper())
        return match.group() if match else None

    def encode_image_to_base64(self, image_path: str) -> str:
        """Convert local image to base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
        
    def parse_images_to_content(self, image_paths: List[str]):
        image_contents = []
        for image_path in image_paths:
            if image_path:  # Only process if path is provided
                base64_image = self.encode_image_to_base64(image_path)
                image_contents.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                })
        return image_contents
        
    def get_image_paths(self, prompt_folder_path: str, n_images: int, plot_path: str):
        prompt_images = ["IMAGE_" + str(i) for i in range(1, n_images + 1)]
        images_paths = [prompt_folder_path + '/' + img + '.png' for img in prompt_images]
        images_paths.append(plot_path)
        return images_paths
    
    def process_essay(self, essay: str) -> str:
        return essay

    def create_essay_prompt(self, plot_title: str, plot_path: str):
        
        # get plot type
        plot_type = self.get_plot_type(plot_path)
        # logger.debug(plot_type)
        if not plot_type: plot_type = "BAR"

        # get proper prompt and images
        PROMPT = {
            "PIE": prompt_pie,
            "TABLE": prompt_table,
            "LINE": prompt_line,
            "BAR": prompt_bar
        }.get(plot_type, prompt_bar)

        

        image_paths =self. get_image_paths(prompt_folder_path=f"/Users/szymon/Documents/projekciki/Essay_LMM_Distillation/src/prompts/{plot_type.lower()}",
                                        n_images=2,
                                        plot_path=plot_path
                                      )
        image_contents = self.parse_images_to_content(image_paths=image_paths)

        PROMPT = PROMPT.format(title=plot_title, image_name=plot_path.split("/")[-1])
        return image_contents, PROMPT

    def get_plot_type(self, plot_path: str):
        image_paths =self. get_image_paths(prompt_folder_path="/Users/szymon/Documents/projekciki/Essay_LMM_Distillation/src/prompts/graph_type",
                                        n_images=0,
                                        plot_path=plot_path
                                      )
        # logger.debug(image_paths)

        image_contents = self.parse_images_to_content(image_paths=image_paths)

        messages = [
            {"role": "system",
            "content": "MM Intelligent Assistant is a large language model that is self-developed to answer using provided plot classes."
            },
            {
                "role": "user",
                "name": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_graph_type
                    },
                    *image_contents
                ]
            }]

        try:
            completion = self.client.chat.completions.create(
                model="MiniMax-Text-01",
                messages=messages,
                max_tokens=100,
                )
            
            response = completion.choices[0].message.content
            return self.match_graph_type(response)
        
        except Exception as e:
            logger.error(f"Error getting plot type: {str(e)}")
            return None


    def essays_generator(self, plot_data: List[Dict[str, str]]) -> Generator[Dict[str, Any], None, None]:
        for i, plot in enumerate(plot_data):
            
            
            try:
            
                plot_title = plot["title"]
                plot_path = plot["path"]

                # logger.debug(plot_title)
                # logger.debug(plot_path)
                
                imgs, prompt = self.create_essay_prompt(plot_title=plot_title, plot_path=plot_path)

                # logger.debug(prompt)
                # return

                messages = [
                    {"role": "system",
                    "content": "MM Intelligent Assistant is a large language model that is self-developed to create Band 9 IELTS Essays. It does it writing description of plot titled <TITLE_LAST> using non-repetitive IELTS Band 9 vacabulary, whenever possible uses synonyms." 
                    },
                    {
                        "role": "user",
                        "name": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            *imgs
                        ]
                    }]
                
                completion = self.client.chat.completions.create(
                    model="MiniMax-Text-01",
                    messages=messages,
                    max_tokens=2500,
                    )
                
                essay = self.process_essay(essay=completion.choices[0].message.content)

                # logger.debug(f"plot title: {plot_title}")
                # logger.debug(f"plot name: {plot_path.split('/')[-1]}")

                yield {
                    'plot_title': plot_title,
                    'plot_name': plot_path.split('/')[-1],
                    'essay': essay,
                    'status': "success"
                }

            except Exception as e:
                    logger.error(f"Error processing plot {plot_path}: {str(e)}")
                    yield {
                    'plot_title': plot_title,
                        'plot_name': plot_path.split('/')[-1],
                        'error': str(e),
                        'status': 'error'
                    }
