import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct
import cv2
import datetime, os

def text_to_bits(text):
    return ''.join(format(ord(c), '08b') for c in text)

def bits_to_text(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(c, 2)) for c in chars if len(c) == 8)

def embed_lsb(frame_bgr, message):
    img = frame_bgr.copy()
    msg_bits = text_to_bits(message) + '1111111111111110'  # stop marker
    flat = img.flatten()
    if len(msg_bits) > len(flat):
        raise ValueError('Message too long for this image')
    for i, bit in enumerate(msg_bits):
        flat[i] = (flat[i] & 0xFE) | int(bit)  # clear LSB, set new bit
    return flat.reshape(img.shape)

ALPHA = 25.0   # watermark strength — higher survives more compression but is more visible

def generate_watermark_key(seed=42):
    rng = np.random.RandomState(seed)
    return rng.randn(64)   # 64 pseudo-random values, same seed = same key

def embed_dct(frame_bgr, metadata_str, seed=42):
    img = frame_bgr.copy()
    # Work on the Y (luminance) channel
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    Y = ycrcb[:, :, 0].astype(np.float64)
    h, w = Y.shape
    # Embed in 8x8 blocks in the mid-frequency range
    key = generate_watermark_key(seed)
    bit_str = ''.join(format(ord(c), '08b') for c in metadata_str)
    bit_str = bit_str[:64]   # embed up to 64 bits
    block_idx = 0
    for i in range(0, h - 7, 8):
        for j in range(0, w - 7, 8):
            if block_idx >= len(bit_str): break
            block = Y[i:i+8, j:j+8]
            d = dct(dct(block.T).T)  # 2D DCT
            # Modify coefficient at mid-frequency position (3,3)
            bit = int(bit_str[block_idx])
            d[3][3] = abs(d[3][3]) * (1 if bit == 1 else -1) + ALPHA * key[block_idx]
            Y[i:i+8, j:j+8] = idct(idct(d.T).T)  # inverse DCT
            block_idx += 1
        if block_idx >= len(bit_str): break
    Y = np.clip(Y, 0, 255)
    ycrcb[:, :, 0] = Y.astype(np.uint8)
    return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

def watermark_capture(frame_bgr, camera_id, person_name, classification,
                       save_dir='data/captures', seed=42):
    ts = datetime.datetime.now()
    ts_str = ts.strftime('%Y-%m-%d %H:%M:%S')
    metadata = f'{ts_str}|CAM:{camera_id}|{person_name}|{classification}'
    watermarked = embed_dct(frame_bgr, metadata, seed=seed)
    os.makedirs(save_dir, exist_ok=True)
    filename = f'{save_dir}/{classification}_{ts.strftime("%Y%m%d_%H%M%S")}.jpg'
    # Save at high quality to preserve DCT watermark
    cv2.imwrite(filename, watermarked, [cv2.IMWRITE_JPEG_QUALITY, 90])
    return watermarked, filename, metadata
