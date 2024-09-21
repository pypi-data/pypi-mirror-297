# # Transformers
from neuralsync_ai.parent.factory import ModelFactory
model = ModelFactory.get_model("llama3_8b_instruct")  # No need to specify model_path
params = ModelFactory.load_params_from_json('parameters.json')
model.set_params(**params)
response = model.generate(
    prompt="What is Artificial Intelligence?",
    system_prompt="You are machine learning expert."
)
print(response)
#
# # Fastpitch
# from parent.factory import ModelFactory
# model = ModelFactory.get_model("fastpitch")
#
# transcription = model.generate(text="Hello, this is Hasan Maqsood",output_path="Hasan.wav")
#
# # VAD
# from parent.factory import ModelFactory
# model = ModelFactory.get_model("silero_vad")
#
# response = model.generate("Youtube.wav")
# print("Speech Timestamps:", response)
#
# # Pyannote
# from parent.factory import ModelFactory
# model = ModelFactory.get_model("pyannote",use_auth_token="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")
# #
# response = model.generate("Hasan.wav", visualize =True)
#
# # Nemo_asr
# from parent.factory import ModelFactory
# model = ModelFactory.get_model("nemo_asr")
#
# transcription = model.generate(audio_files=["Hasan.wav"])
# print(transcription)
#
# Stable Diffusion Medium-3
# from parent.factory import ModelFactory
# model = ModelFactory.get_model("sd_medium3")
#
# image = model.generate(prompt ="House")
# image_path = "new_house.png"
# image.save(image_path)
#
# For distil-large-v2
#
# from parent.factory import ModelFactory
# # # Example usage for distil-whisper/distil-large-v2
# model = ModelFactory.get_model("distil-whisper")
#
# response = model.generate("Youtube.wav")
# print("Transcription:", response)
#
# For openai/whisper-large-v3
# from parent.factory import ModelFactory
# model = ModelFactory.get_model("openai-whisper")
#
# response = model.generate("Youtube.wav")
# print("Transcription:", response)
#
# Nemo_asr
# from parent.factory import ModelFactory
# model = ModelFactory.get_model("nemo_asr")
#
# transcription = model.generate("Hasan.wav")
# print(transcription)