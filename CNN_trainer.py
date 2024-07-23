"""
Hand Gesture Detection Model Training
Authored by: Kaustuv Bhattarai
Date: 2024-07-23

This script trains CNN to detect hand gestures from a dataset of images. And the trained model is saved as a .h5 file. 

"""

import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from time import strftime

current_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_dir, "dataset")


if not os.path.exists(dataset_path):
    print(f"Error: Dataset path '{dataset_path}' does not exist bro")
    exit()

datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

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


model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy']) #model compilation


class TrainingProgressCallback(tf.keras.callbacks.Callback): # Made custom callback for displaying training progress wow lol
    def on_epoch_end(self, epoch, logs=None):
        accuracy = logs.get('accuracy')
        val_accuracy = logs.get('val_accuracy')
        loss = logs.get('loss')
        val_loss = logs.get('val_loss')
        print(f"\nEpoch {epoch + 1}/{self.params['epochs']}")
        print(f"Accuracy: {accuracy:.4f} - Validation Accuracy: {val_accuracy:.4f}")
        print(f"Loss: {loss:.4f} - Validation Loss: {val_loss:.4f}")


print(f"Starting training at {strftime('%Y-%m-%d %H:%M:%S')}")
model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=1, #Increase the value to 20 ish for good result : )
    callbacks=[TrainingProgressCallback()]
)

model.save("hand_detection_model.h5")
print(f"Model training completed and saved as 'hand_detection_model.h5' at {strftime('%Y-%m-%d %H:%M:%S')}")
