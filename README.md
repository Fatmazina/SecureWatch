# SecureWatch

SecureWatch is a Python desktop prototype for real-time video surveillance. It
captures frames from a webcam, detects faces, recognizes enrolled people with
an OpenCV LBPH model, records recognition events in SQLite, and provides a
Tkinter interface with live annotations and alerts. The project also contains
an experimental DCT-based watermarking module for embedding capture metadata
and verifying watermarked images.

This project was developed as a university team project and is published as a
portfolio demonstration. The public repository intentionally excludes
biometric images, local databases, generated captures, trained model files,
virtual environments, and other machine-specific artifacts.
<img width="1275" height="591" alt="image" src="https://github.com/user-attachments/assets/1d933626-0492-4434-9a93-33e42b519baf" />
<img width="671" height="702" alt="image" src="https://github.com/user-attachments/assets/6f6a121e-8555-47cb-94b0-e52c737e7454" />

## What is implemented

- Haar-cascade face detection through OpenCV
- LBPH face recognition using OpenCV's contributed modules
- Webcam enrollment and model training scripts
- SQLite event and people logging
- Tkinter desktop interface with status and event display
- DCT watermark embedding and verification utilities
- Classification helpers for authorized, unauthorized, and unknown identities

The current prototype does **not** implement MTCNN, ArcFace, DeepFace,
TensorFlow, Flask, cosine-similarity classification, or a measured 30 FPS
guarantee. Those technologies should not be attributed to this version.

## Setup

1. Use Python 3.10+ and create a virtual environment.
2. Install the dependencies:

   ```text
   python -m pip install -r requirements.txt
   ```

3. Keep the commands below running from the repository root.
4. Add local enrollment images under `data/faces/<person_name>/`.
5. Train the local LBPH model:

   ```text
   python -m surveillance_project.recognition.trainer
   ```

6. Start the desktop application:

   ```text
   python -m surveillance_project.main
   ```

The trained model and local data are intentionally ignored by Git. A local
camera and an OpenCV installation with `cv2.face` support are required.

## Portfolio summary

**SecureWatch – Intelligent Video Surveillance Prototype:** University team
project. Designed and implemented a Python desktop application for webcam
face detection and LBPH-based recognition, with SQLite event logging, a
Tkinter monitoring interface, enrollment/training workflows, alert
classification, and an experimental DCT-QIM-inspired watermarking utility for
capture metadata. Built with Python, OpenCV, NumPy, Pillow, SciPy, Tkinter,
and SQLite.

## Responsible-use note

Face recognition is biometric processing. Use this prototype only with
appropriate consent, access controls, and applicable privacy protections. Do
not commit real people's face images, surveillance captures, databases, or
trained biometric models to a public repository.
