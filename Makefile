install:
	./setup.py install
	
check:
	python -m unittest discover -s tests/ -p "*_test.py"
docs:
	pdoc --html tsteno --output-dir docs