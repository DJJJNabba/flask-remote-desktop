import cv2
import mss
import numpy as np
from flask import Flask, Response, request, redirect, url_for, render_template, session
from flask_session import Session
import win32api
import win32con
import ctypes
import ctypes.wintypes
from config import Config
from key_mapping import keycode_to_vk  # Import from key_mapping.py
import threading
import subprocess
import pyautogui
import os
import sys
import time

app = Flask(__name__)
app.config.from_object(Config)
Session(app)

PASSWORD = Config.PASSWORD
IMAGE_QUALITY = 50  # Default image quality
FPS = 30  # Default Frames Per Second

# Lock for thread-safe operations
settings_lock = threading.Lock()

# Screen dimensions on the server
with mss.mss() as sct:
    server_monitor = sct.monitors[1]
    server_width = server_monitor["width"]
    server_height = server_monitor["height"]

# MJPEG video streaming
def generate_frames():
    global IMAGE_QUALITY, FPS  # Use global variables for settings

    with mss.mss() as sct:
        monitor = sct.monitors[1]
        last_time = 0
        frame_duration = 1 / FPS

        while True:
            current_time = time.time()
            if current_time - last_time < frame_duration:
                time.sleep(frame_duration - (current_time - last_time))
            last_time = current_time

            img = sct.grab(monitor)
            frame = np.array(img)

            # Get mouse cursor position
            cursor_x, cursor_y = win32api.GetCursorPos()
            cursor_x -= monitor['left']
            cursor_y -= monitor['top']

            # Draw a simple red cross as the cursor on the frame
            cursor_size = 10
            color = (0, 0, 255)  # Red color in BGR
            thickness = 2

            cv2.line(frame, (cursor_x - cursor_size, cursor_y), (cursor_x + cursor_size, cursor_y), color, thickness)
            cv2.line(frame, (cursor_x, cursor_y - cursor_size), (cursor_x, cursor_y + cursor_size), color, thickness)

            # Convert frame to BGR for JPEG encoding
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            # Encode frame as JPEG with specified quality
            _, jpeg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), IMAGE_QUALITY])
            frame_data = jpeg.tobytes()

            try:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
            except GeneratorExit:
                print("Client disconnected from video feed.")
                break

def generate_audio():
    # Use FFmpeg to capture and encode audio
    ffmpeg_command = [
        'ffmpeg',
        '-f', 'dshow',
        '-i', 'audio=CABLE Output (VB-Audio Virtual Cable)',  # Ensure the device name is a string
        '-acodec', 'aac',
        '-f', 'adts',  # Use ADTS format for AAC
        '-hide_banner',  # Hide FFmpeg compilation info
        '-loglevel', 'error',  # Only show errors
        '-nostdin',  # Disable interaction
        '-'
    ]

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE

    process = subprocess.Popen(
        ffmpeg_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        startupinfo=startupinfo
    )

    while True:
        data = process.stdout.read(1024)
        if not data:
            break
        yield data

# Run audio processing in a separate thread
audio_thread = threading.Thread(target=generate_audio)
audio_thread.start()

@app.route('/audio_feed')
def audio_feed():
    return Response(generate_audio(), mimetype='audio/aac')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    global IMAGE_QUALITY, FPS  # Access global variables for settings

    password = request.form.get('password')
    quality = request.form.get('quality', 50)
    fps = request.form.get('fps', 30)
    if password == PASSWORD:
        session['authenticated'] = True
        # Set the quality and FPS as global variables
        try:
            with settings_lock:
                quality = int(quality)
                if quality < 1 or quality > 100:
                    quality = 50
                IMAGE_QUALITY = quality

                fps = int(fps)
                if fps < 1 or fps > 60:
                    fps = 30
                FPS = fps
        except ValueError:
            with settings_lock:
                IMAGE_QUALITY = 50
                FPS = 30
        return redirect(url_for('video_page'))
    else:
        return render_template('login.html', error="Incorrect password. Please try again."), 401

@app.route('/video')
def video_page():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    return render_template('video.html')

@app.route('/video_feed')
def video_feed():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Define necessary structures for SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.wintypes.WORD),
                ("wScan", ctypes.wintypes.WORD),
                ("dwFlags", ctypes.wintypes.DWORD),
                ("time", ctypes.wintypes.DWORD),
                ("dwExtraInfo", PUL)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.wintypes.LONG),
                ("dy", ctypes.wintypes.LONG),
                ("mouseData", ctypes.wintypes.DWORD),
                ("dwFlags", ctypes.wintypes.DWORD),
                ("time",ctypes.wintypes.DWORD),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.wintypes.DWORD),
                ("wParamL", ctypes.wintypes.WORD),
                ("wParamH", ctypes.wintypes.DWORD)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.wintypes.DWORD),
                ("ii", Input_I)]

def mouse_move_relative(dx, dy):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(dx=dx,
                        dy=dy,
                        mouseData=0,
                        dwFlags=win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_MOVE_NOCOALESCE,
                        time=0,
                        dwExtraInfo=ctypes.pointer(extra))
    command = Input(type=win32con.INPUT_MOUSE, ii=ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))

def mouse_click_event(event_flag):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(dx=0,
                        dy=0,
                        mouseData=0,
                        dwFlags=event_flag,
                        time=0,
                        dwExtraInfo=ctypes.pointer(extra))
    command = Input(type=win32con.INPUT_MOUSE, ii=ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))

def mouse_scroll_event(delta):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(dx=0,
                        dy=0,
                        mouseData=delta,
                        dwFlags=win32con.MOUSEEVENTF_WHEEL,
                        time=0,
                        dwExtraInfo=ctypes.pointer(extra))
    command = Input(type=win32con.INPUT_MOUSE, ii=ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))

def press_key(vk_code):
    extra = ctypes.c_ulong(0)
    scan_code = ctypes.windll.user32.MapVirtualKeyW(vk_code, 0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(wVk=0,
                        wScan=scan_code,
                        dwFlags=win32con.KEYEVENTF_SCANCODE,
                        time=0,
                        dwExtraInfo=ctypes.pointer(extra))
    x = Input(type=win32con.INPUT_KEYBOARD, ii=ii_)
    result = ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    if result == 0:
        print(f"Error sending key down event for vk_code: {vk_code}")

def release_key(vk_code):
    extra = ctypes.c_ulong(0)
    scan_code = ctypes.windll.user32.MapVirtualKeyW(vk_code, 0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(wVk=0,
                        wScan=scan_code,
                        dwFlags=win32con.KEYEVENTF_SCANCODE | win32con.KEYEVENTF_KEYUP,
                        time=0,
                        dwExtraInfo=ctypes.pointer(extra))
    x = Input(type=win32con.INPUT_KEYBOARD, ii=ii_)
    result = ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    if result == 0:
        print(f"Error sending key up event for vk_code: {vk_code}")

@app.route('/mouse_move', methods=['POST'])
def mouse_move():
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    data = request.json
    delta_x = data.get('delta_x', 0)
    delta_y = data.get('delta_y', 0)

    mouse_move_relative(int(delta_x), int(delta_y))

    return '', 204

@app.route('/mouse_click', methods=['POST'])
def mouse_click():
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    data = request.json
    button = data['button']
    action = data['action']

    if button == 'left':
        if action == 'down':
            mouse_click_event(win32con.MOUSEEVENTF_LEFTDOWN)
        elif action == 'up':
            mouse_click_event(win32con.MOUSEEVENTF_LEFTUP)
    elif button == 'right':
        if action == 'down':
            mouse_click_event(win32con.MOUSEEVENTF_RIGHTDOWN)
        elif action == 'up':
            mouse_click_event(win32con.MOUSEEVENTF_RIGHTUP)
    elif button == 'middle':
        if action == 'down':
            mouse_click_event(win32con.MOUSEEVENTF_MIDDLEDOWN)
        elif action == 'up':
            mouse_click_event(win32con.MOUSEEVENTF_MIDDLEUP)

    return '', 204

@app.route('/mouse_scroll', methods=['POST'])
def mouse_scroll():
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    data = request.json
    delta_y = data.get('delta_y', 0)

    # Invert delta_y for natural scrolling (common for touchpads)
    delta_y = -int(delta_y)

    # Windows scroll amount is in multiples of WHEEL_DELTA (usually 120)
    WHEEL_DELTA = 120
    scroll_amount = int(delta_y / abs(delta_y)) * WHEEL_DELTA if delta_y != 0 else 0

    if scroll_amount != 0:
        mouse_scroll_event(scroll_amount)

    return '', 204

@app.route('/key_press', methods=['POST'])
def key_press():
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    data = request.json
    key_code = data.get('keyCode')
    action = data.get('action')  # 'down' or 'up'

    try:
        key_code = int(key_code)

        # Debugging output
        print(f"Received key code: {key_code}, action: {action}")

        # Use pyautogui for Escape and Windows keys
        if key_code == 123:  # F12 mapped to Windows key
            if action == 'down':
                pyautogui.keyDown('winleft')
            elif action == 'up':
                pyautogui.keyUp('winleft')
        elif key_code == 121:  # F10 mapped to Escape key
            if action == 'down':
                pyautogui.keyDown('esc')
            elif action == 'up':
                pyautogui.keyUp('esc')
        else:
            vk_code = keycode_to_vk.get(key_code, None)
            if vk_code is None:
                print(f"Unhandled key code: {key_code}")
                return '', 204

            # Debugging output
            print(f"Mapped to virtual key code: {vk_code}")

            if action == 'down':
                press_key(vk_code)
            elif action == 'up':
                release_key(vk_code)
            else:
                print(f"Invalid action: {action}")  # Debugging output
    except ValueError as e:
        print(f"Error handling key: {e}")  # Debugging output

    return '', 204

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    global IMAGE_QUALITY, FPS  # Declare globals to modify
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        quality = request.form.get('quality', 50)
        fps = request.form.get('fps', 30)
        try:
            with settings_lock:
                quality = int(quality)
                if quality < 1 or quality > 100:
                    quality = 50
                IMAGE_QUALITY = quality

                fps = int(fps)
                if fps < 1 or fps > 60:
                    fps = 30
                FPS = fps
            return redirect(url_for('video_page'))  # Ensure 'video_page' route exists
        except ValueError:
            return render_template('settings.html', error="Invalid input. Please enter valid numbers.")

    return render_template('settings.html', quality=IMAGE_QUALITY, fps=FPS)

@app.route('/restart', methods=['GET'])
def restart():
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    try:
        # Execute restart.py to handle the restart
        python = sys.executable
        restart_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "restart.py")
        subprocess.Popen([python, restart_script])
        
        # Immediately redirect to /login before the server shuts down
        return redirect(url_for('login'))
    except Exception as e:
        print(f"Failed to restart application: {e}")
        return "Failed to restart application.", 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=True, debug=False)