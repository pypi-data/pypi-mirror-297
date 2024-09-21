import nemo.collections.asr as nemo_asr

from parent.interface import model


class asrmodel(model):
    """
    A class representing an ASR model for automatic speech recognition using NeMo.

    Methods
    -------
    load_model(model_path: str)
        Load the ASR model from the given path or from a pretrained model.

    generate(audio_file: str, **kwargs)
        Transcribe speech from an audio file.

    set_params(params: dict)
        Set parameters for ASR transcriptions.
    """

    def __init__(self):
        self.model = None
        self.params = {}

    def load_model(self, model_name_or_path):
        """
        Load the ASR model from a pretrained model or from a given path.

        Parameters
        ----------
        model_name_or_path : str
            The name of the pretrained model or the path to the model file.
        """
        self.model = nemo_asr.models.ASRModel.from_pretrained(model_name_or_path)
        return self

    def set_params(self, **kwargs):
        """
        Set parameters for ASR transcription.

        Parameters
        ----------
        params : dict
            Dictionary of parameters to be used in ASR transcriptions.
        """
        self.params.update(kwargs)

    def generate(self, audio_files, **kwargs):
        """
        Transcribe speech from an audio file.

        Parameters
        ----------
        audio_files : list of str
            A list of audio file paths to transcribe.

        **kwargs
            Additional arguments for transcription, if any.

        Returns
        -------
        list of str
            Transcriptions of the input audio files.
        """
        # audio_files = [audio_files]
        combined_params = {**self.params, **kwargs}
        # Example: Add any model-specific parameters here, if necessary
        # print(f"Audio files: {audio_files}")
        transcriptions = self.model.transcribe(audio_files, **combined_params)
        return transcriptions
