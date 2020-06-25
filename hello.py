from collections import namedtuple

from flask import Flask, render_template, send_file, redirect

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import torch
import torchvision
# import cv2
import os
import io
import urllib


torch.nn.Module.dump_patches = True
model = torch.load('models/maskRCNN.pt', map_location='cpu')
model.eval()



def plot_masks(numpy_img, preds):
    masks = preds['masks'].detach().numpy()
    for mask in masks:
        mask = (np.rollaxis(mask, 0, 3)* 255).astype(np.float32)
        numpy_img = numpy_img + mask
        numpy_img[numpy_img>255] = 255
        numpy_img[numpy_img<0] = 0

    numpy_img = Image.fromarray(numpy_img.astype(np.uint8))
    return numpy_img

def plot_preds(numpy_img, preds):
    boxes = preds['boxes'].detach().numpy()

    for box in boxes:
        numpy_img = Image.fromarray(numpy_img)
        draw = ImageDraw.Draw(numpy_img)
        draw.rectangle(((box[0],box[1]), (box[2],box[3])), fill=None, outline = 'red')
        numpy_img = np.array(numpy_img)

    numpy_img = Image.fromarray(numpy_img)
    return numpy_img




app = Flask(__name__)


SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
TEMPLATES_AUTO_RELOAD = True

@app.route('/')
def index():
    print('hi')
    return render_template('index.html')

@app.route('/main')
def main():
    return '<h1>Main page</h1>' #render_template('main.html', messages = messages)

@app.route('/load_data')
def load():

    resource = urllib.request.urlopen('https://thumbs.dreamstime.com/z/%D1%81%D0%B5%D1%80%D0%B8%D0%B8-%D0%B8%D0%B4%D1%8F-%D0%BB%D1%8E%D0%B4%D0%B5%D0%B9-%D0%B2-%D1%83%D0%BB%D0%B8%D1%86%D0%B5-%D0%BE%D0%BA%D1%81%D1%84%D0%BE%D1%80%D0%B4%D0%B0-%D0%BB%D0%BE%D0%BD%D0%B4%D0%BE%D0%BD%D0%B5-101417496.jpg')
    out = open("static/pics/img_loaded.jpg", 'wb')
    out.write(resource.read())
    out.close()
    return '<h1>loading</h1>' 

# from flask_wtf.file import FileField, FileRequired
class LinkForm(FlaskForm):
    link = StringField('link to the picture', validators=[DataRequired()])

@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = LinkForm()
    if form.validate_on_submit():
        if os.path.isfile('static/pics/img_loaded.jpg') != False:
            os.remove('static/pics/img_loaded.jpg')
        resource = urllib.request.urlopen(form.link.data)
        out = open("static/pics/img_loaded.jpg", 'wb')
        out.write(resource.read())
        out.close()
        return redirect('/detect')

    return render_template('submit.html', form=form)





@app.route('/show')
def show():
    return '<img src="/static/pics/img_loaded.jpg" alt="NY_people">'


@app.route('/detect')
def detect():

    img_numpy = Image.open("static/pics/img_loaded.jpg")
    img_numpy = np.array(img_numpy)
    img = torch.from_numpy(img_numpy.astype('float32')).permute(2,0,1)
    img = img / 255.
    


    with torch.no_grad():
        predictions = model(img[None,...])

    mask = Image.fromarray(predictions[0]['masks'][0, 0].mul(255).byte().numpy())
    
    img_with_boxes = plot_preds(img_numpy, predictions[0])
    img_with_masks = plot_masks(img_numpy, predictions[0])
    img_all = plot_preds(np.array(img_with_masks), predictions[0])
    img_with_boxes.save('static/pics/detection_img.jpg', format= 'JPEG')
    img_with_masks.save('static/pics/mask.jpg', format= 'JPEG')
    img_all.save('static/pics/segmentation_and_detection.jpg', format= 'JPEG')
    
    return '<img src="/static/pics/detection_img.jpg" alt="NY_people">'

@app.route('/boxes')
def draw_boxes():
    return '<img src="/static/pics/detection_img.jpg" alt="NY_people">'

@app.route('/masks')
def draw_masks():
    return '<img src="/static/pics/mask.jpg" alt="NY_people">'

@app.route('/result')
def draw_all():
    return '<img src="/static/pics/segmentation_and_detection.jpg" alt="NY_people">'



    