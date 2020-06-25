FROM python:3.6-slim

COPY . /root

WORKDIR /root

RUN pip install flask ngrok gunicorn matplotlib numpy Pillow torchvision wtforms flask_wtf 
# opencv-python torch
