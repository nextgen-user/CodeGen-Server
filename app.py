import os
import requests
data={}
import subprocess
from flask import Flask, request, url_for, redirect
from werkzeug.utils import secure_filename
import os
import asyncio
import traceback
import json


# Files stored in
UPLOAD_FOLDER = 'static'
 
# Allowed files extensions for upload
ALLOWED_EXTENSIONS = set(['pdf','jpg','png','csv','docx','jpeg','svg','xls','xlsx','doc','mp4','gif'])
 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
 
# Check file has an allowed extension
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route("/execute", methods=["POST"])
def execute():
    global data
    code = request.data.decode("utf-8")
    print(code)
    try:
        exec(code,globals())  
    except Exception as e:
        print(e)
        return {"Error":json.dumps(str(traceback.format_exc()))}
    return data

@app.route('/', methods=['GET','POST'])
def index():
 
    # If a post method then handle file upload
    if request.method == 'POST':
 
        if 'file' not in request.files:
            return redirect('/')
 
        file = request.files['file']
 
 
        if file :
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
 
 
    # Get Files in the directory and create list items to be displayed to the user
    file_list = ''
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        # Create link html
        link = url_for("static", filename=f) 
        file_list = file_list + '<li><a href="%s">%s</a></li>' % (link, f)
 
    # Format return HTML - allow file upload and list all available files
    return_html = '''
    <!doctype html>
    <title>Upload File</title>
    <h1>Upload File</h1>
    <form method=post enctype=multipart/form-data>
            <input type=file name=file><br>
            <input type=submit value=Upload>
    </form>
    <hr>
    <h1>Files</h1>
    <ol>%s</ol>
    ''' % file_list
 
    return return_html
 
 
