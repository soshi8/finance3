# -*- coding: utf-8 -*-

from flask import Flask, render_template,request
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np


stock_data = pd.read_csv('stockchart_20180908.csv')
count_s =  len(stock_data)
owarine = stock_data['終値'].values.tolist()
successive_data = []
answers = []
for i in range(4, count_s):
    successive_data.append([owarine[i-4], owarine[i-3], owarine[i-2], owarine[i-1]])
    answers.append(owarine[i] )
    
reg = LinearRegression().fit(successive_data, answers)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('input.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':

        #フォームの値のチェック
        try:
           val1 = float(request.form['bef4'])
        except ValueError:
           return "４日前の値が数字ではありません"

        try:
           val2 = float(request.form['bef3'])
        except ValueError:
           return "３日前の値が数字ではありません"

        try:
           val3 = float(request.form['bef2'])
        except ValueError:
           return "２日前の値が数字ではありません"

        try:
           val4 = float(request.form['bef1'])
        except ValueError:
           return "１日前の値が数字ではありません"

        test_data = np.array([[val1,val2,val3,val4]])
        predicted = reg.predict(test_data)
        msg = str(predicted.tolist()[0]) + "円" 

        return render_template("result.html",val = msg)


if __name__ == '__main__':
    app.debug = True
    app.run()