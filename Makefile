serve: main
	cd public; python -m http.server 8888

build: clean static-files
	python -m ssg.main "/boot.dev-ssg/"

main: clean static-files
	python -m ssg.main

static-files:
	cd static; cp -r ./* ../docs

test:
	@./test.sh

clean:
	- rm -r docs/*

.PHONY: serve build static-files test clean
