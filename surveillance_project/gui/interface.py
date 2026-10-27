import tkinter as tk
from tkinter import ttk, messagebox
import cv2, threading
from PIL import Image, ImageTk

class App:
    def __init__(self, root, pipeline):
        self.root = root
        self.pipeline = pipeline
        self.running = False
        root.title('Surveillance Platform v1.0')
        root.configure(bg='#1a1a2e')
        self._build_layout()

    def _build_layout(self):
        # Left: video feed
        left = tk.Frame(self.root, bg='#1a1a2e')
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.video_label = tk.Label(left, bg='black')
        self.video_label.pack()
        # Controls
        ctrl = tk.Frame(left, bg='#1a1a2e')
        ctrl.pack(fill=tk.X, pady=6)
        self.start_btn = tk.Button(ctrl, text='Start', command=self.start,
            bg='#16a34a', fg='white', font=('Arial', 12, 'bold'), width=10)
        self.start_btn.pack(side=tk.LEFT, padx=4)
        self.stop_btn = tk.Button(ctrl, text='Stop', command=self.stop,
            bg='#dc2626', fg='white', font=('Arial', 12, 'bold'), width=10)
        self.stop_btn.pack(side=tk.LEFT, padx=4)

        # Right: status + log
        right = tk.Frame(self.root, bg='#1a1a2e', width=320)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        # Status card
        self.status_var = tk.StringVar(value='Idle')
        self.status_label = tk.Label(right, textvariable=self.status_var,
            font=('Arial', 14, 'bold'), bg='#0f3460', fg='white',
            padx=12, pady=8, width=28)
        self.status_label.pack(pady=(0,8))
        # FPS display
        self.fps_var = tk.StringVar(value='FPS: --')
        tk.Label(right, textvariable=self.fps_var, bg='#1a1a2e',
            fg='#94a3b8', font=('Arial', 11)).pack()
        # Event log
        tk.Label(right, text='Event Log', bg='#1a1a2e', fg='white',
            font=('Arial', 12, 'bold')).pack(pady=(12,4))
        self.log_text = tk.Text(right, height=25, bg='#0f172a', fg='#e2e8f0',
            font=('Courier', 10), state=tk.DISABLED, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run_pipeline, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def _run_pipeline(self):
        import time
        frame_count = 0
        t0 = time.time()
        for frame, annotations in self.pipeline.run():
            if not self.running: break
            frame_count += 1
            if time.time() - t0 > 0:
                fps = frame_count / (time.time() - t0)
                self._update_frame(frame, annotations, fps)

    def _update_frame(self, frame, annotations, fps):
        # Annotate frame with bounding boxes
        color_map = {'AUTHORIZED':(0,200,0),'UNAUTHORIZED':(0,0,255),'UNKNOWN':(0,165,255)}
        for (x, y, w, h, text) in annotations:
            color = color_map.get(text.split(' ')[0], (200,200,200))
            cv2.rectangle(frame, (x,y), (x+w,y+h), color, 2)
            cv2.putText(frame, text, (x, y-8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
        # Convert to Tkinter image
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(rgb).resize((640, 480)))
        self.video_label.configure(image=img)
        self.video_label.image = img
        self.fps_var.set(f'FPS: {fps:.1f}')

    def trigger_alert(self, classification, name, image_path):
        if classification == 'UNAUTHORIZED':
            self.status_label.config(bg='#7c2d12')
            self.status_var.set(f'ALERT: {name}')
            self._log(f'[ALERT] Known unauthorized: {name} | {image_path}')
            messagebox.showwarning('Alert', f'Known unauthorized person: {name}')
        elif classification == 'UNKNOWN':
            self.status_label.config(bg='#450a0a')
            self.status_var.set('ALARM: UNKNOWN PERSON')
            self._log(f'[ALARM] Unknown person detected | {image_path}')
            messagebox.showerror('Alarm', 'Unknown person detected!')
        else:
            self.status_label.config(bg='#14532d')
            self.status_var.set(f'Access: {name}')
            self._log(f'[OK] Authorized: {name}')

    def _log(self, msg):
        import datetime
        ts = datetime.datetime.now().strftime('%H:%M:%S')
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f'{ts} {msg}\n')
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
