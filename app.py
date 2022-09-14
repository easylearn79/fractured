#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 21:36:07 2022

@author: abdul
"""
import os
import numpy as np
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from flask import Flask , render_template  , request , send_file
from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.preprocessing.image import load_img , img_to_array
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.imagenet_utils import preprocess_input, decode_predictions



try:
    import shutil
    shutil.rmtree('uploaded / image')
    print()
except:
    pass

app = Flask(__name__)



json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("model.h5")
print("Loaded model from disk")


ALLOWED_EXT = set(['jpg' , 'jpeg' , 'png' , 'jfif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT
           
           
app.config['UPLOAD_FOLDER'] = 'image'
  
  
@app.route('/')
def home():
        return render_template("index.html")


def finds(img_path, model):
    img = load_img(img_path, target_size=(256, 256))
    x = img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)
    
    x = preprocess_input(x, mode='caffe')

    preds = model.predict(x)
    
    
    return preds


    
@app.route('/predict', methods = ['GET', 'POST'])
def upload_file(): 
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
            
        preds = finds(file_path, model)
        
        pred_class = preds.argmax(axis=-1)
        
        pred_class = int(pred_class)
        classes ={0: "Fractured", 1: "UnFractured"}

        return str("The image is classified as: "+str(classes[pred_class]))

    return None



if __name__ == "__main__":
    app.run(debug = True)