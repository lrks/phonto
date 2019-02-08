FROM tensorflow/tensorflow:latest-py3

RUN pip install -q keras
RUN pip install -q Pillow
RUN python -c 'from keras.applications.mobilenet import MobileNet; MobileNet()'

RUN apt update
RUN apt install -y wget unzip cmake sudo jq imagemagick
RUN wget -q https://github.com/Dobiasd/FunctionalPlus/archive/master.zip
RUN unzip master.zip
RUN cd FunctionalPlus-* && mkdir -p build && cd build && cmake .. && make && sudo make install && cd /
RUN rm -f master.zip

RUN apt install -y mercurial
RUN hg clone https://bitbucket.org/eigen/eigen/
RUN cd eigen && mkdir -p build && cd build && cmake .. && make && sudo make install && sudo ln -s /usr/local/include/eigen3/Eigen /usr/local/include/Eigen && cd /

RUN wget https://github.com/nlohmann/json/archive/v3.1.2.zip
RUN unzip v3.1.2.zip
RUN cd json-* && mkdir -p build && cd build && cmake .. && make && sudo make install && cd /
RUN rm -rf v3.1.2.zip

RUN wget -q https://github.com/Dobiasd/frugally-deep/archive/master.zip
RUN unzip master.zip
RUN mv frugally-deep-master frugally-deep
RUN cd frugally-deep && mkdir -p build && cd build && cmake .. && make && sudo make install && cd /
RUN rm -f master.zip

WORKDIR /work
