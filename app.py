import asyncio
from collections import Counter
from datetime import datetime
import time
from flask import Flask, Response, render_template, request
from camera import VideoCamera
import spotify.spotify as spotify

EMOTION_LIST_FILE = 'emotion_list.txt'
app = Flask(__name__)
stop_video = False

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
def video_feed():
    with VideoCamera() as camera:
        return Response(generate_frames(camera),mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames(camera):
    global stop_video
    emotions = []
    while not stop_video:
        frame, emotion = next(camera)
        emotions.append(emotion)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.05)  # Add a small delay to reduce CPU usage
    camera.stop_capture()    
    print("Capture stopped.")
    write_emotions_data_to_file(emotions)
    print("Emotions data stored.")
    
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

def stop_video_feed():
    global stop_video
    stop_video = True

@app.route('/get_emotion')
def get_emotion():
    stop_video_feed()
    final_emotion = ""
    with open(EMOTION_LIST_FILE, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('Final Emotion'):
                final_emotion = line.split(':')[-1].strip()
        if final_emotion == '':     
            raise RuntimeError("Final emotion not found in file")
    return final_emotion

if __name__ == '__main__':
    app.debug = True
    app.run()
