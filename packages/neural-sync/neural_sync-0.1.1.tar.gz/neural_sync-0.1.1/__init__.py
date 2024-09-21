# __init__.py
from parent.factory import ModelFactory
from .parent.factory import ModelFactory
from neural_sync.parent.factory import ModelFactory
from parent.interface import model
from parent.factory import ModelFactory
from child.Speech_To_Text.whispermodel import whispermodel
from child.Speech_To_Text.nemo_asr import asrmodel
from child.Diarization.pyannote import SpeakerDiarizationModel
from child.TTS.fastpitch import TTSModel
from child.VAD.silero_vad import vadmodel
from child.Text_To_Img.stablediffusion import diffusionmodel
from child.transformers.transformers_model import transformersmodel

__all__ = [
    'model',
    'ModelFactory',
    'whispermodel',
    'asrmodel',
    'SpeakerDiarizationModel',
    'TTSModel',
    'vadmodel',
    'diffusionmodel',
    'transformersmodel'
]
