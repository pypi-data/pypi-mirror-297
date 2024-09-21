# Neural_sync Library

## Overview

The Neural_sync Library provides a unified interface for working with different machine learning models across various tasks. This library aims to standardize the way models are loaded, parameters are set, and results are generated, enabling a consistent approach regardless of the model type.

## Supported Models

### Text-to-Speech (TTS)
- **FastPitch & HiFi-GAN**: Convert text to high-quality speech audio.

### Speech-to-Text (STT)
- **Distil-Large-V2**: Transcribe speech to text.
- **Openai/whisper-large-v3**: Transcribe speech to text.
- **Nemo_asr**: Transcribe speech to text.

### Speaker Diarization
- **Pyannote 3.1**: Identify and separate speakers in an audio file.

### Voice Activity Detection (VAD)
- **Silero VAD**: Detect speech segments in audio files.

### Text-to-Image Generation
- **Stable Diffusion Medium-3**: Generate images from text prompts.

### Transformers-based Models
- **llama2, llama3, llama3_1**
- **Mistralv2, Mistralv3**
- **Phi3.5 Mini**
- **AgentLM 7b**

### Quantized Models
- **LLaMA 2, LLaMA 3, LLaMA 3.1**
- **Mistral v2, Mistral v3**
- **Phi3.5 Mini**
- **AgentLM 7b**

## Installation

To install the library and its dependencies, use the following command:

```bash
pip install -r requirements.txt
```
## Usage Examples
### 1. Transformers
Transformers models are versatile and can be used for various NLP tasks. Here's an example using the LLaMA 3 model

```bash
from parent.factory import ModelFactory
model = ModelFactory.get_model("agentlm")  # No need to specify model_path
params = ModelFactory.load_params_from_json('parameters.json')
model.set_params(**params)
response = model.generate(
     prompt="What is Artificial Intelligence?",
     system_prompt="Answer in German."
 )
print(response)
```
Similarly use following string for other models of transformers:
- agentlm
- Phi3_5
- llama2
- llama3
- llama3_1
- Mistralv2
- Mistralv3



### 2. FastPitch (Text-to-Speech)

FastPitch is used for generating speech from text:
```bash
from parent.factory import ModelFactory
model = ModelFactory.get_model("fastpitch")

response = model.generate(text="Hello, this is Hasan Maqsood",output_path="Hasan.wav")
```


### 3. Voice Activity Detection (VAD)

Silero VAD is used for detecting speech timestamps in audio files:

```bash
from parent.factory import ModelFactory
model = ModelFactory.get_model("silero_vad")

response = model.generate("Youtube.wav")
print("Speech Timestamps:", response)
```

### 4. Speaker Diarization

Pyannote is used for speaker diarization:
```bash
from parent.factory import ModelFactory
model = ModelFactory.get_model("pyannote",use_auth_token="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")
response = model.generate("Hasan.wav", visualize =True)
```

### 5. Automatic Speech Recognition (Speech-To-Text)

Nemo ASR is used for transcribing audio to text:
```bash
from parent.factory import ModelFactory
model = ModelFactory.get_model("nemo_asr")
response = model.generate(audio_files=["Hasan.wav"])
print(response)
```

### 6. Distil/ Openai whsiper (Speech-To-Text)

 Distil-whisper is used for transcribing audio to text:
```bash
from parent.factory import ModelFactory
model = ModelFactory.get_model("whisper")
response = model.generate("Youtube.wav")
print("Transcription:", response)
```
 Openai-whisper is also used for transcribing audio to text:
```bash
 from parent.factory import ModelFactory
 model = ModelFactory.get_model("openai-whisper")
 response = model.generate("Youtube.wav")
 print("Transcription:", response)
```
### 7. Text-to-Image Generation

Stable Diffusion is used for generating images from text prompts:

```bash
from parent.factory import ModelFactory
model = ModelFactory.get_model("sd_medium3")
response = model.generate(prompt ="House")
image_path = "new_house.png"
response.save(image_path)
```



