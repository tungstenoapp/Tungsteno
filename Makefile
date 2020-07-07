install:
	./setup.py install

check:
	python -m unittest discover -s tests/ -p "*_test.py"
docs:
	pdoc3 --html tsteno --output-dir docs -f