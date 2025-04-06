serve: build
	cd public; python -m http.server 8888

build: clean static-files
	python -m ssg.main

static-files:
	cd static; cp -r ./* ../public

test:
	@./test.sh

clean:
	- rm -r public/*

.PHONY: serve build static-files test clean
