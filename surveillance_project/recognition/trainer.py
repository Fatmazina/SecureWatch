import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cv2, numpy as np, os, pickle
from detection.preprocessor import preprocess_face

def train_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create(
        radius=1, neighbors=8, grid_x=8, grid_y=8
    )
    faces, labels, label_map = [], [], {}
    label_id = 0
    for person_name in os.listdir('data/faces'):
        person_dir = f'data/faces/{person_name}'
        if not os.path.isdir(person_dir):
            continue
        label_map[label_id] = person_name
        for img_file in os.listdir(person_dir):
            img = cv2.imread(f'{person_dir}/{img_file}', cv2.IMREAD_GRAYSCALE)
            if img is None: continue
            img = cv2.resize(img, (128, 128))
            faces.append(img)
            labels.append(label_id)
        label_id += 1
    recognizer.train(faces, np.array(labels))
    recognizer.save('surveillance_project/models/lbph_model.yml')
    with open('surveillance_project/models/label_map.pkl', 'wb') as f:
        pickle.dump(label_map, f)
    print(f'Trained on {len(faces)} images, {label_id} people')
    return recognizer, label_map

if __name__ == "__main__":
    train_model()
