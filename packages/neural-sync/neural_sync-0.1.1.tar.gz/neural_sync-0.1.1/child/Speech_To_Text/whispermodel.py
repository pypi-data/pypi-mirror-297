import io
import numpy as np
import torch
from pydub import AudioSegment
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

from parent.interface import model


class whispermodel(model):
    """
    A class representing a Whisper ASR model using Hugging Face Transformers.

    Methods
    -------
    load_model(model_path: str)
        Load the model and processor from the given path.

    predict(audio_file_path: str)
        Transcribe audio from a file path and return the transcription.

    set_params(params: dict)
        Set parameters for transcription from a dictionary.
    """

    def __init__(self):
        self.model = None
        self.processor = None
        self.pipe = None
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.params = {}

    def load_model(self, model_path):
        """
        Load the model and processor from the given path.

        Parameters
        ----------
        model_path : str
            The path to the model directory.
        """
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_path, torch_dtype=self.torch_dtype, low_cpu_mem_usage=True
        )
        self.model.to(self.device)

        self.processor = AutoProcessor.from_pretrained(model_path)
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            max_new_tokens=128,
            torch_dtype=self.torch_dtype,
            device=self.device,
        )
        return self

    def set_params(self, **kwargs):
        """
        Set parameters for transcription from a dictionary.

        Parameters
        ----------
        params : dict
            Dictionary of parameters to be used in transcription.
        """
        self.params.update(kwargs)

    def generate(self, audio_file_path):
        """
        Transcribe audio from a file path and return the transcription.

        Parameters
        ----------
        audio_file_path : str
            The path to the audio file to be transcribed.
        """
        audio_array = self.load_audio_from_file(audio_file_path)
        result = self.pipe(audio_array)
        return result["text"]

    def load_audio_from_file(self, file_path):
        audio = AudioSegment.from_file(file_path)
        audio = audio.set_frame_rate(16000)
        audio = audio.set_channels(1)
        audio = audio.set_sample_width(2)
        audio = audio.get_array_of_samples()
        return np.array(audio, dtype=np.float32)
