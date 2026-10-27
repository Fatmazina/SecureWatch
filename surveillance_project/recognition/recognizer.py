import cv2
import pickle

def load_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('surveillance_project/models/lbph_model.yml')
    with open('surveillance_project/models/label_map.pkl', 'rb') as f:
        label_map = pickle.load(f)
    return recognizer, label_map

def recognize_face(face_gray_128, recognizer, label_map, threshold=60):
    img = (face_gray_128 * 255).astype('uint8')
    label_id, confidence = recognizer.predict(img)
    # Lower confidence = better match (LBPH distance metric)
    if confidence < threshold:
        return label_map[label_id], confidence
    else:
        return 'unknown', confidence
