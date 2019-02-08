NAME := lrks/keras
TAG := debug

.PHONY: build run release clean
build:
	sudo docker build --force-rm=true -t $(NAME):$(TAG) ./

run:
	sudo docker run --rm -v $(dir $(abspath $(dir $$PWD))):/work -it $(NAME):$(TAG) /bin/bash

cmd := python /frugally-deep/keras_export/convert_model.py `find results/ -name "*;export.h5"` `find results/ -name "*;export.h5" | sed "s/h5/json/"`
cmd += ; g++ -std=c++14 -O3 phonto.cpp -o phonto.bin
cmd += && strip phonto.bin
cmd += && jq -c . `find results/ -name "*;export.json"` | gzip -c > /tmp/model.gzip
cmd += && ./phonto.sh `find results/ -name "*;export.json"` phonto.bin /tmp/model.gzip > phonto
cmd += && chmod +x phonto
release:
	sudo docker run --rm -v $(dir $(abspath $(dir $$PWD))):/work -it $(NAME):$(TAG) /bin/bash -c '$(cmd)'

clean:
	rm -f ../phonto ../phonto.bin ../results/*export.*
