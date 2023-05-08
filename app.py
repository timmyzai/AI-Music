import asyncio
from collections import Counter
from datetime import datetime
import time
import traceback
from flask import Flask, Response, render_template, request
from camera import *
import spotify.spotify as spotify

EMOTION_LIST_FILE = 'emotion_list.txt'
app = Flask(__name__)
emotions = []

@app.route('/')
def index():
    result = None
    return render_rec_songs_template(result)

@app.route('/get_rec_songs')
def get_rec_songs():
    emotion = request.args.get('emotion')
    result = asyncio.run(spotify.main(emotion))
    return render_rec_songs_template(result)

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_emotion')
def get_emotion():
    global emotions
    counter = Counter(emotions)
    total_emotions = len(emotions)
    emotion_data = []
    for emotion, count in counter.items():
        percentage = round(count / total_emotions * 100, 2)
        emotion_data.append(f"{emotion}: {percentage}%")

    final_emotion = counter.most_common(1)[0][0]

    with open(EMOTION_LIST_FILE, 'w') as f:
        f.write(f"Raw Emotion List: {emotions}\n")
        f.write(f"Processed Emotion Data: {', '.join(emotion_data)}\n")
        f.write(f"Final Emotion: {final_emotion}\n{datetime.now().isoformat()}")

    return final_emotion

def gen(camera):
    global emotions
    emotions = []
    while True:
        frame, emotion = camera.get_frame()
        emotions.append(emotion)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.05) # Add a small delay to reduce CPU usage
  

def render_rec_songs_template(result):
    return render_template('rec_songs.html', emotion_dict=spotify.emotion_dict, rec_songs=result)

if __name__ == '__main__':
    app.debug = True
    try:
        app.run()
    except SystemExit as e:
        traceback.print_exc()