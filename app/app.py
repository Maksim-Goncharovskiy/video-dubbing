import os
import shutil
import uuid

import streamlit as st

from video_dubbing import VideoDubber
from video_dubbing.utils import cpu_config, gpu_config


UPLOAD_DIR = "uploads"


def run_app():
    st.set_page_config(
        page_title="Dubbing",  
        page_icon="🎬",                     
    )
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    st.title("Видео-дубляж с английского на русский")
    st.write("Загрузите видео, выберите параметры дубляжа и получить перевод и озвучку на русском языке.")

    uploaded_file = st.file_uploader("Выберите видео", type=["mp4", "avi", "mov"])

    if uploaded_file:
        input_filename = f"{uuid.uuid4()}_{uploaded_file.name}"
        input_path = os.path.join(UPLOAD_DIR, input_filename)
    
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    
        st.video(input_path)
        st.write("**Оригинальное видео** ")

        if st.button("Перевести и озвучить"):
            with st.spinner("Идет обработка... Это займёт несколько минут"):
                output_filename = f"translated_{input_filename}"
                output_path = os.path.join(UPLOAD_DIR, output_filename)

                dubber = VideoDubber(cpu_config)
                dubber(input_path, output_path)
                
                st.success("Готово!")
                st.video(output_path)
                st.write("**Переведенное видео**")
                
                with open(output_path, "rb") as f:
                    st.download_button(
                        label="Скачать результат",
                        data=f,
                        file_name=f"translated_{uploaded_file.name}",
                        mime="video/mp4"
                    )

    shutil.rmtree(UPLOAD_DIR)


if __name__ == "__main__":
    run_app()
