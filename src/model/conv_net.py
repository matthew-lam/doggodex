import os
import numpy as np
from tensorflow.keras.layers import Flatten, Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Replace these dirs as needed
TRAINING_SET_DIR = os.getcwd() + '/augmented_dog_pics/training_set/' 
VALIDATION_SET_DIR = os.getcwd() + '/augmented_dog_pics/validation_set/'

IMAGE_WIDTH = 500
IMAGE_HEIGHT = 375

def run_model():
    resnet = ResNet50(include_top=False, weights="imagenet")
    resnet_output = resnet.output

    resnet_output = GlobalAveragePooling2D()(resnet_output)

    dropout = Dropout(0.15)(resnet_output)
    predictions = Dense(120, activation ='softmax')(dropout)
    model = Model(inputs = resnet.input, outputs = predictions)

    for layer in resnet.layers:
      layer.trainable = False

    # Summarise and compile model
    model.summary()
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    # Generate training and validation data with augmentations
    gen_training = ImageDataGenerator()
    training_data = gen_training.flow_from_directory(
        directory=TRAINING_SET_DIR,
        target_size=(IMAGE_HEIGHT, IMAGE_WIDTH),
        class_mode='categorical',
    )

    gen_validation = ImageDataGenerator()
    validating_data = gen_validation.flow_from_directory(
        directory=VALIDATION_SET_DIR,
        target_size=(IMAGE_HEIGHT, IMAGE_WIDTH),
        class_mode='categorical',
    )

    # Fit model
    model.fit_generator(
        training_data,
        steps_per_epoch=training_data.n // training_data.batch_size,
        epochs=15,
        validation_data=validating_data,
        validation_steps=validating_data.n // validating_data.batch_size
    )

    model.save('dog_model.h5')
