# 基にした情報・ソースコード
#   https://qiita.com/kazuki_hayakawa/items/c93a21313ccbd235b82b
#   http://aidiary.hatenablog.com/entry/20170108/1483876657
import os, sys
import numpy as np
from keras.applications.mobilenet import MobileNet
from keras.models import Sequential, Model
from keras.layers import Input, Activation, Dropout, Flatten, Dense
from keras.preprocessing import image
from keras import optimizers

classes = ['photo', 'non-photo']
nb_classes = len(classes)
img_width, img_height = 150, 150

result_dir = 'results'
test_data_dir = 'dataset/test'

def model_load():
    input_tensor = Input(shape=(img_width, img_height, 3))
    mobilenet = MobileNet(include_top=False, weights='imagenet', input_tensor=input_tensor)

    top_model = Sequential()
    top_model.add(Flatten(input_shape=mobilenet.output_shape[1:]))
    top_model.add(Dense(256, activation='relu'))
    top_model.add(Dropout(0.5))
    top_model.add(Dense(nb_classes, activation='softmax'))

    model = Model(input=mobilenet.input, output=top_model(mobilenet.output))
    model.load_weights(os.path.join(result_dir, 'finetuning.h5'))
    model.compile(loss='binary_crossentropy',
              optimizer=optimizers.SGD(lr=1e-3, momentum=0.9),
              metrics=['accuracy'])
    return model


if __name__ == '__main__':
    model = model_load()

    test_imagelist = os.listdir(test_data_dir)
    for test_image in test_imagelist:
        filename = os.path.join(test_data_dir, test_image)
        img = image.load_img(filename, target_size=(img_width, img_height))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = x / 255
        pred = model.predict(x)[0]

        top = 1
        top_indices = pred.argsort()[-top:][::-1]
        result = [(classes[i], pred[i]) for i in top_indices]
        print('file name is', test_image)
        print(result)
        print('=======================================')
