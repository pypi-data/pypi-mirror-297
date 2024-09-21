from neural_sync.child.Speech_To_Text.whispermodel import whispermodel
from neural_sync.child.Speech_To_Text.nemo_asr import asrmodel
from neural_sync.child.Diarization.pyannote import SpeakerDiarizationModel
from neural_sync.child.TTS.fastpitch import TTSModel
from neural_sync.child.VAD.silero_vad import vadmodel
# from child.Quantized.quantized import quantizedmodel
from neural_sync.child.Text_To_Img.stablediffusion import diffusionmodel
from neural_sync.child.transformers.transformers_model import transformersmodel
# from parent.interface import load_params_from_json
#import osneuralsync_ai
import json
import os


class ModelFactory:
    @staticmethod
    def load_paths():
        with open('model_paths.json', 'r') as file:
            return json.load(file)

    @staticmethod
    def get_model(model_name, **kwargs):
        model_paths = ModelFactory.load_paths()
        model_path = kwargs.get('model_path', model_paths.get(model_name))

        if model_name == "pyannote":
            return SpeakerDiarizationModel().load_model(model_path, **kwargs)
        elif model_name == "nemo_asr":
            return asrmodel().load_model(model_path)
        elif model_name == "distil_whisper":
            return whispermodel().load_model(model_path)
        elif model_name == "sd_medium3":
            return diffusionmodel().load_model(model_path)
        elif model_name == "llama3_8b_instruct":
            return transformersmodel().load_model(model_path)
        elif model_name == "agentlm":
            return transformersmodel().load_model(model_path)
        elif model_name == "Phi3_5":
            return transformersmodel().load_model(model_path)
        elif model_name == "llama2":
            return transformersmodel().load_model(model_path)
        elif model_name == "Mistralv2":
            return transformersmodel().load_model(model_path)
        elif model_name == "Mistralv3":
            return transformersmodel().load_model(model_path)
        elif model_name == "llama3_1_8b_instruct":
            return transformersmodel().load_model(model_path)
        elif model_name == "fastpitch":
            return TTSModel().load_model()
        elif model_name == "silero_vad":
            return vadmodel().load_model()
        elif model_name == "openai_whisper":
            return whispermodel().load_model(model_path)
        # Add other models as needed
        else:
            raise ValueError(f"Unknown model: {model_name}")

    @staticmethod
    def load_params_from_json(json_file):
        """
        Load parameters from a JSON file.

        Parameters
        ----------
        json_file : str
            The path to the JSON file containing parameters.

        Returns
        -------
        dict
            Dictionary of parameters loaded from the JSON file.
            Returns an empty dictionary if the file is not found.
        """
        if not os.path.exists(json_file):
            print(f"Warning: {json_file} not found. Using default parameters.")
            return {}  # Return an empty dict if the file does not exist
        with open(json_file, 'r') as file:
            params = json.load(file)
        return params
