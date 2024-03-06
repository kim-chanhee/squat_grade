import sys
import os
import requests
import base64
import pandas as pd
import csv, pymysql, logging
import numpy as np
import cv2
from flask import Flask, request, jsonify
import tensorflow as tf
from collections import Counter
from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)


# 이미지 디렉토리 경로 지정
image_folder = 'camImage'

# 모델 경로
model_path = 'C:/CH_Project/자세교정/Model/CNN_model.h5'
model = tf.keras.models.load_model(model_path)

# 이미지 전처리 함수
def preprocess_image(img):
    img = cv2.resize(img, (32, 32))
    # img = img / 255.0
    return img

# 이미지 분류 함수
def classify_image(img):
    processed_image = preprocess_image(img)
    prediction = model.predict(np.expand_dims(processed_image, axis=0))
    predicted_class = np.argmax(prediction, axis=1) + 1
    return predicted_class

for filename in os.listdir(image_folder):
    print(filename)
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        img_path = os.path.join(image_folder, filename)
        print(img_path)
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        print(img.shape)
        predicted_class = classify_image(img)
        print(f'File: {filename}, Predicted class: {predicted_class}')
        # 여기에서 데이터베이스에 결과 저장 로직 추가
