# import json
# import os
from abc import ABC, abstractmethod


class model(ABC):
    """
    Abstract base class for all models.

    Methods
    -------
    load_model(model_path: str)
        Load the model from the given path.

    generate(prompt: str, **kwargs)
        Generate output based on the prompt or any other input and optional parameters.

    set_params(params: dict)
        Set parameters for output generation.
    """

    @abstractmethod
    def load_model(self, model_path):
        """
        Load the model from the given path.

        Parameters
        ----------
        model_path : str
            The path to the model file.
        """
        pass

    @abstractmethod
    def generate(self, prompt, **kwargs):
        """
        Generate output based on the prompt or any other input and optional parameters.

        Parameters
        ----------
        prompt : str
            The prompt to generate text from.

        **kwargs
            Additional arguments for output generation. For example:
            - temperature: float
            - top_p: float
            - max_new_tokens: int
            - and others specific to the model.
        """
        pass

    @abstractmethod
    def set_params(self, params: dict):
        """
        Set parameters for generating output from a dictionary.

        Parameters
        ----------
        params : dict
            Dictionary of parameters to be used in generating output.
        """
        pass


# def load_params_from_json(json_file):
#     """
#     Load parameters from a JSON file.
#
#     Parameters
#     ----------
#     json_file : str
#         The path to the JSON file containing parameters.
#
#     Returns
#     -------
#     dict
#         Dictionary of parameters loaded from the JSON file.
#         Returns an empty dictionary if the file is not found.
#     """
#     if not os.path.exists(json_file):
#         print(f"Warning: {json_file} not found. Using default parameters.")
#         return {}  # Return an empty dict if the file does not exist
#     with open(json_file, 'r') as file:
#         params = json.load(file)
#     return params
