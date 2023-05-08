import asyncio
from collections import Counter
import time
from flask import Flask, Response, redirect, render_template, jsonify, request, url_for
from camera import *
import spotify.spotify as spotify

app = Flask(__name__)

emotions = []

def render_rec_songs_template(result):
    return render_template('rec_songs.html', emotion_dict=spotify.emotion_dict, rec_songs=result)

@app.route('/')
def index():
    result = None
    return render_rec_songs_template(result)

@app.route('/get_rec_songs')
def get_rec_songs():
    emotion = request.args.get('emotion')
    result = asyncio.run(spotify.main(emotion))
    return render_rec_songs_template(result)

def gen(camera):
    while True:
        frame, emotion = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
               b'X-Emotion: ' + emotion.encode() + b'\r\n')

# def gen(camera):
#     global emotions
#     emotions = []
#     start_time = time.time()
#     while time.time() - start_time < 5:
#         frame, emotion = camera.get_frame()
#         emotions.append(emotion)
#         yield (b'--frame\r\n'
#                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#         time.sleep(0.05) # Add a small delay to reduce CPU usage
#     print(emotions)

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_emotion')
def get_emotion():
    global emotions
    print(emotions)
    counter = Counter(emotions)
    final_emotion = counter.most_common(1)[0][0]
    return final_emotion

if __name__ == '__main__':
    app.debug = True
    app.run()