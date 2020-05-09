.PHONY:
all: requirements test

.PHONY:
requirements:
	pip -q install . --no-cache-dir

.PHONY:
test:
	pip -q install -U -r requirements-test.txt --no-cache-dir
	nosetests -s -v .
