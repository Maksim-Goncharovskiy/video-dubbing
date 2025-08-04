# Video Dubbing
## About project
<img width="1358" height="434" alt="Pipeline" src="https://github.com/user-attachments/assets/3854f386-e4a0-40c6-ae90-2f0c526c6a39" />
### Main Features

### Output examples
| Original (english)                                                              | Voice Cloning (XTTS-v2)                                                         | SileroTTS (xenia)                                                               |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| <video src=https://github.com/user-attachments/assets/15be4daa-3d86-417c-8638-fc021a21a97d> | <video src=https://github.com/user-attachments/assets/ba071859-b7f6-4aba-b81b-837dd01dd76c> | <video src=https://github.com/user-attachments/assets/d420c94e-aa70-4a29-b9b6-c026d39689c4> |
| <video src=https://github.com/user-attachments/assets/ce14f88f-2c64-46fc-a60c-f649698a39f5> | <video src=https://github.com/user-attachments/assets/97376eed-2fdf-4f3f-8710-04146243d709> | <video src=https://github.com/user-attachments/assets/9f971d95-6143-4dcc-aed1-ca77fc0ff316> |

## To do
- [ ] Logging ✍️
- [ ] Reading and processing configs 📚
- [ ] Batch processing ⬆️
- [ ] Diarization for multi-speaker dubbing
- [ ] OpenAI API for high quality translation 
- [ ] OpenAI API for processing transcription before translation (numbers -> words)


## Project structure
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


## Dev mode instruction
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

## Fine-tuning XTTS-v2
### Dataset
For fine-tuning I used the RUSLAN dataset. It was preprocessed by script: `/scripts/process_ruslan_dataset.py`

You can download preprocessed version from kaggle: https://www.kaggle.com/datasets/maksimgoncharovskiy/ruslan-preprocessed

### Fine-tuned model
You can download and use my checkpoint from kaggle: https://www.kaggle.com/models/maksimgoncharovskiy/xtts-v2_ruslan_134566

After you download a checkpoint you can use it in video-dubbing pipeline. All you need is to provide a path to checkpoint in config file. 


## Demo Streamlit app
For now demo app uses a default CPU config for video dubbing, which means using a SileroTTS model.

<img width="868" height="987" alt="demo-app-1" src="https://github.com/user-attachments/assets/cbc3ff56-db1c-4764-86de-b2fa69ba4794" />
<img width="847" height="710" alt="demo-app-2" src="https://github.com/user-attachments/assets/c585779c-2a82-4361-9ced-edc2a1c4d02e" />

### Run with Docker
```bash
docker build -t demo-app .

docker run -p 8000:8501 --name demo demo-app
```

