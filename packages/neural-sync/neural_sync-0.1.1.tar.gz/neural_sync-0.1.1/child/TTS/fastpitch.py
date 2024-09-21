import json
import soundfile as sf
import torch
from abc import ABC, abstractmethod
from nemo.collections.tts.models import FastPitchModel, HifiGanModel

from parent.interface import model


class TTSModel(model):
    """
    A class representing a TTS model using NVIDIA NeMo for text-to-speech generation.

    Methods
    -------
    load_model(model_path: str)
        Load both the FastPitch and HiFi-GAN models.

    generate(prompt: str, **kwargs)
        Generate speech audio based on the prompt text.

    set_params(params: dict)
        Set parameters for text-to-speech generation.
    """

    def __init__(self):
        self.spec_generator = None
        self.vocoder = None
        self.params = {}

    def load_model(self, model_path=None):
        """
        Load FastPitch and HiFi-GAN models.

        Parameters
        ----------
        model_path : str, optional
            Path to the FastPitch model if custom, else load pretrained.
        """
        # Loading the FastPitch and HiFi-GAN models
        self.spec_generator = FastPitchModel.from_pretrained(model_name="nvidia/tts_en_fastpitch")
        self.vocoder = HifiGanModel.from_pretrained(model_name="nvidia/tts_hifigan")
        return self

    def set_params(self, **kwargs):
        """
        Set parameters for TTS generation.

        Parameters
        ----------
        params : dict
            Dictionary of parameters like parsing settings, vocoder params, etc.
        """
        self.params.update(kwargs)

    def generate(self, text, **kwargs):
        """
        Generate speech audio based on the input text prompt.

        Parameters
        ----------
        text : str
            The text to generate speech for.

        **kwargs
            Additional arguments for generation (optional).
        """
        # Update parameters for this specific call
        combined_params = {**self.params, **kwargs}

        # Parse and generate spectrogram
        parsed_text = self.spec_generator.parse(text)
        spectrogram = self.spec_generator.generate_spectrogram(tokens=parsed_text)

        # Convert spectrogram to audio
        audio = self.vocoder.convert_spectrogram_to_audio(spec=spectrogram)

        # Saving audio to disk
        audio_path = combined_params.get("output_path", "speech.wav")
        sf.write(audio_path, audio.to('cpu').detach().numpy()[0], 22050)

        return audio_path
