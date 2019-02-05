FROM tensorflow/tensorflow:latest-py3

RUN pip install -q keras
RUN pip install -q Pillow
RUN python -c 'from keras.applications.vgg16 import VGG16; VGG16()'

WORKDIR /work
