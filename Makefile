serve: build

build: clean static-files

static-files:
	cd static; cp -r ./* ../public

test:
	@./test.sh

clean:
	rm -r public/*

.PHONY: serve build static-files test clean
