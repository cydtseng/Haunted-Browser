from fileinput import filename
from flask import Flask, render_template, request, Response, flash, redirect
from camera import Video
from whitenoise import WhiteNoise
import os
import shutil

app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app)
my_static_folders = (
    "static/css/",
    "static/uploads/",
)
for static in my_static_folders:
    app.wsgi_app.add_files(static)

app.secret_key = "notsosecret"
UPLOAD_FOLDER = 'static/uploads/'
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
    if 'imageFile' not in request.files:
        flash('No file part')
        return redirect(request.url)
    imageFile = request.files['imageFile']
    if imageFile.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if imageFile and allowed_file(imageFile.filename):
        isdir = os.path.isdir(app.config['UPLOAD_FOLDER']) 
        if isdir:
            shutil.rmtree(app.config['UPLOAD_FOLDER'])
        os.mkdir(app.config['UPLOAD_FOLDER'])
        imageFile.save(os.path.join(app.config['UPLOAD_FOLDER'], imageFile.filename))
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
