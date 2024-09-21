import torch
from PIL import Image
from abc import ABC, abstractmethod
from diffusers import StableDiffusion3Pipeline

from parent.interface import model


class diffusionmodel(model):
    """
    A class representing a Stable Diffusion model for image generation using Hugging Face Diffusers.

    Methods
    -------
    load_model(model_path: str)
        Load the model from the given path.

    generate(prompt: str, **kwargs)
        Generate an image based on the prompt and optional parameters.

    set_params(params: dict)
        Set parameters for image generation from a dictionary.
    """

    def __init__(self):
        self.pipeline = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.params = {}

    def load_model(self, model_path):
        """
        Load the model from the given path.

        Parameters
        ----------
        model_path : str
            The path to the model file or Hugging Face model name.
        """
        self.pipeline = StableDiffusion3Pipeline.from_pretrained(
            model_path,
            torch_dtype=torch.float16
        )
        self.pipeline = self.pipeline.to(self.device)
        return self

    def set_params(self, **kwargs):
        """
        Set parameters for image generation from a dictionary.

        Parameters
        ----------
        params : dict
            Dictionary of parameters to be used in image generation.
        """
        self.params.update(kwargs)

    def generate(self, prompt, **kwargs):
        """
        Generate an image based on the prompt and optional parameters.

        Parameters
        ----------
        prompt : str
            The prompt to generate an image from.

        **kwargs
            Additional arguments for image generation, such as:
            - height: int
            - width: int
            - guidance_scale: float
        """
        # Combine global and local parameters
        combined_params = {**self.params, **kwargs}

        # Generate image
        output = self.pipeline(prompt, **combined_params)
        return output.images[0]  # Return the first image in the batch
