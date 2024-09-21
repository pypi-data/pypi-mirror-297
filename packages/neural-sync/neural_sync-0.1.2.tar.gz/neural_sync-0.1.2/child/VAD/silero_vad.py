import torch

from parent.interface import model


# from abc import ABC, abstractmethod

class vadmodel(model):
    """
    A class representing a Voice Activity Detection (VAD) model using Silero VAD.

    Methods
    -------
    load_model(model_name: str)
        Load the VAD model from the given path or repository.

    generate(audio_file: str, **kwargs)
        Perform VAD on the provided audio file and return speech timestamps.

    set_params(params: dict)
        Set parameters for VAD.
    """

    def __init__(self):
        self.model = None
        self.get_speech_timestamps = None
        self.read_audio = None
        self.params = {}

    def load_model(self, repo_or_dir='snakers4/silero-vad', model_name='silero_vad'):
        """
        Load the VAD model from the given path or repository.

        Parameters
        ----------
        repo_or_dir : str
            The path or repository for the Silero VAD model.
        model_name : str
            The name of the model to be loaded.
        """
        # Load the Silero VAD model and utilities
        self.model, utils = torch.hub.load(repo_or_dir=repo_or_dir, model=model_name)
        (self.get_speech_timestamps, _, self.read_audio, _, _) = utils
        return self

    def set_params(self, **kwargs):
        """
        Set parameters for VAD (not used in Silero VAD, but kept for consistency).

        Parameters
        ----------
        params : dict
            Dictionary of parameters to be used in VAD.
        """
        self.params.update(kwargs)

    def generate(self, audio_file, **kwargs):
        """
        Perform VAD on the provided audio file.

        Parameters
        ----------
        audio_file : str
            The path to the audio file.

        **kwargs
            Additional arguments for VAD.

        Returns
        -------
        speech_timestamps : list of dict
            A list of dictionaries with speech timestamps.
        """
        # Read the audio file using the Silero utility
        wav = self.read_audio(audio_file)

        # Perform VAD using the loaded model and get speech timestamps
        speech_timestamps = self.get_speech_timestamps(wav, self.model)

        return speech_timestamps
