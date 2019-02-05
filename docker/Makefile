NAME := lrks/keras
TAG := debug

.PHONY: build run
build:
	sudo docker build --force-rm=true -t $(NAME):$(TAG) ./
run:
	#sudo docker run --rm -u $(shell id -u):$(shell id -g) -p 8888:8888 -v $(dir $(abspath $(dir $$PWD))):/work -it $(NAME):$(TAG) /bin/bash
	sudo docker run --rm -v $(dir $(abspath $(dir $$PWD))):/work -it $(NAME):$(TAG) /bin/bash
