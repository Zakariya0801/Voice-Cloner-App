import os
from flask import Flask, render_template, request, flash, redirect, url_for
from functionality import create_audio
from waitress import serve
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/resources'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/index')
def index():
    return render_template("main.html")

@app.route('/audioresult', methods=['POST'])
def get_audio():
    if 'audio-file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['audio-file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # return redirect(url_for('download_file', name=filename))
        text = request.args.get("input-text")
        file_loc = create_audio(filename,text)
        return f"Hello World {file_loc}"

if __name__ == "__main__":
    serve(app,host="0.0.0.0", port=3000)