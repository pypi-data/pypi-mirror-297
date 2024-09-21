import matplotlib.pyplot as plt
import torch
from pyannote.audio import Pipeline
from pyannote.core import notebook

from parent.interface import model


class SpeakerDiarizationModel(model):
    """
    A class representing a speaker diarization model using pyannote.

    Methods
    -------
    load_model(model_path: str)
        Load the speaker diarization model from the given path.

    generate(audio_file: str, visualize: bool)
        Perform speaker diarization on the provided audio file and visualize results if needed.

    set_params(params: dict)
        Set parameters for speaker diarization.
    """

    def __init__(self):
        self.pipeline = None
        self.params = {}

    def load_model(self, model_path, use_auth_token):
        """
        Load the speaker diarization model from the given path.

        Parameters
        ----------
        model_path : str
            The path or model name for pyannote's model.
        use_auth_token : str
            The Hugging Face authentication token.
        """
        # Load the model pipeline from pretrained
        self.pipeline = Pipeline.from_pretrained(
            model_path,
            use_auth_token=use_auth_token
        )

        # Move the pipeline to GPU
        self.pipeline.to(torch.device("cuda"))

        return self

    def set_params(self, **kwargs):
        """
        Set parameters for speaker diarization.

        Parameters
        ----------
        params : dict
            Dictionary of parameters to be used in speaker diarization.
        """
        self.params.update(kwargs)

    def generate(self, audio_file, visualize=False, **kwargs):
        """
        Perform speaker diarization on the provided audio file and visualize results if needed.

        Parameters
        ----------
        audio_file : str
            The path to the audio file.
        visualize : bool
            Whether to visualize the diarization result.
        **kwargs
            Additional arguments for the diarization process.

        Returns
        -------
        diarization result
        """
        # Update parameters for this specific call
        combined_params = {**self.params, **kwargs}

        # Perform diarization
        diarization = self.pipeline(audio_file, **combined_params)

        # Visualize the diarization results if requested
        if visualize:
            self.visualize_diarization(diarization)

        return diarization

    def visualize_diarization(self, diarization):
        """
        Visualize the diarization output using a timeline plot.

        Parameters
        ----------
        diarization : pyannote.core.Annotation
            The diarization result to be visualized.
        """
        fig, ax = plt.subplots(figsize=(15, 3))
        notebook.plot_annotation(diarization, ax=ax, time=True, legend=True)
        plt.title("Speaker Diarization")
        plt.show()
