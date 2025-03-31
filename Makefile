serve: build

build:
	python src/main.py

test:
	@python -m unittest discover -s src

clean:
	rm -r public/*

.PHONY: serve build clean
