import json
import torch
from transformers import pipeline

from parent.interface import model


class transformersmodel(model):
    """
    A class representing a transformer model for text generation using Hugging Face Transformers.

    Methods
    -------
    load_model(model_path: str)
        Load the model from the given path.

    generate(prompt: str, **kwargs)
        Generate text based on the prompt and optional parameters.

    set_params(params: dict)
        Set parameters for text generation from a dictionary.
    """

    def __init__(self):
        self.pipeline = None
        self.params = {}

    def load_model(self, model_path):
        """
        Load the model from the given path.

        Parameters
        ----------
        model_path : str
            The path to the model file.
        """
        self.pipeline = pipeline(
            "text-generation",
            model=model_path,
            model_kwargs={"torch_dtype": torch.float16},
            device_map="auto",
            **self.params
        )
        return self

    def set_params(self, **kwargs):
        """
        Set parameters for text generation from a dictionary.

        Parameters
        ----------
        params : dict
            Dictionary of parameters to be used in text generation.
        """
        self.params.update(kwargs)

    def generate(self, prompt, system_prompt=None, **kwargs):
        """
        Generate text based on the prompt and optional parameters.

        Parameters
        ----------
        prompt : str
            The prompt to generate text from.

        **kwargs
            Additional arguments for text generation, such as:
            - temperature: float
            - top_p: float
            - max_new_tokens: int
            - other arguments supported by the model.
        """
        if system_prompt:
            full_prompt = f"System: {system_prompt}\nUser: {prompt}"
        else:
            full_prompt = prompt
        # Update parameters for this specific call
        combined_params = {**self.params, **kwargs}

        # Default settings for the pipeline
        gen_params = {}
        # "max_new_tokens": 1000
        # Update with any additional parameters
        gen_params.update(combined_params)

        # Transformers pipeline expects 'inputs' key instead of 'prompt'
        outputs = self.pipeline(prompt, **gen_params)
        return outputs[0]["generated_text"]

# Helper function to load parameters from a JSON file
