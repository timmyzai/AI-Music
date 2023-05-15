import numpy as np
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from threading import Thread
import pandas as pd
import concurrent.futures

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

emotion_model = Sequential()
emotion_model.add(Conv2D(32, kernel_size=(
    3, 3), activation='relu', input_shape=(48, 48, 1)))
emotion_model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Dropout(0.25))
emotion_model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Dropout(0.25))
emotion_model.add(Flatten())
emotion_model.add(Dense(1024, activation='relu'))
emotion_model.add(Dropout(0.5))
emotion_model.add(Dense(7, activation='softmax'))
emotion_model.load_weights('model.h5')

cv2.ocl.setUseOpenCL(False)

emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
global last_frame1
last_frame1 = np.zeros((480, 640, 3), dtype=np.uint8)
show_text = [0]
    
class WebcamVideoStream:
    def __init__(self):
        self.stream = cv2.VideoCapture(0)
        self.stopped = False
        
    def __del__(self):
        self.stream = None

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while not self.stopped:
            ret, self.frame = self.stream.read()

    def read(self):
        return self.stream.read()

    def stop(self):
        self.stopped = True
   
class VideoCamera(object):
    def __init__(self):
        self.webcam = WebcamVideoStream()
        self.capture_frames = True

    def __del__(self):
        self.webcam.stop()

    def __next__(self):
        if self.capture_frames:
            return self.start_capture()
        else:
            self.webcam.stop()
            raise StopIteration

    def stop_capture(self):
        self.capture_frames = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.webcam.stop()

    def start_capture(self):
        image = self._read_frame()
        self._display_frame(image)
        image = cv2.resize(image, (600, 500))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
        emotions_results = self.get_emotions(gray, face_rects)
        face_info_results = self.get_face_info(image, face_rects)
        
        for result in concurrent.futures.as_completed(emotions_results + face_info_results):
            pass
        last_frame1 = image.copy()
        jpeg = self._encode_image(last_frame1)
        emotion = emotion_dict[show_text[0]]
        return jpeg, emotion

    def _read_frame(self):
        ret, image = self.webcam.read()
        if not ret:
            cv2.destroyAllWindows()
        return image

    def _display_frame(self, image):
        cv2.imshow('image', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    def get_emotions(self, gray, face_rects):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(self._detect_emotions, gray, face_rect) for face_rect in face_rects]
        return results

    def get_face_info(self, image, face_rects):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(self._draw_face_info, image, face_rect) for face_rect in face_rects]
        return results

    def _detect_emotions(self, gray, face_rect):
        (x, y, w, h) = face_rect
        roi_gray_frame = gray[y:y + h, x:x + w]
        cropped_img = cv2.resize(roi_gray_frame, (48, 48))
        cropped_img = np.expand_dims(cropped_img, axis=0)
        cropped_img = np.expand_dims(cropped_img, axis=-1)
        prediction = emotion_model.predict(cropped_img)
        show_text[0] = np.argmax(prediction)

    def _draw_face_info(self, image, face_rect):
        (x, y, w, h) = face_rect
        x_coords = np.array([x, x + w, x + 20])
        y_coords = np.array([y - 50, y + h + 10, y - 60])
        cv2.rectangle(image, (x_coords[0], y_coords[0]), (x_coords[1], y_coords[1]), (0, 255, 0), 2)
        cv2.putText(image, emotion_dict[show_text[0]], (x_coords[2], y_coords[2]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    def _encode_image(self, image):
        jpeg = cv2.imencode('.jpg', image)
        return jpeg[1].tobytes()
    