import sys
import os
import requests
import base64
import pandas as pd
import csv, pymysql, logging

from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)


host = "database-1.c1u44syskgrt.ap-northeast-2.rds.amazonaws.com" #mysql workbench에 연결할 때 썼던 그 aws엔드포인트입니다.
port = 3306 #포트번호는 손대지않으셨다면 3306 고정
username = "admin" #rds 만드실 때 입력하셨던 이름
database = "Chan" #RDS DB내에서 연결하고싶은 데이터베이스 이름입니다.
#workbench연결만 하신분들은 workbench에 들어가서 연결해둔 aws rds에 접속하여 CREATE DATABASE name 하시면 생성됩니다.
password = "kch43214782"



@app.route('/')
def main():
    error = None
    return "Hello Flask"









if __name__ == "__main__":
    app.run(debug=True)