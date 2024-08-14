import os
import cv2
import pyautogui
import numpy as np
import mediapipe as mp
import tkinter as tk
from tkinter import Label, Button, Frame, Text
from PIL import Image, ImageTk, ImageDraw
from time import strftime, time
from datetime import datetime

# Mediapipe Initialization
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

current_dir = os.path.dirname(os.path.abspath(__file__))

# Global Variables
show_overlay = True
show_coords = False
dark_mode = False
gesture_count = 0
refresh_rate = 10
detection_threshold = 0.7
mouse_control_enabled = True

# Initialize variables for performance metrics
total_frames = 0
detected_frames = 0
gesture_history = {}

def toggle_mouse_control():
    global mouse_control_enabled
    mouse_control_enabled = not mouse_control_enabled  # Toggle the mouse control state
    mouse_button.config(text="Mouse Control ON" if mouse_control_enabled else "Mouse Control OFF")  # Update the button text
    log_console.insert(tk.END, f"Mouse Control {'enabled' if mouse_control_enabled else 'disabled'}.\n")  # Log the action

def analyze_gesture_pattern(gesture):
    global gesture_history

    if gesture in gesture_history:
        gesture_history[gesture] += 1
    else:
        gesture_history[gesture] = 1

    # Update the analytics section
    analytics_text = "\n".join([f"{g}: {c} times" for g, c in gesture_history.items()])
    analytics_label.config(text=f"Gesture Analytics:\n{analytics_text}")

    # Log the analysis
    log_console.insert(tk.END, f"Analyzed Gesture Pattern: {gesture}\n")

def update_performance_metrics(hand_landmarks, start_time):
    global total_frames, detected_frames

    total_frames += 1
    if hand_landmarks:
        detected_frames += 1

    accuracy = (detected_frames / total_frames) * 100
    processing_time = time() - start_time

    # Update the performance label in the GUI
    performance_label.config(text=f"Processing Time: {processing_time:.2f}s | Detection Accuracy: {accuracy:.2f}%")

    # Log performance metrics
    log_console.insert(tk.END, f"Frame Processed | Processing Time: {processing_time:.2f}s | Detection Accuracy: {accuracy:.2f}%\n")

def determine_hand_orientation(hand_landmarks):
    if hand_landmarks:
        for hand in hand_landmarks:
            wrist = hand.landmark[mp_hands.HandLandmark.WRIST]
            index_tip = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            if index_tip.y < wrist.y:
                return "Palm Facing Up"
            else:
                return "Palm Facing Down"
    return "Unknown Orientation"

def determine_hand_position(hand_landmarks):
    if hand_landmarks:
        for hand in hand_landmarks:
            wrist = hand.landmark[mp_hands.HandLandmark.WRIST]
            if wrist.x < 0.3:
                return "Left"
            elif wrist.x > 0.7:
                return "Right"
            else:
                return "Center"
    return "Unknown Position"

def detect_hand_in_image(image, overlay=True, show_coords=False):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    if results.multi_hand_landmarks and overlay:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            if show_coords:
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.putText(image, f'{id}', (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        return results.multi_hand_landmarks
    else:
        return None

def round_corners(image, radius):
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, image.size[0], image.size[1]), radius, fill=255)
    rounded_image = Image.new('RGBA', image.size)
    rounded_image.paste(image, (0, 0), mask)
    return rounded_image

def time_update():
    string = strftime('%Y-%m-%d %H:%M:%S')
    clock_label.config(text=string)
    clock_label.after(1000, time_update)

def toggle_overlay():
    global show_overlay
    show_overlay = not show_overlay
    overlay_button.config(relief="sunken" if show_overlay else "raised")
    overlay_button.config(text="Overlay ON" if show_overlay else "Overlay OFF")

def toggle_coords():
    global show_coords
    show_coords = not show_coords
    coords_button.config(relief="sunken" if show_coords else "raised")
    coords_button.config(text="Coords ON" if show_coords else "Coords OFF")

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    root.configure(bg='black' if dark_mode else 'white')
    title_label.config(bg='black' if dark_mode else 'white', fg='white' if dark_mode else 'black')
    secondary_label.config(bg='black' if dark_mode else 'white', fg='white' if dark_mode else 'black')
    result_label.config(bg='black' if dark_mode else 'white', fg='white' if dark_mode else 'black')
    description_label.config(bg='black' if dark_mode else 'white', fg='white' if dark_mode else 'black')
    clock_label.config(bg='black' if dark_mode else 'white', fg='white' if dark_mode else 'black')
    control_panel.configure(bg='black' if dark_mode else 'white')
    overlay_button.config(bg='black' if dark_mode else 'white', fg='white' if dark_mode else 'black')
    coords_button.config(bg='black' if dark_mode else 'white', fg='white' if dark_mode else 'black')
    theme_button.config(bg='black' if dark_mode else 'white', fg='white' if dark_mode else 'black')
    log_console.config(bg='black' if dark_mode else 'white', fg='white' if dark_mode else 'black')

def update_gesture_count():
    global gesture_count
    gesture_count += 1
    gesture_count_label.config(text=f"Gesture Count: {gesture_count}")

def set_refresh_rate(rate):
    global refresh_rate
    refresh_rate = int(rate)

def draw_hand_replica(image, hand_landmarks):
    canvas = np.ones((300, 300, 3), dtype=np.uint8) * 255
    if hand_landmarks:
        for hand in hand_landmarks:
            for lm in hand.landmark:
                cx, cy = int(lm.x * 300), int(lm.y * 300)
                cv2.circle(canvas, (cx, cy), 5, (0, 0, 0), -1)
    return canvas

def get_fingers_up(hand_landmarks):
    fingers_up = []
    if hand_landmarks:
        for hand in hand_landmarks:
            landmarks = [(lm.x, lm.y) for lm in hand.landmark]
            if landmarks[mp_hands.HandLandmark.THUMB_TIP][0] < landmarks[mp_hands.HandLandmark.THUMB_MCP][0]:
                fingers_up.append("Thumb")
            if landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP][1] < landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP][1]:
                fingers_up.append("Index")
            if landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP][1] < landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP][1]:
                fingers_up.append("Middle")
            if landmarks[mp_hands.HandLandmark.RING_FINGER_TIP][1] < landmarks[mp_hands.HandLandmark.RING_FINGER_PIP][1]:
                fingers_up.append("Ring")
            if landmarks[mp_hands.HandLandmark.PINKY_TIP][1] < landmarks[mp_hands.HandLandmark.PINKY_PIP][1]:
                fingers_up.append("Pinky")
    return fingers_up

def control_mouse_pointer(hand_landmarks):
    if hand_landmarks and mouse_control_enabled:
        for hand in hand_landmarks:
            index_tip = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            screen_width, screen_height = pyautogui.size()
            mouse_x = int(index_tip.x * screen_width)
            mouse_y = int(index_tip.y * screen_height)
            pyautogui.moveTo(mouse_x, mouse_y)

def handle_mouse_clicks(gesture):
    if mouse_control_enabled:
        if "Index" in gesture and "Pinky" not in gesture:
            pyautogui.click()  # Left click
        elif "Index" in gesture and "Pinky" in gesture:
            pyautogui.rightClick()  # Right click
    else:
        log_console.insert(tk.END, "Mouse control is disabled. No action taken.\n")

def update_frame():
    start_time = time()
    success, frame = cap.read()
    if not success:
        return

    frame = cv2.flip(frame, 1)
    hand_landmarks = detect_hand_in_image(frame, overlay=show_overlay, show_coords=show_coords)

    if hand_landmarks:
        orientation = determine_hand_orientation(hand_landmarks)
        position = determine_hand_position(hand_landmarks)
        fingers_up = get_fingers_up(hand_landmarks)
        result_label.config(text=f"Orientation: {orientation} | Position: {position} | Fingers Up: {', '.join(fingers_up)}")
        control_mouse_pointer(hand_landmarks)
        handle_mouse_clicks(fingers_up)
        analyze_gesture_pattern(', '.join(fingers_up))
        update_gesture_count()

    update_performance_metrics(hand_landmarks, start_time)

    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    img_tk = ImageTk.PhotoImage(round_corners(img, 10))
    lmain.img_tk = img_tk
    lmain.config(image=img_tk)
    lmain.after(refresh_rate, update_frame)


import os
from datetime import datetime
import tkinter as tk

def save_logs():
    # Get the current date and time
    current_time = datetime.now()
    # Format the filename with the date and timestamp
    log_filename = current_time.strftime("gesture_logs_%Y-%m-%d_%H-%M-%S.txt")
    # Create the full path for the log file
    log_file_path = os.path.join(current_dir, log_filename)
    
    # Retrieve the logs from the Text widget
    logs = log_console.get("1.0", tk.END)
    
    # Write the logs to the file
    with open(log_file_path, "w") as log_file:
        log_file.write(logs)
    
    # Notify the user that the logs have been saved
    log_console.insert(tk.END, f"Logs saved to {log_filename}\n")

def on_closing():
    save_logs()
    root.destroy()


# Setup the GUI
root = tk.Tk()
root.title("Hand Gesture Recognition")
root.geometry("900x700")
root.configure(bg='white')

title_label = Label(root, text="Hand Gesture Recognition", font=("Helvetica", 24), bg='white')
title_label.pack(pady=10)

secondary_label = Label(root, text="Admin Panel created by Kaustuv Bhattarai", font=("Helvetica", 12), bg='white')
secondary_label.pack(pady=5)

video_frame = Frame(root, bg='white')
video_frame.pack(pady=10)

lmain = Label(video_frame, bg='white')
lmain.pack()

hand_frame = Label(root, bg='white')
hand_frame.pack(side=tk.RIGHT, padx=10, pady=10)

result_label = Label(root, text="No gestures detected", font=("Helvetica", 14), bg='white')
result_label.pack(pady=10)

description_label = Label(root, text="Controls and Analytics", font=("Helvetica", 16), bg='white')
description_label.pack(pady=10)

control_panel = Frame(root, bg='white')
control_panel.pack(pady=5)

overlay_button = Button(control_panel, text="Overlay ON", command=toggle_overlay, bg='white')
overlay_button.pack(side=tk.LEFT, padx=5)

coords_button = Button(control_panel, text="Coords OFF", command=toggle_coords, bg='white')
coords_button.pack(side=tk.LEFT, padx=5)

theme_button = Button(control_panel, text="Dark Mode", command=toggle_theme, bg='white')
theme_button.pack(side=tk.LEFT, padx=5)

mouse_button = Button(control_panel, text="Mouse Control ON", command=toggle_mouse_control, bg='white')
mouse_button.pack(side=tk.LEFT, padx=5)

log_frame = Frame(root, bg='white')
log_frame.pack(pady=10, fill=tk.BOTH, expand=True)

log_console = Text(log_frame, wrap=tk.WORD, bg='white')
log_console.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

gesture_count_label = Label(root, text="Gesture Count: 0", font=("Helvetica", 14), bg='white')
gesture_count_label.pack(pady=10)

performance_label = Label(root, text="Processing Time: 0.00s | Detection Accuracy: 0.00%", font=("Helvetica", 14), bg='white')
performance_label.pack(pady=10)

analytics_label = Label(root, text="Gesture Analytics: \n", font=("Helvetica", 14), bg='white')
analytics_label.pack(pady=10)

clock_label = Label(root, font=('Helvetica', 12), bg='white')
clock_label.pack(pady=5)
time_update()

# Start the video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    log_console.insert(tk.END, "Error: Unable to access the camera.\n")

update_frame()


# Bind the function to the window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter main loop
root.mainloop()




