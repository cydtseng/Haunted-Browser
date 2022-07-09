from flask import Flask, render_template, request, Response
from camera import Video

app = Flask(__name__)

@app.route('/', methods= ['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def detect():
    #get the user image
    imageFile = request.files['imageFile']
    image_path = './img/' + imageFile.filename
    imageFile.save(image_path)
    return render_template('video.html')


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
