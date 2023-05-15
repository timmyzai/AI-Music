import asyncio
from collections import Counter
from datetime import datetime
import time
from flask import Flask, Response, render_template, request
from camera import *
import spotify.spotify as spotify

EMOTION_LIST_FILE = 'emotion_list.txt'
app = Flask(__name__)

@app.route('/')
def index():
    result = None
    return render_rec_songs_template(result)

@app.route('/get_rec_songs')
def get_rec_songs():
    emotion = request.args.get('emotion')
    result = asyncio.run(spotify.main(emotion))
    return render_rec_songs_template(result, emotion)

def render_rec_songs_template(result, emotion = None):
    return render_template('index.html', emotion_dict=spotify.emotion_dict, rec_songs=result, emotion=emotion)

@app.route('/video_feed')
async def video_feed():
    async for frame in gen_frames( VideoCamera()):
        return Response(frame, mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_frames(camera):
    emotions = []
    start_time = time.time()
    while True:
        if time.time() - start_time > 5:
            camera.stop_capture()
            write_emotions_data_to_file(emotions)
            break
        frame, emotion = next(camera)
        emotions.append(emotion)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.05) # Add a small delay to reduce CPU usage
        
def write_emotions_data_to_file(emotions):
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

@app.route('/get_emotion')
def get_emotion():
    final_emotion = ""
    with open(EMOTION_LIST_FILE, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('Final Emotion'):
                final_emotion = line.split(':')[-1].strip()
            else:
                raise RuntimeError("Final emotion not found in file")
    return final_emotion

if __name__ == '__main__':
    app.debug = True
    app.run()
    