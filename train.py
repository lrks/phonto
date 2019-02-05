# 基にした情報・ソースコード
#   https://qiita.com/kazuki_hayakawa/items/c93a21313ccbd235b82b
#   http://aidiary.hatenablog.com/entry/20170108/1483876657
import os
from keras.applications.mobilenet import MobileNet
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import Input, Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
import numpy as np
import time


classes = ['photo', 'non-photo']
nb_classes = len(classes)

img_width, img_height = 150, 150

train_data_dir = 'dataset/train'
validation_data_dir = 'dataset/validation'
nb_train_samples = 1000
nb_validation_samples = 400

batch_size = 32
nb_epoch = 10

result_dir = 'results'
if not os.path.exists(result_dir): os.mkdir(result_dir)


def mobilenet_model_maker():
    input_tensor = Input(shape=(img_width, img_height, 3))
    mobilenet = MobileNet(include_top=False, weights='imagenet', input_tensor=input_tensor)

    top_model = Sequential()
    top_model.add(Flatten(input_shape=mobilenet.output_shape[1:]))
    top_model.add(Dense(256, activation='relu'))
    top_model.add(Dropout(0.5))
    top_model.add(Dense(nb_classes, activation='softmax'))

    model = Model(input=mobilenet.input, output=top_model(mobilenet.output))
    return model


def image_generator():
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        zoom_range=0.2,
        horizontal_flip=True)
    validation_datagen = ImageDataGenerator(rescale=1.0 / 255)

    train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        color_mode='rgb',
        classes=classes,
        class_mode='categorical',
        batch_size=batch_size,
        shuffle=True)

    validation_generator = validation_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        color_mode='rgb',
        classes=classes,
        class_mode='categorical',
        batch_size=batch_size,
        shuffle=True)

    return (train_generator, validation_generator)


if __name__ == '__main__':
    start = time.time()

    mobilenet_model = mobilenet_model_maker()
    for layer in mobilenet_model.layers[:72]:
        layer.trainable = False
        if "bn" in layer.name:
            layer.trainable = True

    mobilenet_model.compile(loss='binary_crossentropy',
              optimizer=optimizers.SGD(lr=1e-3, momentum=0.9),
              metrics=['accuracy'])
    train_generator, validation_generator = image_generator()

    history = mobilenet_model.fit_generator(
        train_generator,
        samples_per_epoch=nb_train_samples,
        nb_epoch=nb_epoch,
        validation_data=validation_generator,
        nb_val_samples=nb_validation_samples)
    mobilenet_model.save_weights(os.path.join(result_dir, 'finetuning.h5'))

    process_time = (time.time() - start) / 60
    print(process_time)
