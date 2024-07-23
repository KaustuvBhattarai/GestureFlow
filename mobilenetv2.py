"""
Alternative training using MobileNetV2 model
"""

import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import MobileNetV2
from time import strftime


current_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_dir, "dataset")

if not os.path.exists(dataset_path):
    print(f"Error: Dataset path '{dataset_path}' does not exist.")
    exit()

datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_generator = datagen.flow_from_directory(
    dataset_path,
    target_size=(128, 128),
    batch_size=32,
    class_mode='binary',
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    dataset_path,
    target_size=(128, 128),
    batch_size=32,
    class_mode='binary',
    subset='validation'
)

base_model = MobileNetV2(input_shape=(128, 128, 3), include_top=False, weights='imagenet') # Load the MobileNetV2 model, and excluding the top layers

model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])


class TrainingProgressCallback(tf.keras.callbacks.Callback):
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
    epochs=10,  # edit the number of epochs as needed
    callbacks=[TrainingProgressCallback()]
)

model.save("hand_detection_model_mobilenetv2.h5")
print(f"Model training completed and saved as 'hand_detection_model_mobilenetv2.h5' at {strftime('%Y-%m-%d %H:%M:%S')}")
