from flask import Flask, request, url_for, redirect
import subprocess
import os

data={}
app = Flask(__name__)

@app.route("/execute", methods=["POST"])
def execute():
    global data
    code = request.data.decode("utf-8")
    print(code)
    try:
        exec(code,globals())  
    except Exception as e:
        print(e)
        return {"Error":str(e)}
    return data

@app.route('/')
def home():
    return 'Hello, World!'
