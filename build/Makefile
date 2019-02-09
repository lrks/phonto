NAME := lrks/keras
TAG := debug

.PHONY: build run release clean
build:
	sudo docker build --force-rm=true -t $(NAME):$(TAG) ./

run:
	sudo docker run --rm -v $(dir $(abspath $(dir $$PWD))):/work -it $(NAME):$(TAG) /bin/bash

cmd := mkdir -p /tmp/phonto
cmd += && python /frugally-deep/keras_export/convert_model.py `find results/ -name "*;export.h5"` `find results/ -name "*;export.h5" | sed "s/h5/json/"`
cmd += ; g++ -std=c++14 -O3 phonto.cpp -o /tmp/phonto/phonto -static
cmd += && strip /tmp/phonto/phonto
cmd += && jq -c . `find results/ -name "*;export.json"` > /tmp/phonto/model.json
cmd += && tar -cvf /tmp/phonto.tar /tmp/phonto
cmd += && zopfli /tmp/phonto.tar
cmd += && ./phonto.sh `find results/ -name "*;export.json"` > phonto
cmd += && cat /tmp/phonto.tar.gz >> phonto
cmd += && chmod +x phonto
cmd += && cp /tmp/phonto.tar.gz /work
release:
	sudo docker run --rm -v $(dir $(abspath $(dir $$PWD))):/work -it $(NAME):$(TAG) /bin/bash -c '$(cmd)'

clean:
	rm -f ../phonto ../phonto.bin ../results/*export.*
