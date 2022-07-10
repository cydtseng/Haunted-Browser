from fileinput import filename
from flask import Flask, render_template, request, Response, flash, redirect
from camera import Video
import os
import shutil

app = Flask(__name__)

app.secret_key = "notsosecret"
UPLOAD_FOLDER = 'static/uploads/'
SCARE_FOLDER = 'static/scare/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'webp'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods= ['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def detect():
    print(request.files)
    # if 'imageFile' or 'scareFile' not in request.files:
    #     flash('No file part')
    #     return redirect(request.url)
    imageFile = request.files['imageFile']
    scareFile = request.files['scareFile']
    if imageFile.filename == '':
        flash('No user image selected.')
        return redirect(request.url)
    if scareFile.filename == '':
        flash('No scare image selected.')
        return redirect(request.url)
    if imageFile and allowed_file(imageFile.filename) and allowed_file(scareFile.filename):
        isdir = os.path.isdir(app.config['UPLOAD_FOLDER']) 
        isScareDir = os.path.isdir(SCARE_FOLDER)
        if isdir:
            shutil.rmtree(app.config['UPLOAD_FOLDER'])
        if isScareDir:
             shutil.rmtree(SCARE_FOLDER)
        os.mkdir(app.config['UPLOAD_FOLDER'])
        os.mkdir(SCARE_FOLDER)
        imageFile.save(os.path.join(app.config['UPLOAD_FOLDER'], imageFile.filename))
        scareFile.save(os.path.join(SCARE_FOLDER, scareFile.filename))
        return render_template('video.html')
    else :
        flash('Allowed image types are - png, jpg, jpeg, webp')
        return redirect(request.url)


def render(camera):
    while True:
        frame=camera.get_frame()
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')

@app.route('/video')
def video():
    return Response(render(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(port=3000, debug=True)
