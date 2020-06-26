FROM python:3.6-slim

COPY . /root

WORKDIR /root

RUN pip install torch==1.5.1+cpu -f https://download.pytorch.org/whl/torch_stable.html torchvision==0.6.1+cpu -f https://download.pytorch.org/whl/torch_stable.html flask ngrok gunicorn matplotlib numpy Pillow wtforms flask_wtf
