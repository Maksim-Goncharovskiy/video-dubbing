import os
import yaml
from dataclasses import dataclass, field
from importlib import resources
from typing import Dict, Any

import video_dubbing.pipelines
from video_dubbing.pipelines import *



@dataclass
class ProcessorConfig:
    stage: str = field(repr=True)
    model: type = field(repr=True)
    params: Dict[str, Any] = field(repr=True)



def load_config(config_path: str) -> Dict[str, ProcessorConfig]:
    with open(config_path, 'r', encoding='utf-8') as f:
        yaml_data = yaml.safe_load(f)
    
    pipeline = []
    for processor_data in yaml_data['pipeline']:
        model_class = getattr(video_dubbing.pipelines, processor_data['model']) 
        
        pipeline.append(
            ProcessorConfig(
                stage=processor_data['stage'],
                model=model_class,
                params=processor_data['params']
            ))
    
    return {
        'pipeline': pipeline,
        'temp-dir': yaml_data['temp-dir']
    }



def get_default_config(config_name: str) -> str:
    try:
        with resources.path("video_dubbing.configs", config_name) as config_path:
            return str(config_path)
    except:
        package_dir = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(package_dir, "configs", config_name)



CPU_CONFIG_PATH = get_default_config("cpu_config.yaml")
GPU_CONFIG_PATH = get_default_config("gpu_config.yaml")



cpu_config = load_config(CPU_CONFIG_PATH)
gpu_config = load_config(GPU_CONFIG_PATH)
