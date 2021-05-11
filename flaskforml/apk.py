from flask import Flask, render_template,request,redirect,url_for 
from pymongo import MongoClient
from datetime import datetime
import pickle
import numpy as np
import sqlite3
import pandas as pd

import nltk
import string
import matplotlib.pyplot as plt

from sklearn.utils import resample
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

client=MongoClient('mongodb://localhost:27017')
db=client.get_database('pavan')
login=db.login
reviews=db.review
analysis1=db.analysis
apk=Flask(__name__)



@apk.route("/")
def imfin():
    return  render_template("base2.html")

@apk.route("/log",methods=["POST","GET"])
def loginset():
    if request.method=='POST' and 'usermail' in request.form and 'password' in request.form and 'mail' in request.form  and 'sub' in request.form:
        user=request.form.get('usermail')
        password=request.form.get('password')
        if user=='admin' and password=='1234':
            rev=reviews.find({},{ "_id":0, "Name":1, "Item":1, "Review":1,"Entry_time":1 ,"Entry_date":1}).sort("_id",-1)
            return render_template('admin.html',reslt=rev)
        else:
            login.insert_many([{"Name":user,"password":password}])
            ver=reviews.find({},{ "_id":0, "Name":1, "Item":1, "Review":1,"Entry_time":1 ,"Entry_date":1}).sort("_id",-1)
            return render_template('base.html',vers=ver)
    

@apk.route("/insert",methods=["POST","GET"])
def home_page1():
    
    if request.method=='POST' and 'user' in request.form and 'review' in request.form and 'item' in request.form and 'sub' in request.form:
        user=request.form.get('user')
        item=request.form.get('item')
        review=request.form.get('review')
        timing=datetime.now()
        timingdate=timing.strftime("%x")
        timingtime=timing.strftime("%X")
        reviews.insert_many([{"Name":user,"Item":item,"Review":review,"Entry_time":timingtime,"Entry_date":timingdate}])
        
        vectorizer = pickle.load(open("vect.pkl", "rb"))
        ve= pickle.load(open("logetest.pkl", "rb"))
        gg = vectorizer.transform([review])

        fg  =  ve.predict(gg)
        fg=str(fg[0])
        fg=int(fg)
        
        analysis1.insert_many([{"result":fg}])
        
        return render_template("thank.html")
    else: 
        
        return render_template("base.html",online="enter the details")



if __name__ == "__main__":    

    apk.run(debug=True)   