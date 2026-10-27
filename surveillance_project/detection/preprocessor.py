import cv2, numpy as np

def preprocess_face(frame, box, output_size=(128, 128)):
    x, y, w, h = box
    # Add 20% margin around the face
    margin_x = int(w * 0.2)
    margin_y = int(h * 0.2)
    x1 = max(0, x - margin_x)
    y1 = max(0, y - margin_y)
    x2 = min(frame.shape[1], x + w + margin_x)
    y2 = min(frame.shape[0], y + h + margin_y)
    crop = frame[y1:y2, x1:x2]
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, output_size)
    # Normalize pixel values to 0-1 range
    normalized = resized.astype(np.float32) / 255.0
    return normalized
