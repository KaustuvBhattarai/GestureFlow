import os
import cv2
import pyautogui
import numpy as np
import mediapipe as mp
import tkinter as tk
from tkinter import Label, Button, Frame, Entry, Text
from PIL import Image, ImageTk, ImageDraw
from time import strftime, time

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

# Global variable to track mouse control state
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


# Function to analyze gesture patterns
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

# Function to update performance metrics
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

# Function to determine hand orientation
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

# Function to determine hand position relative to the screen
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

# Function to detect hand in the image and return landmarks
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

# Function to round corners of an image
def round_corners(image, radius):
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, image.size[0], image.size[1]), radius, fill=255)
    rounded_image = Image.new('RGBA', image.size)
    rounded_image.paste(image, (0, 0), mask)
    return rounded_image

# Function to update time on the GUI
def time_update():
    string = strftime('%Y-%m-%d %H:%M:%S')
    clock_label.config(text=string)
    clock_label.after(1000, time_update)

# Function to toggle overlay display
def toggle_overlay():
    global show_overlay
    show_overlay = not show_overlay
    overlay_button.config(relief="sunken" if show_overlay else "raised")
    overlay_button.config(text="Overlay ON" if show_overlay else "Overlay OFF")

# Function to toggle coordinate display
def toggle_coords():
    global show_coords
    show_coords = not show_coords
    coords_button.config(relief="sunken" if show_coords else "raised")
    coords_button.config(text="Coords ON" if show_coords else "Coords OFF")

# Function to toggle between light and dark mode
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

# Function to update gesture count
def update_gesture_count():
    global gesture_count
    gesture_count += 1
    gesture_count_label.config(text=f"Gesture Count: {gesture_count}")

# Function to set the refresh rate for the video stream
def set_refresh_rate(rate):
    global refresh_rate
    refresh_rate = int(rate)

# Function to draw a replica of the hand on a blank canvas
def draw_hand_replica(image, hand_landmarks):
    canvas = np.ones((300, 300, 3), dtype=np.uint8) * 255
    if hand_landmarks:
        for hand in hand_landmarks:
            for lm in hand.landmark:
                cx, cy = int(lm.x * 300), int(lm.y * 300)
                cv2.circle(canvas, (cx, cy), 5, (0, 0, 0), -1)
    return canvas

# Function to check which fingers are up
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

# Main function to update the frame and process hand gestures
def update_frame():
    global start_time
    start_time = time()
    ret, frame = cap.read()

    if ret:
        hand_landmarks = detect_hand_in_image(frame, show_overlay, show_coords)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        
        hand_replica = draw_hand_replica(frame, hand_landmarks)
        hand_replica_img = Image.fromarray(hand_replica)
        hand_replica_tk = ImageTk.PhotoImage(image=hand_replica_img)
        hand_frame.imgtk = hand_replica_tk
        hand_frame.config(image=hand_replica_tk)
        
        if hand_landmarks:
            gesture = get_fingers_up(hand_landmarks)
            result_label.config(text=f"Fingers Up: {', '.join(gesture)}")
            analyze_gesture_pattern(', '.join(gesture))
        else:
            result_label.config(text="No Hand Detected")

        update_performance_metrics(hand_landmarks, start_time)
        
    lmain.after(refresh_rate, update_frame)


#Gesture control Beta
# Define a function to control the mouse pointer
def control_mouse_pointer(hand_landmarks):
    if hand_landmarks:
        for hand in hand_landmarks:
            # Use the index finger tip landmark to control the mouse pointer
            index_tip = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            screen_width, screen_height = pyautogui.size()
            mouse_x = int(index_tip.x * screen_width)
            mouse_y = int(index_tip.y * screen_height)
            pyautogui.moveTo(mouse_x, mouse_y)

# Define a function to handle mouse clicks based on gestures
def handle_mouse_clicks(gesture):
    if mouse_control_enabled:
        if "Index" in gesture and "Pinky" not in gesture:
            pyautogui.click()  # Left click
        elif "Index" in gesture and "Pinky" in gesture:
            pyautogui.rightClick()  # Right click
    else:
        log_console.insert(tk.END, "Mouse control is disabled. No action taken.\n")

# Update the main function to include mouse control
def update_frame():
    global start_time
    start_time = time()
    ret, frame = cap.read()
    if ret:
        hand_landmarks = detect_hand_in_image(frame, show_overlay, show_coords)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        
        hand_replica = draw_hand_replica(frame, hand_landmarks)
        hand_replica_img = Image.fromarray(hand_replica)
        hand_replica_tk = ImageTk.PhotoImage(image=hand_replica_img)
        hand_frame.imgtk = hand_replica_tk
        hand_frame.config(image=hand_replica_tk)
        
        if hand_landmarks:
            gesture = get_fingers_up(hand_landmarks)
            result_label.config(text=f"Fingers Up: {', '.join(gesture)}")
            analyze_gesture_pattern(', '.join(gesture))
            
            # Control the mouse pointer
            control_mouse_pointer(hand_landmarks)
            
            # Handle mouse clicks
            handle_mouse_clicks(gesture)
        else:
            result_label.config(text="No Hand Detected")

        update_performance_metrics(hand_landmarks, start_time)
        
    lmain.after(refresh_rate, update_frame)

# Function to clear the gesture analytics history
def clear_analytics_history():
    global gesture_history
    gesture_history.clear()  # Clear the gesture history dictionary
    analytics_label.config(text="Gesture Analytics:\nNo data available.")  # Update the analytics label
    log_console.insert(tk.END, "Analytics history cleared.\n")  # Log the action


# GUI Initialization
root = tk.Tk()
root.title("Hand Gesture Recognition Interface")
root.geometry("1400x800")
root.configure(bg='white')

# Create a main frame to hold all widgets
main_frame = Frame(root, bg='white')
main_frame.pack(expand=True, fill=tk.BOTH)

# Create a frame for the video feed
video_frame = Frame(main_frame, bg='white')
video_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Create a label for the video feed
lmain = Label(video_frame, bg='white')
lmain.pack()

# Create a frame for the control panel and log console
side_frame = Frame(main_frame, bg='white')
side_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create a frame for the control panel
control_panel = Frame(side_frame, bg='white')
control_panel.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

# Create control buttons and labels
overlay_button = Button(control_panel, text="Overlay ON", command=toggle_overlay, bg='white')
overlay_button.pack(side=tk.LEFT, padx=5, pady=5)

coords_button = Button(control_panel, text="Coords OFF", command=toggle_coords, bg='white')
coords_button.pack(side=tk.LEFT, padx=5, pady=5)

theme_button = Button(control_panel, text="Toggle Theme", command=toggle_theme, bg='white')
theme_button.pack(side=tk.LEFT, padx=5, pady=5)

gesture_count_label = Label(control_panel, text="Gesture Count: 0", bg='white')
gesture_count_label.pack(side=tk.LEFT, padx=5, pady=5)

# Create a button to clear analytics history
clear_analytics_button = Button(control_panel, text="Clear Analytics", command=clear_analytics_history, bg='white')
clear_analytics_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create a button to toggle mouse control
mouse_button = Button(control_panel, text="Mouse Control ON", command=toggle_mouse_control, bg='white')
mouse_button.pack(side=tk.LEFT, padx=5, pady=5)


# Create a frame for the log console
log_frame = Frame(side_frame, bg='white')
log_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create a label for the log console
log_label = Label(log_frame, text="Log Console", bg='white')
log_label.pack(side=tk.TOP, padx=5, pady=5)

# Create a text widget for the log console
log_console = Text(log_frame, wrap=tk.WORD, bg='white')
log_console.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Add widgets for performance metrics and gesture analytics
performance_label = Label(side_frame, text="Performance Metrics", bg='white')
performance_label.pack(side=tk.TOP, padx=10, pady=5)

analytics_label = Label(side_frame, text="Gesture Analytics", bg='white')
analytics_label.pack(side=tk.TOP, padx=10, pady=5)

# Create labels for time and results
clock_label = Label(root, text="", font=("Helvetica", 12), bg='white')
clock_label.pack(side=tk.TOP, anchor='e', padx=10, pady=5)
time_update()

result_label = Label(root, text="", font=("Helvetica", 16), bg='white')
result_label.pack(side=tk.TOP, pady=10)

description_label = Label(root, text="Hand Gesture Detection Results", font=("Helvetica", 14), bg='white')
description_label.pack(side=tk.TOP, pady=5)

title_label = Label(root, text="Admin CP for GestureFlow", font=("Helvetica", 18), bg='white')
title_label.pack(side=tk.TOP, pady=10)

secondary_label = Label(root, text="Update Issued by Kaustuv Bhattarai 08-01-2024", font=("Helvetica", 12), bg='white')
secondary_label.pack(side=tk.TOP, pady=5)

# Create a frame for the hand replica
hand_frame = Label(root, bg='white')
hand_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# Start video capture
cap = cv2.VideoCapture(0)
update_frame()

root.mainloop()
