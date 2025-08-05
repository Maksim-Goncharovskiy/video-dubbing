# Video dubbing
## Table of contents
1. [About project](#title1)
   - 1.1. [Project structure](#title1.1)
   - 1.2. [Main features](#title1.2)
   - 1.3. [Output examples](#title1.3)
   - 1.4. [To do](#title1.4)
2. [Fine tuning XTTS-v2](#title2)
   - 2.1. [Dataset](#title2.1)
   - 2.2. [Fine-tuned model](#title2.2)
3. [Docs](#title3)
    - 3.1. [Installation](#title3.1)
    - 3.2. [Video dubbing module usage](#title3.2)
    - 3.3. [Streamlit demo app](#title3.3)


## <a id="title1">About project</a>
This project is about dubbing english videos into russian language. 

The main purpose is to build a solution, which can be used locally without using any API services. Therefore, to achieve this goal, I have developed video dubbing pipelines, which consist of pretrained models for each stage of dubbing:

<img width="1358" height="434" alt="Pipeline" src="https://github.com/user-attachments/assets/3854f386-e4a0-40c6-ae90-2f0c526c6a39" />

The project consists of two parts:
1. Video-dubbing `python module` with pipeline implementation and wrappers over models.
2. Simple streamlit `demo app` for user-friendly video-dubbing interface.
   
>[!NOTE]
>The developed module allows you to flexibly customize the pipeline for yourself using the config system, as well as the ability to easily add wrappers over new models.

### <a id="title1.1">Project structure</a>
```
root/
├── app/  # streamlit demo app      
└── notebooks/       
└── scripts/  # scripts for datasets processing
└── video_dubbing/
	└── core/  # basic classes
	└── pipelines/  # implementation of all stages of dubbing
	└── utils/  # extra useful thing, configs for example
	└── video_dubber.py  # API for video dubbing
```

### <a id="title1.2">Main Features</a>
1. The resulting dubbing is synchronized with the original video.
2. Easy pipeline configuration via configuration files.
3. Several options for voice synthesis: voice cloning (XTTS-v2); using a specific voice that differs from the original speaker (SileroTTS, XTTS-v2).
4. For faster inference on the CPU, you can use SileroTTS. Video-dubbing module also supports GPU usage.
5. It is easy to use your own checkpoints for any models in module. All you need is to provide a paths to your model's weights in config file (look at default configs in `video_dubbing/configs/`


### <a id="title1.3">Output examples</a>
| Original (english)                                                              | Voice Cloning (XTTS-v2)                                                         | SileroTTS (xenia)                                                               |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| <video src=https://github.com/user-attachments/assets/15be4daa-3d86-417c-8638-fc021a21a97d> | <video src=https://github.com/user-attachments/assets/ba071859-b7f6-4aba-b81b-837dd01dd76c> | <video src=https://github.com/user-attachments/assets/023d221e-8e8c-4bf2-8217-f73ad232c0d8> |
| <video src=https://github.com/user-attachments/assets/ce14f88f-2c64-46fc-a60c-f649698a39f5> | <video src=https://github.com/user-attachments/assets/97376eed-2fdf-4f3f-8710-04146243d709> | <video src=https://github.com/user-attachments/assets/9f971d95-6143-4dcc-aed1-ca77fc0ff316> |


### <a id="title1.4">To do</a>
- [ ] Logging ✍️
- [X] Reading and processing configs 📚
- [ ] Batch processing ⬆️
- [ ] Diarization for multi-speaker dubbing
- [ ] OpenAI API for high quality translation 
- [ ] OpenAI API for processing transcription before translation (numbers -> words)

_____________________________________________________________

## <a id="title2">Fine-tuning XTTS-v2</a>
Default XTTS-v2 has a few problems with russian language: 
* wrong accents
* inexpressive intonation
* sometimes there are artifacts at the end of synthesized audios.
In order to have a better TTS performance on russian language it is recommended to do fine-tuning.

You can find xtts-v2 fine-tuning example in my notebook: `notebooks/fine-tune-xtts.ipynb` 

### <a id="title2.1">Dataset</a>
For fine-tuning I used the RUSLAN dataset:
* original: https://ruslan-corpus.github.io/
* kaggle: https://www.kaggle.com/datasets/freezerainml/ruslan

It was preprocessed by script: `/scripts/process_ruslan_dataset.py`. 

You can download my preprocessed version from kaggle: https://www.kaggle.com/datasets/maksimgoncharovskiy/ruslan-preprocessed

>[!NOTE]
>You can use any other dataset, but it must be in the LJSpeech format.

### <a id="title2.2">Fine-tuned model</a>
You can download and use my checkpoint from kaggle: https://www.kaggle.com/models/maksimgoncharovskiy/xtts-v2_ruslan_134566

After you download a checkpoint you can use it in video-dubbing pipeline. All you need is to provide a path to checkpoint in config file. 

___________________________________________________________________

## <a id="title3">Docs</a>
### <a id="title3.1">I. Installation</a>
1. Clone repository
```bash
git clone https://github.com/Maksim-Goncharovskiy/video-dubbing.git
```

2. Make virtual enviroment for Python 3.10.18. You can use Miniconda:
```bash
conda create -n project_env_name python=3.10
```

3. Go to repository dir and install requirements:
```bash
pip install -r requirements.txt
```

4. Install video dubbing module
```bash
pip install -e .
```

### <a id="title3.2">II. Video dubbing module usage</a>
#### Quick start
```python
from video_dubbing import VideoDubber
from video_dubbing.utils import cpu_config, gpu_config

dubber = VideoDubber(config=cpu_config) # or gpu_config for voice cloning with XTTS

input_video_path = "input.mp4"
output_video_path = "output.mp4"

dubber(input_video_path, output_video_path)
```

#### Using your own config
Let's imagine that you want to use large-v3 whisper version and moreover you have fine-tuned version of xtts-v2. You can easily build your own video_dubbing pipeline by creating custom config file. Config file should has the same format as default config files in `video_dubbing/configs`:

```yaml
# This is our custom config file
pipeline:
  - stage: vad
    model: SileroVADProcessor
    params:
      model_path: "./models/SileroVAD/snakers4-silero-vad" # provide path if you've already downloaded model weights
      threshold: 0.5
      min_silence_duration_ms: 1000
      min_speech_duration_ms: 1000

  - stage: asr
    model: FasterWhisperProcessor
    params:
      model_size_or_path: "large-v3" # use new model size. Model weights will be downloaded.
      device: cuda
      compute_type: float32

  - stage: mt
    model: HelsinkiEnRuProcessor
    params:
      model_path: ""
      device: cpu
      
  - stage: tts
    model: XTTSProcessor
    params:
      model_path: "./models/XTTS/XTTS_ft_ruslan/" # provide path to your fine-tuned model
      device: cuda
      speaker: "./ruslan-wavs/reference.wav" # if you provide path to reference audio, the dubbing will be done by the voice of the selected speaker


temp-dir: "./video-dubbing-temp-dir"
```

>[!IMPORTANT]
>If `speaker` arg in config is not provided while using XTTS model, dubbing will be done with voice cloning.

Then use `load_config` function:
```python
from video_dubbing import VideoDubber
from video_dubbing.utils import load_config

config_path = "custom_config.yaml"
custom_config = load_config(config_path)

dubber = VideoDubber(config=cpu_config) # or gpu_config for voice cloning with XTTS

input_video_path = "input.mp4"
output_video_path = "output.mp4"

dubber(input_video_path, output_video_path)
```

Moreover there is an opportunity to construct your config directly in python:
```python
from video_dubbing import VideoDubber
from video_dubbing.utils import ProcessorConfig

config = {
    "pipeline": [
        ProcessorConfig(
            stage="vad",
            model=SileroVADProcessor,
            params={
                "model_path": "./Models/SileroVAD/snakers4-silero-vad", 
                "threshold": 0.5,  
                "min_silence_duration_ms": 1000, 
                "min_speech_duration_ms": 1000
            }
        ),
        ProcessorConfig(
            stage="asr",
            model=FasterWhisperProcessor,
            params={
                "model_size_or_path": "./Models/FasterWhisper/tiny-en", 
                "device": "cpu", 
                "compute_type": "int8"
            }
        ), 
        ProcessorConfig(
            stage="mt",
            model=HelsinkiEnRuProcessor,
            params={
                "model_path": "./Models/OpusEnRu", 
                "device": 'cpu'
            }
        ),  
        ProcessorConfig(
            stage="tts",
            model=SileroTTSProcessor,
            params={
                "model_path": "./Models/SileroModels", 
                "device": 'cpu', 
                "speaker": "xenia"
            }
        )
    ],
    "temp-dir": "./video-dubbing-temp-dir"}

dubber = VideoDubber(config=config)
```

If you are interested in adding your own models in pipeline or you want to find out how `video_dubbing` module works, please, read the `tutoral`. (not done yet)

### <a id="title3.3">III. Demo streamlit app</a>
>[!IMPORTANT]
>For now demo app uses a default CPU config for video dubbing, which means using a SileroTTS model.

<img width="400" alt="demo-app-1" src="https://github.com/user-attachments/assets/cbc3ff56-db1c-4764-86de-b2fa69ba4794" />
<img width="400" alt="demo-app-2" src="https://github.com/user-attachments/assets/c585779c-2a82-4361-9ced-edc2a1c4d02e" />

#### Run demo app with Docker
1. Build docker image
```bash
docker build -t demo-app .
```

2. Run docker container
```bash
docker run -p 8000:8501 --name demo demo-app
```
