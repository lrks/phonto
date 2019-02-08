# https://qiita.com/kazuki_hayakawa/items/c93a21313ccbd235b82b
# http://aidiary.hatenablog.com/entry/20170108/1483876657
import os,sys
import numpy as np
from keras.applications.mobilenet import MobileNet
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import Input, Activation, Dropout, Flatten, Dense
from keras.preprocessing import image
from keras import optimizers

class Phonto:
    def __init__(self, classes, img_size, result_dir):
        self.classes = classes
        self.nb_classes = len(classes)
        self.img_width = img_size[0]
        self.img_height = img_size[1]
        self.result_dir = result_dir
        if not os.path.exists(result_dir): os.mkdir(result_dir)
        self.save_filename = 'finetuning.h5'

    def __load_model(self):
        input_tensor = Input(shape=(self.img_width, self.img_height, 3))
        mobilenet = MobileNet(include_top=False, weights='imagenet', input_tensor=input_tensor)
        top_model = Sequential()
        top_model.add(Flatten(input_shape=mobilenet.output_shape[1:]))
        top_model.add(Dense(256, activation='relu'))
        top_model.add(Dropout(0.5))
        top_model.add(Dense(self.nb_classes, activation='softmax'))
        return Model(input=mobilenet.input, output=top_model(mobilenet.output))

    def __compile_model(self, model):
        model.compile(loss='binary_crossentropy',
            optimizer=optimizers.SGD(lr=1e-3, momentum=0.9), metrics=['accuracy'])


    def train(self, train_data, validation_data, batch_size, nb_epoch):
        train_data_dir = train_data[0]
        nb_train_samples = train_data[1]
        validation_data_dir = validaton_data[0]
        nb_validation_samples = validation_data[1]

        def image_generator():
            train_datagen = ImageDataGenerator(
                rescale=1.0 / 255,
                zoom_range=0.2,
                horizontal_flip=True)
            validation_datagen = ImageDataGenerator(rescale=1.0 / 255)
            train_generator = train_datagen.flow_from_directory(
                train_data_dir,
                target_size=(self.img_width, self.img_height),
                color_mode='rgb',
                classes=self.classes,
                class_mode='categorical',
                batch_size=batch_size,
                shuffle=True)
            validation_generator = validation_datagen.flow_from_directory(
                validation_data_dir,
                target_size=(self.img_width, self.img_height),
                color_mode='rgb',
                classes=self.classes,
                class_mode='categorical',
                batch_size=batch_size,
                shuffle=True)
            return (train_generator, validation_generator)

        mobilenet_model = self.__load_model()
        for layer in mobilenet_model.layers[:72]:
            layer.trainable = False
            if "bn" in layer.name: layer.trainable = True
        self.__compile_model(mobilenet_model)
        train_generator, validation_generator = image_generator()

        history = mobilenet_model.fit_generator(
            train_generator,
            samples_per_epoch=nb_train_samples,
            nb_epoch=nb_epoch,
            validation_data=validation_generator,
            nb_val_samples=nb_validation_samples)
        mobilenet_model.save_weights(os.path.join(self.result_dir, self.save_filename))

    def predict(self, test_data_dir):
        model = self.__load_model()
        model.load_weights(os.path.join(self.result_dir, self.save_filename))
        self.__compile_model(model)

        test_imagelist = os.listdir(test_data_dir)
        for test_image in test_imagelist:
            filename = os.path.join(test_data_dir, test_image)
            img = image.load_img(filename, target_size=(self.img_width, self.img_height))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = x / 255
            pred = model.predict(x)[0]
            print(test_image, [(self.classes[i], pred[i]) for i in reversed(pred.argsort())])

    def export_model(self):
        model = self.__load_model()
        model.load_weights(os.path.join(self.result_dir, self.save_filename))
        self.__compile_model(model)
        model.save(os.path.join(self.result_dir, ';'.join(self.classes) + ';export.h5'), include_optimizer=False)



if __name__ == '__main__':
    argc = len(sys.argv)
    if argc < 2 or sys.argv[1] not in ['train', 'predict', 'export']:
        print("%s train|predict|export" % sys.argv[0])
        exit(1)

    classes = ['photo', 'non-photo']
    img_width, img_height = 150, 150
    result_dir = 'results'
    phonto = Phonto(classes, (img_width, img_height), result_dir)

    if sys.argv[1] == 'train':
        train_data = ['dataset/train', 1000]
        validation_data = ['dataset/validation', 400]
        batch_size = 32
        nb_epoch = 10
        phonto.train(train_data, validation_data, batch_size, nb_epoch)
    elif sys.argv[1] == 'predict':
        test_data_dir = 'dataset/test'
        phonto.predict(test_data_dir)
    elif sys.argv[1] == 'export':
        phonto.export_model()
