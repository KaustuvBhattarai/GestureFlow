import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

# Define paths
current_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_dir, "dataset")

# Image data generator for training with data augmentation
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2
)

train_generator = datagen.flow_from_directory(
    dataset_path,
    target_size=(64, 64),
    batch_size=32,
    class_mode='binary',
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    dataset_path,
    target_size=(64, 64),
    batch_size=32,
    class_mode='binary',
    subset='validation'
)

# Building the CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

# Training the model
model.fit(train_generator, validation_data=validation_generator, epochs=20)

# Save the model
model.save("hand_detection_model.h5")

# Function to detect hands in a new image
def detect_hand_in_image(model, image, threshold=0.4):  # Adjusted threshold
    image_resized = cv2.resize(image, (64, 64))
    image_array = np.expand_dims(image_resized, axis=0) / 255.0
    prediction = model.predict(image_array)
    return "Hand" if prediction[0][0] > threshold else "No Hand"

# Load the trained model
model = tf.keras.models.load_model("hand_detection_model.h5")

# GUI setup
root = tk.Tk()
root.title("Hand Detection")

lmain = Label(root)
lmain.pack()

cap = cv2.VideoCapture(0)

def update_frame():
    ret, frame = cap.read()
    if ret:
        result = detect_hand_in_image(model, frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, update_frame)
        result_label.config(text="Detected: " + result)

result_label = Label(root, text="Starting...", font=("Helvetica", 16))
result_label.pack()

update_frame()
root.mainloop()

cap.release()
cv2.destroyAllWindows()
