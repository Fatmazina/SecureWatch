import cv2
import numpy as np
from scipy.fftpack import dct
from watermark.embedder import generate_watermark_key, bits_to_text

def extract_lsb(frame_bgr):
    flat = frame_bgr.flatten()
    bits = ''.join(str(b & 1) for b in flat)
    stop = bits.find('1111111111111110')
    return bits_to_text(bits[:stop]) if stop != -1 else ''

def verify_image(image_path, seed=42):
    img = cv2.imread(image_path)
    if img is None:
        return False, 'File not found'
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    Y = ycrcb[:, :, 0].astype(np.float64)
    key = generate_watermark_key(seed)
    bits = []
    block_idx = 0
    h, w = Y.shape
    for i in range(0, h - 7, 8):
        for j in range(0, w - 7, 8):
            if block_idx >= 64: break
            block = Y[i:i+8, j:j+8]
            d = dct(dct(block.T).T)
            bits.append('1' if d[3][3] > 0 else '0')
            block_idx += 1
        if block_idx >= 64: break
    bit_str = ''.join(bits)
    chars = [bit_str[i:i+8] for i in range(0, len(bit_str), 8)]
    metadata = ''.join(chr(int(c, 2)) for c in chars if len(c) == 8)
    if '|CAM:' in metadata:
        return True, metadata
    return False, 'No valid watermark found'
