import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(sys.path)

from detection.detector import FaceDetector
from recognition.recognizer import load_model
from recognition.database import init_db, log_event
from detection.preprocessor import preprocess_face
from gui.interface import App
import cv2
import datetime
import tkinter as tk

class Pipeline:
    def __init__(self):
        self.detector = FaceDetector()
        self.recognizer, self.label_map = load_model()
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        init_db()

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret: break
            annotations = []
            faces = self.detector.detect(frame)
            for (x, y, w, h) in faces:
                face_roi = preprocess_face(frame, (x, y, w, h))
                label, confidence = self.recognizer.predict(face_roi)
                person_name = self.label_map.get(label, "Unknown")

                if confidence < 100:
                    cls = person_name
                    conf = (100 - confidence) / 100
                else:
                    cls = "Unknown"
                    conf = 0.0

                path = f'data/captures/{datetime.datetime.now():%Y%m%d_%H%M%S}.jpg'
                cv2.imwrite(path, frame)
                log_event(label, 'CAM01', cls, conf, path)
                annotations.append((x, y, w, h, f'{cls} ({conf:.2f})'))

            yield frame, annotations

if __name__ == '__main__':
    pipeline = Pipeline()
    root = tk.Tk()
    gui = App(root, pipeline)
    root.mainloop()
