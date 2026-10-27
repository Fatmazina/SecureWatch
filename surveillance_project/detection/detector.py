import cv2

class FaceDetector:
    def __init__(self, model_path='models/haarcascade_frontalface_default.xml'):
        self.cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(gray, 1.1, 4)
        return faces
