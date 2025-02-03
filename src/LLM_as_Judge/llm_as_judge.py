import gc
import time
import torch
from transformers import Idefics3ForConditionalGeneration, AutoProcessor

class LLmAsJudge:
    """
        Class gets test_dataset
        1. Goes through each element in the dataset
            - generates using standard SmolVLM
            - generate using MinMax
            - generate using fine-tuned SmolVLM
        2. Independent judge given wanted answer chooses which answer is better
        3. There are 3 distinct counteres:
            a. prefered_standard
            b. prefered_minmax
            c. prefered_fine_tuned
            d. equal_fine_tuned_minmax
        4. Success is to be accomplished if SmolVLM as at least as prefered as minmax
        5. Essays are graded using IELTS requirements.
    """
    def __init__(self, test_dataset):
        self.test_dataset = test_dataset




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

        print(f"GPU allocated memory: {torch.cuda.memory_allocated() / 1024**3:.2f} GB")
        print(f"GPU reserved memory: {torch.cuda.memory_reserved() / 1024**3:.2f} GB")

    def get_model_smol_processor(self):
        model_id = "HuggingFaceTB/SmolVLM-Instruct"
        model = Idefics3ForConditionalGeneration.from_pretrained(
            model_id,
            device_map="auto",
            torch_dtype=torch.bfloat16,
            # _attn_implementation="flash_attention_2",
        )

        processor = AutoProcessor.from_pretrained(model_id)

        return model, processor
    
    def generate_SmolVLM(self, sample):
        model, processor = self.get_model_smol_processor()
        return self.generate_text_from_sample(model, processor, sample)

    def generate_SmolVLM_fine_tuned(self):
        model, processor = self.get_model_smol_processor()
        adapter = "/root/Essay_LLM_Distillation/src/SmolVLM_training/smolvlm-instruct-trl-sft-ChartQA"
        
        


        

    def generate_text_from_sample(model, processor, sample, max_new_tokens=1024, device="cuda"):
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