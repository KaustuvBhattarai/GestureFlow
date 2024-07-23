"""
GestureFlow Beta V4
Real-time Hand Gesture Detection System using OpenCV and a Pretrained CNN Model
Authored by: Kaustuv Bhattarai
Date: 2024-07-23

This script uses a pretrained CNN model to detect hand gestures in real-time from a webcam feed.
It includes a graphical user interface (GUI) created with Tkinter, featuring a control panel
for toggling theme settings.

Added extra comments to make it beginner friendly and to make myself understand the code better when I have to debug it :P
With nice stuff to keep you from getting bored

Wanna make contributions? Have ideas? Mail it on: sso.encom@icloud.com
(don't litter my inbox pls)

Also Dependencies:
- tensorflow
- opencv-python
- pillow

To install dependencies, run:
pip install tensorflow opencv-python pillow
"""

import os

import os
import cv2
import numpy as np
import tensorflow as tf
import tkinter as tk
from tkinter import Label, Button, Frame
from PIL import Image, ImageTk, ImageDraw
from time import strftime

try:
    import tensorflow as tf
except ImportError:
    print("TensorFlow is not installed. Install it using 'pip install tensorflow'")

try:
    import cv2
except ImportError:
    print("OpenCV is not installed. Install it using 'pip install opencv-python'")

current_dir = os.path.dirname(os.path.abspath(__file__))
model = tf.keras.models.load_model(os.path.join(current_dir, "hand_detection_model.h5"))

def detect_hand_in_image(image):
    """
    Detects hands in the given image using a pretrained CNN model.

    Args:
        image (ndarray): The input image in BGR format.

    Returns:
        str: "Hand" if a hand is detected, otherwise "No Hand".
    """
    try:
        image_resized = cv2.resize(image, (64, 64))
        image_array = np.expand_dims(image_resized, axis=0) / 255.0
        prediction = model.predict(image_array)
        return "Hand" if prediction[0][0] > 0.5 else "No Hand"
    except Exception as e:
        print(f"Error in detect_hand_in_image: {e}")
        return "No Hand"

def round_corners(image, radius):
    """
    Rounds the corners of the given image.

    Args:
        image (PIL.Image.Image): The input image.
        radius (int): The radius of the rounded corners.

    Returns:
        PIL.Image.Image: The image with rounded corners. (Doesn't Usually work I haven't figured out why maybe needs lancos)
    """
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, image.size[0], image.size[1]), radius, fill=255)
    rounded_image = Image.new('RGBA', image.size)
    rounded_image.paste(image, (0, 0), mask)
    return rounded_image

def time():
    string = strftime('%Y-%m-%d %H:%M:%S')
    clock_label.config(text=string)
    clock_label.after(1000, time)

def toggle_theme():
    """
    
    Toggles the theme between light and dark mode. Yeah buttons look like ass in dark mode. 
    I don't care enough to fix it yayy

    """
    global dark_mode
    dark_mode = not dark_mode
    root.configure(bg='black' if dark_mode else 'white')
    title_label.config(bg='black' if dark_mode else 'white', fg='white' if dark_mode else 'black')
    secondary_label.config(bg='black' if dark_mode else 'white', fg='white' if dark_mode else 'black')
    result_label.config(bg='black' if dark_mode else 'white', fg='white' if dark_mode else 'black')
    description_label.config(bg='black' if dark_mode else 'white', fg='white' if dark_mode else 'black')
    clock_label.config(bg='black' if dark_mode else 'white', fg='white' if dark_mode else 'black')
    control_panel.configure(bg='black' if dark_mode else 'white')
    theme_button.config(bg='black' if dark_mode else 'white', fg='white' if dark_mode else 'black')

root = tk.Tk()
root.title("GestureFlow Beta")



# Set window size to nearly fullscreen with a 1-inch gap (If you're a 4 incher guy feel free to change it to 384 pixels)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width - 2 * 96
window_height = screen_height - 2 * 96
root.geometry(f"{window_width}x{window_height}+{96}+{96}")
dark_mode = False
root.configure(bg='white') # Just a racist function to set background color to white initially (WHITE SUPREMACY)

title_label = Label(root, text="GestureFlow Beta V4", font=("futura", 24, "bold"), bg='white', fg='black')
title_label.pack(pady=(10, 0))

secondary_label = Label(root, text="Real-time Hand Gesture Detection System", font=("Helvetica", 16, "italic"), bg='white', fg='black')
secondary_label.pack(pady=(0, 20))

lmain = Label(root)
lmain.pack(pady=20)

# Control panel for buttons (Men are like toasters, Women are more like Accordions - Patrick Jane)
control_panel = Frame(root, bg='white')
control_panel.pack(side="bottom", fill="x", pady=10)


# Button container for right alignment (yeah I'm quoting random quotes from the mentalist cause I'm bored af coding this piece of )

button_container = Frame(control_panel, bg='white')
button_container.pack(side="right", padx=10)


# Button to toggle theme (Cause once you go black you never go back)

theme_button = Button(button_container, text="Dark Mode", command=toggle_theme, bg='white', fg='black')
theme_button.pack(side="left", padx=10)

result_label = Label(root, text="Starting...", font=("Helvetica", 16), bg='white', fg='black')
result_label.pack(pady=20)

description_label = Label(root, text="V4 Update Issued by Kaustuv Admin at 11:55:03 07/22/24. Check system log for details.", font=("helvetica", 12), bg='white', fg='black')
description_label.pack(side="bottom", pady=20)

clock_label = Label(root, font=("Helvetica", 12), bg='white', fg='black')
clock_label.pack(side="bottom", pady=10)

time()

cap = cv2.VideoCapture(0)

def update_frame():
    ret, frame = cap.read()
    if ret:
        result = detect_hand_in_image(frame)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, update_frame)

        # Update the hand icon based on detection result (Needs the Overlay activation to run I tried making it that way and I'm too tired to revert it)

        if result == "Hand":
            icon_path = os.path.join(current_dir, "hand_icon.png")
        else:
            icon_path = os.path.join(current_dir, "no_hand_icon.png")
        
        if os.path.exists(icon_path):
            icon = Image.open(icon_path)
            icon = icon.resize((64, 64), Image.LANCZOS)
            icon = round_corners(icon, 10)
            icon = ImageTk.PhotoImage(icon)
            result_label.config(image=icon)
            result_label.image = icon
        else:
            result_label.config(text="Icon not found", image='')

update_frame()
root.mainloop()
cap.release()
cv2.destroyAllWindows()


# Don't forget to release the webcam and close OpenCV windows when done (very important learned it the hard way)