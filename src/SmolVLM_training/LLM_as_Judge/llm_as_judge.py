import gc
import time
import torch
from openai import OpenAI
from dotenv import load_dotenv
import os
import re
import random
from tqdm import tqdm
from transformers import Idefics3ForConditionalGeneration, AutoProcessor
from src.SmolVLM_training.utils import load_data_huggingface, format_data, process_essay
from src.prompts.judge.judge_decide import prompt as decide_prompt
from src.Logger.logger import setup_logger



logger = setup_logger()
load_dotenv("/root/Essay_LLM_Distillation/.env")

class LLmAsJudge():
    """
        Class gets test_dataset
        1. Goes through each element in the dataset
            - generates using standard SmolVLM
            - generate using fine-tuned SmolVLM
        2. There is an inependent judge - MiniMax model
        3. Firstly it checks if the fine-tuned answer is more or less the same, gives binary score 0,1
        4. Secondly it compares output from SmolVLM and fine-tuned version with the golden sample, 
        then assigns certain score.
        5. Lastly BLEU score is utilised to compare golden standard answer with the one generated by SmolVLM
    """

    # ADEPTER_PATH = "/root/Essay_LLM_Distillation/src/SmolVLM_training/smolvlm-instruct-trl-sft-ChartQA_increased_batch"

    def __init__(self, essays_output_path, adapter_path):
        self.client = OpenAI(
            api_key=os.getenv('API_KEY'),
            base_url="https://api.minimaxi.chat/v1",
        )
        self.essays_path = essays_output_path
        self.adapter_path = adapter_path


    def clear_memory(self):
        # Delete variables if they exist in the current global scope
        if 'inputs' in globals(): del globals()['inputs']
        if 'model' in globals(): del globals()['model']
        if 'processor' in globals(): del globals()['processor']
        if 'trainer' in globals(): del globals()['trainer']
        if 'peft_model' in globals(): del globals()['peft_model']
        if 'bnb_config' in globals(): del globals()['bnb_config']
        time.sleep(2)

        # Garbage collection and clearing CUDA memory
        gc.collect()
        time.sleep(2)
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
        time.sleep(2)
        gc.collect()
        time.sleep(2)

        # print(f"GPU allocated memory: {torch.cuda.memory_allocated() / 1024**3:.2f} GB")
        # print(f"GPU reserved memory: {torch.cuda.memory_reserved() / 1024**3:.2f} GB")

    def get_model_and_processor(self):
        model_id = "HuggingFaceTB/SmolVLM-Instruct"
        model = Idefics3ForConditionalGeneration.from_pretrained(
            model_id,
            device_map="auto",
            torch_dtype=torch.bfloat16
        )

        processor = AutoProcessor.from_pretrained(model_id)

        return model, processor
    
        

    def generate_text_from_sample(self, model, processor, sample, max_new_tokens=1024, device="cuda"):
        # Prepare the text input by applying the chat template
        text_input = processor.apply_chat_template(
            sample[1:2],  # Use the sample without the system message
            add_generation_prompt=True
        )

        image_inputs = []
        image = sample[1]['content'][0]['image']
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image_inputs.append([image])

        # Prepare the inputs for the model
        model_inputs = processor(
            text=text_input,
            images=image_inputs,
            return_tensors="pt",
        ).to(device)  # Move inputs to the specified device

        # Generate text with the model
        generated_ids = model.generate(**model_inputs, max_new_tokens=max_new_tokens)

        # Trim the generated ids to remove the input ids
        trimmed_generated_ids = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        # Decode the output text
        output_text = processor.batch_decode(
            trimmed_generated_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )

        return output_text[0]  # Return the first decoded output text
    

    def generate_SmolVLM(self, sample):
        
        try:
            
            model, processor = self.get_model_and_processor()

            
            return self.generate_text_from_sample(model, processor, sample)
        except Exception as e:
            logger.error(e)

    def generate_SmolVLM_fine_tuned(self, sample):
        try: 
            model, processor = self.get_model_and_processor()
            # trained adapter, we use it to inject model with new knowledge, without
            # disturbing core parameters
            model.load_adapter(self.adapter_path)
            return self.generate_text_from_sample(model, processor, sample)
        except Exception as e:
            logger.error(e)


    def match_ranking(self, text):
        match = re.search(r'(first|second)', text.lower())
        return match.group(1) if match else None
    

    def write_to_files(self, idx, winner, title, essay, standard_essay, fine_tuned_essay):
        
            # golden
            golden_dir = os.path.join(self.essays_path, "golden")
            os.makedirs(golden_dir, exist_ok=True)
            golden_path = os.path.join(golden_dir, f"{idx}.txt")

            # standard
            standard_dir = os.path.join(self.essays_path, "standard")
            os.makedirs(standard_dir, exist_ok=True)
            smol_path = os.path.join(standard_dir, f"{idx}.txt")

            # fine tuned
            finetuned_dir = os.path.join(self.essays_path, "finetuned")
            os.makedirs(finetuned_dir, exist_ok=True)
            smol_finetuned_path = os.path.join(finetuned_dir, f"{idx}.txt")
            
            # save judged on essays
            with open(golden_path, 'w') as file:
                file.write(f"{title}\n{essay}\n{winner}")

            with open(smol_path, 'w') as file:
                file.write(standard_essay)

            with open(smol_finetuned_path, 'w') as file:
                file.write(fine_tuned_essay)


    def judge_sample_MiniMax(self, idx, sample):

        try:
            # get rid of essay structure for better judgment
            essay = process_essay(sample['essay'])
            image = sample['image']
            title = sample['title']


            formatted_sample = format_data(sample)
            
            self.clear_memory()
            standard_essay = self.generate_SmolVLM(formatted_sample)
            fine_tuned_essay = self.generate_SmolVLM_fine_tuned(formatted_sample)



            # prompt = decide_prompt.format(golden_title=title, golden_essay=essay, first_essay=standard_essay, second_essay=fine_tuned_essay)
            is_fine_tuned_first = random.random() < 0.5
            prompt = decide_prompt.format(golden_title=title, golden_essay=essay,
                                        first_essay=fine_tuned_essay if is_fine_tuned_first else standard_essay,
                                        second_essay=standard_essay if is_fine_tuned_first else fine_tuned_essay)

            messages = [
                {
                    "role": "system",
                    "content": "You are an intelligent assistent whose role is to compare two essays. You should decide which would be better on IELTS exam and features higher score band."
                },
                {
                    "role": "user",
                    "name": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image}"
                            }
                        }
                    ]
                }
            ]

            completion = self.client.chat.completions.create(
                model="MiniMax-Text-01",
                messages=messages,
                max_tokens=100,
                )
            return completion.choices[0].message.content, title, essay, standard_essay, fine_tuned_essay, is_fine_tuned_first
        
        except Exception as e:
            logger.error(e)


    def judge_smolVLM(self, data_repo_id: str):
        self.clear_memory()

        scores = {
            "standard": 0,
            "fine_tuned": 0
            }

        try:
            _, test_dataset, _ = load_data_huggingface(repo_id=data_repo_id)

            for i, sample in tqdm(enumerate(test_dataset)):
                llm_response, title, essay, standard_essay, fine_tuned_essay, is_fine_tuned_first = self.judge_sample_MiniMax(i, sample)
                response = self.match_ranking(llm_response)
                if response == "first":
                    if is_fine_tuned_first:
                        scores["fine_tuned"] += 1
                    else:
                        scores["standard"] += 1
                elif response == "second":
                    if not is_fine_tuned_first:
                        scores["fine_tuned"] += 1
                    else:
                        scores["standard"] += 1
                
                self.write_to_files(i, llm_response, title, essay, standard_essay, fine_tuned_essay)
                
                logger.debug(scores)

        except Exception as e:
            logger.error(e)

        
        return scores

if __name__ == "__main__":
    judge = LLmAsJudge(essays_output_path="/root/Essay_LLM_Distillation/src/SmolVLM_training/LLM_as_Judge/JudgeDatasets_unstructured",
                       adapter_path="/root/Essay_LLM_Distillation/src/SmolVLM_training/smolvlm-instruct-trl-sft-ChartQA_trained_unstructured")
    print(judge.judge_smolVLM(data_repo_id="szymmon/SmolVLM_Essay_Database"))
    # judge.generate_all("finetuned")
    # _, test, _ = load_data_huggingface()
    # logger.debug(test[0])

    # for m in test:
    #     filename = m['filename']
    #     essay = m['essay']
    #     image = m['image']
    #     title = m['title']

    #     logger.debug(title)
    #     logger.debug(essay)