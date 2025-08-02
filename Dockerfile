FROM python:3.10-slim AS builder

WORKDIR /app

COPY requirements.txt requirements.txt


RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    apt-get install -y ffmpeg \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip && \
    apt-get purge -y --auto-remove gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

#RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu



FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/

COPY /app/app.py app.py 

COPY video_dubbing/ video_dubbing/

COPY setup.py setup.py 

RUN pip3 install -e . 


ENTRYPOINT ["streamlit run app.py"]