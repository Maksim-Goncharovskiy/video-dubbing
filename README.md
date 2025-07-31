# Video Dubbing
![](./readme_files/Pipeline.png)

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

## To do
- [ ] Logging ✍️
- [ ] Reading and processing configs 📚
- [ ] Batch processing ⬆️
- [ ] Diarization for multi-speaker dubbing
- [ ] OpenAI API for high quality translation 
- [ ] OpenAI API for processing transcription before translation (numbers -> words)