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
app.secret_key = "your_secret_key"

host = "database-1.c1u44syskgrt.ap-northeast-2.rds.amazonaws.com" #mysql workbench에 연결할 때 썼던 그 aws엔드포인트입니다.
port = 3306 #포트번호는 손대지않으셨다면 3306 고정
username = "admin" #rds 만드실 때 입력하셨던 이름
database = "Chan" #RDS DB내에서 연결하고싶은 데이터베이스 이름입니다.
#workbench연결만 하신분들은 workbench에 들어가서 연결해둔 aws rds에 접속하여 CREATE DATABASE name 하시면 생성됩니다.
password = "kch43214782"

def connect_to_mysql():
    conn = pymysql.connect(host=host, port=port, user=username, passwd=password, db=database, charset='utf8')
    cursor = conn.cursor()
    return conn, cursor


@app.route('/', methods=['GET', 'POST'])
def main():
    error = None

    if request.method == 'POST':
        U_id = request.form['U_id']
        U_pw = request.form['U_pw']
 
        conn, cursor = connect_to_mysql()
        cursor = conn.cursor()
        sql = "SELECT U_id FROM login WHERE U_id = %s AND U_pw = %s"
        value = (U_id, U_pw)
        cursor.execute("set names utf8")
        cursor.execute(sql, value)

        data = cursor.fetchall()
        cursor.close()
        conn.close()
 
        for row in data:
            data = row[0]
 
        if data:
            session['login_user'] = U_id
            return redirect(url_for('home'))
        else:
            error = 'invalid input data detected !'
    return render_template('main.html', error = error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        U_id = request.form['U_id']
        U_pw = request.form['U_pw']
        conn, cursor = connect_to_mysql()
        cursor = conn.cursor()
 
        sql = "INSERT INTO login (U_id, U_pw) VALUES (%s, %s)" 
        cursor.execute(sql,(U_id, U_pw))
        conn.commit()
        print("로그인 데이터가 성공적으로 삽입되었습니다.")

        data = cursor.fetchall()
 
        if not data:
            conn.commit()
            return redirect(url_for('main'))
        else:
            conn.rollback()
            return "Register Failed"
 
        cursor.close()
        conn.close()
    return render_template('register.html', error=error)
 
@app.route('/home', methods=['GET', 'POST'])
def home():
    error = None
    U_id = session['login_user']
    return render_template('home.html', error=error, U_id=U_id)

# ===============================
# 이미지 디렉토리 경로
img_dir = 'C:/CH_Project/자세교정/Model'
model_path = os.path.join(img_dir, 'CNN_model.h5')
model = tf.keras.models.load_model(model_path)

# 이미지 전처리 함수
def preprocess_image(img):
    img = tf.image.resize(img, (32, 32), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    return img

# 이미지 분류 함수
def classify_image(img):
    # 이미지 전처리
    processed_image = preprocess_image(img)
    # 이미지를 모델에 입력하여 예측 수행
    prediction = model.predict(tf.expand_dims(processed_image, axis=0))
    predicted_class = np.argmax(prediction, axis=1) + 1
    return predicted_class

# --------------------------------
@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return 'No file part'
    
    # 클라이언트로부터 이미지를 받음
    image_file = request.files['image']
    
    # 이미지 파일을 numpy 배열로 변환
    nparr = np.frombuffer(image_file.read(), np.uint8)
    
    # numpy 배열을 OpenCV 이미지로 변환
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # 이미지를 분류하여 클래스 예측
    predicted_classes = classify_image(img)
    
    # 클래스 수 세기
    class_counts = Counter(predicted_classes)
    count_4 = class_counts.get(4, 0)
    
    # 등급 지정
    if count_4 >= 30:
        grade = 'F'
    elif count_4 >= 25:
        grade = 'E'
    elif count_4 >= 20:
        grade = 'D'
    elif count_4 >= 15:
        grade = 'C'
    elif count_4 >= 10:
        grade = 'B'
    else:
        grade = 'A'

    return render_template('home.html', grade=grade)

    # 예측된 클래스와 등급을 JSON 형식으로 반환
    # return jsonify({'grade': grade})  # 예측된 클래스 : 'predicted_classes': predicted_classes.tolist(),



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5052)