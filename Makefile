install-dev: venv
	$(VENV)/pip install -e .

build: venv
	$(VENV)/python setup.py sdist bdist_wheel

publish: venv
	$(VENV)/twine check dist/* && $(VENV)/twine upload dist/*

clean: clean-venv
	find . -type d -name __pycache__ -exec rm -r {} \+
	find . -type d -name build -exec rm -r {} \+
	find . -type d -name dist -exec rm -r {} \+
	find . -type d -name *.egg-info -exec rm -r {} \+

include Makefile.venv
