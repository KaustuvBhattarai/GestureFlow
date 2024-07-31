import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from time import strftime, time
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class TrainingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CNN Trainer for GestureFlow V3.3.6")
        self.root.geometry("928x704")  # Making window size with a gap of 96 pixels from all sides

        self.dataset_path = tk.StringVar()
        self.epochs = tk.IntVar(value=20)
        self.conv_layers = tk.IntVar(value=3)
        self.filters = tk.IntVar(value=32)
        self.kernel_size = tk.IntVar(value=3)
        self.dense_units = tk.IntVar(value=128)
        self.dropout_rate = tk.DoubleVar(value=0.5)

        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        title_label = ttk.Label(frame, text="CNN Trainer for GestureFlow", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=10, sticky=tk.N)

        description_label = ttk.Label(frame, text="Configure the CNN parameters, select the dataset, and start training.", wraplength=600, justify=tk.CENTER)
        description_label.grid(row=1, column=0, columnspan=3, pady=10, sticky=tk.N)

        dataset_label = ttk.Label(frame, text="Dataset Path:")
        dataset_label.grid(row=2, column=0, pady=10, sticky=tk.W)
        dataset_entry = ttk.Entry(frame, textvariable=self.dataset_path, width=50)
        dataset_entry.grid(row=2, column=1, pady=10, sticky=tk.W)
        browse_button = ttk.Button(frame, text="Browse", command=self.browse_dataset)
        browse_button.grid(row=2, column=2, pady=10, sticky=tk.W)

        epochs_label = ttk.Label(frame, text="Epochs:")
        epochs_label.grid(row=3, column=0, pady=10, sticky=tk.W)
        epochs_entry = ttk.Entry(frame, textvariable=self.epochs)
        epochs_entry.grid(row=3, column=1, pady=10, sticky=tk.W)

        conv_layers_label = ttk.Label(frame, text="Convolutional Layers:")
        conv_layers_label.grid(row=4, column=0, pady=10, sticky=tk.W)
        conv_layers_entry = ttk.Entry(frame, textvariable=self.conv_layers)
        conv_layers_entry.grid(row=4, column=1, pady=10, sticky=tk.W)

        filters_label = ttk.Label(frame, text="Filters:")
        filters_label.grid(row=5, column=0, pady=10, sticky=tk.W)
        filters_entry = ttk.Entry(frame, textvariable=self.filters)
        filters_entry.grid(row=5, column=1, pady=10, sticky=tk.W)

        kernel_size_label = ttk.Label(frame, text="Kernel Size:")
        kernel_size_label.grid(row=6, column=0, pady=10, sticky=tk.W)
        kernel_size_entry = ttk.Entry(frame, textvariable=self.kernel_size)
        kernel_size_entry.grid(row=6, column=1, pady=10, sticky=tk.W)

        dense_units_label = ttk.Label(frame, text="Dense Units:")
        dense_units_label.grid(row=7, column=0, pady=10, sticky=tk.W)
        dense_units_entry = ttk.Entry(frame, textvariable=self.dense_units)
        dense_units_entry.grid(row=7, column=1, pady=10, sticky=tk.W)

        dropout_rate_label = ttk.Label(frame, text="Dropout Rate:")
        dropout_rate_label.grid(row=8, column=0, pady=10, sticky=tk.W)
        dropout_rate_entry = ttk.Entry(frame, textvariable=self.dropout_rate)
        dropout_rate_entry.grid(row=8, column=1, pady=10, sticky=tk.W)

        start_button = ttk.Button(frame, text="Start Training", command=self.start_training)
        start_button.grid(row=9, column=0, columnspan=3, pady=20, sticky=tk.W)

        self.progress_bar = ttk.Progressbar(frame, orient='horizontal', length=300, mode='determinate')
        self.progress_bar.grid(row=10, column=0, columnspan=3, pady=10, sticky=tk.W)

        self.estimated_time_label = ttk.Label(frame, text="")
        self.estimated_time_label.grid(row=11, column=0, columnspan=3, pady=10, sticky=tk.W)

        footer_label = ttk.Label(frame, text="Last Update Issued By Kaustuv Bhattarai. 2024-07-31: 22:30:02:325065", font=("Helvetica", 10), foreground="grey")
        footer_label.grid(row=12, column=0, columnspan=3, pady=10, sticky=tk.W)

    def browse_dataset(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dataset_path.set(directory)

    def create_model(self):
        model = Sequential()
        for _ in range(self.conv_layers.get()):
            if model.layers:
                model.add(Conv2D(self.filters.get(), (self.kernel_size.get(), self.kernel_size.get()), activation='relu'))
            else:
                model.add(Conv2D(self.filters.get(), (self.kernel_size.get(), self.kernel_size.get()), activation='relu', input_shape=(64, 64, 3)))
            model.add(MaxPooling2D((2, 2)))

        model.add(Flatten())
        model.add(Dense(self.dense_units.get(), activation='relu'))
        model.add(Dropout(self.dropout_rate.get()))
        model.add(Dense(1, activation='sigmoid'))

        model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def start_training(self):
        if not os.path.exists(self.dataset_path.get()):
            messagebox.showerror("Error", f"Dataset path '{self.dataset_path.get()}' does not exist")
            return

        self.model = self.create_model()
        datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
        train_generator = datagen.flow_from_directory(
            self.dataset_path.get(),
            target_size=(64, 64),
            batch_size=32,
            class_mode='binary',
            subset='training'
        )
        validation_generator = datagen.flow_from_directory(
            self.dataset_path.get(),
            target_size=(64, 64),
            batch_size=32,
            class_mode='binary',
            subset='validation'
        )

        self.progress_bar['value'] = 0
        self.estimated_time_label['text'] = ""

        training_thread = threading.Thread(target=self.train_model, args=(train_generator, validation_generator))
        training_thread.start()

    def train_model(self, train_generator, validation_generator):
        class TrainingProgressCallback(tf.keras.callbacks.Callback):
            def __init__(self, progress_bar, estimated_time_label, epochs):
                super().__init__()
                self.progress_bar = progress_bar
                self.estimated_time_label = estimated_time_label
                self.epochs = epochs
                self.start_time = None

            def on_train_begin(self, logs=None):
                self.start_time = time()

            def on_epoch_end(self, epoch, logs=None):
                elapsed_time = time() - self.start_time
                remaining_epochs = self.epochs - (epoch + 1)
                remaining_time = remaining_epochs * (elapsed_time / (epoch + 1))
                self.estimated_time_label['text'] = f"Estimated time remaining: {int(remaining_time // 60)} minutes, {int(remaining_time % 60)} seconds"
                self.progress_bar['value'] += 100 / self.epochs
                self.progress_bar.update_idletasks()

        callback = TrainingProgressCallback(self.progress_bar, self.estimated_time_label, self.epochs.get())
        self.model.fit(
            train_generator,
            validation_data=validation_generator,
            epochs=self.epochs.get(),
            callbacks=[callback]
        )
        self.model.save("hand_detection_model.h5")
        messagebox.showinfo("Info", "Model training completed and saved as 'hand_detection_model.h5'")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingApp(root)
    root.mainloop()
