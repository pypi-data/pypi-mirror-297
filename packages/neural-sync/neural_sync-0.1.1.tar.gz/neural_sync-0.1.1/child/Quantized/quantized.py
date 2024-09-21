import json
from llama_cpp import Llama

from parent.interface import model


class quantizedmodel(model):
    """
    A class representing a quantized model for text generation using Llama.

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
        self.model = None
        self.params = {}

    def load_model(self, model_path):
        """
        Load the model from the given path.

        Parameters
        ----------
        model_path : str
            The path to the model file.
        """
        self.model = Llama(model_path=model_path)
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

    def generate(self, prompt, **kwargs):
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
        # Update parameters for this specific call
        combined_params = {**self.params, **kwargs}

        response = self.model.create_chat_completion(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

        )
        return response["choices"][0]["message"]["content"]
