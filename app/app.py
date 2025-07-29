from video_dubbing import VideoDubber
from video_dubbing.utils import cpu_config


if __name__ == "__main__":
    dubber = VideoDubber(config=cpu_config)
    dubber(input_video_path="/home/maksim/Repos/video-dubbing/test-videos/videoplayback.mp4", output_video_path="/home/maksim/output.mp4")