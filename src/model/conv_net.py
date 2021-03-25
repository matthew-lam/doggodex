import os
import numpy as np
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from constants import IMAGE_HEIGHT, IMAGE_WIDTH

TRAINING_SET_DIR = os.getcwd() + '/augmented_dog_pics_1/training_set/'
VALIDATION_SET_DIR = os.getcwd() + '/augmented_dog_pics_1/validation_set/'

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True' # Uncomment if getting 'OMP: ERROR#15' and vice versa.


def run_model():
    model = Sequential()
    model.add(Conv2D(filters=64, kernel_size=5, activation='relu',
                     input_shape=(IMAGE_HEIGHT, IMAGE_WIDTH, 3)))
    model.add(MaxPooling2D(pool_size=5))
    model.add(Conv2D(filters=64, kernel_size=5, activation='relu'))
    model.add(MaxPooling2D(pool_size=5))
    model.add(Conv2D(filters=64, kernel_size=3, activation='relu'))
    model.add(MaxPooling2D(pool_size=3))
    model.add(Flatten())
    model.add(Dense(4, activation='relu'))
    model.add(Dense(2, activation='softmax'))

    model.summary()

    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    generator_data = ImageDataGenerator().flow_from_directory(
        directory=TRAINING_SET_DIR,
        target_size=(IMAGE_HEIGHT, IMAGE_WIDTH),
        class_mode='categorical',
    )

    model.fit_generator(
        generator_data,
        steps_per_epoch=2000 // 32,
        epochs=50,
        validation_data=VALIDATION_SET_DIR,
        validation_steps=800 // 32
    )
