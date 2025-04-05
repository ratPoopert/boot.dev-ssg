serve: build

build:
	python src/main.py

test:
	@./test.sh

clean:
	rm -r public/*

.PHONY: serve build test clean
