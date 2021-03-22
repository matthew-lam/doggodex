import os
import numpy as np
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from constants import IMAGE_HEIGHT, IMAGE_WIDTH

DOG_PIC_DIR = os.getcwd() + '/augmented_dog_pics_1/'
validation_dir = os.getcwd() + '/validation_dog_pics/'

os.environ['KMP_DUPLICATE_LIB_OK']='True' # Uncomment if getting 'OMP: ERROR#15' and vice versa.

def run_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(IMAGE_HEIGHT, IMAGE_WIDTH, 3)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(Flatten())
    model.add(Dense(2, activation='softmax'))

    model.summary()

    model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

    generator_data = ImageDataGenerator().flow_from_directory(
        directory=DOG_PIC_DIR,
        target_size=(IMAGE_HEIGHT, IMAGE_WIDTH),
        class_mode='categorical',
    )

    model.fit_generator(
        generator_data,
        steps_per_epoch=2000 // 32,
        epochs=50,
        validation_data=validation_dir,
        validation_steps=800 // 32
    )
