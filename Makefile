.PHONY: tests

# Clean
clean:
	@find . -name '__pycache__' | xargs rm -fr {} \;
	@find . -name '.coverage' | xargs rm -fr {} \;
	@find . -name 'build' | xargs rm -fr {} \;
	@find . -name 'dist' | xargs rm -fr {} \;
	@find . -name '.pytest_cache' | xargs rm -fr {} \;
	@find . -type d -name '*.egg-info' | xargs rm -fr {} \;
	@find . -type d -name '*.eggs' | xargs rm -fr {} \;

# Install
install:
	@pip install .
dev_install:
	@pip install -e .

# Tests
qa_check_code:
	@find ./src -name "*.py" | xargs flake8 --exclude *.eggs* --exclude ./src/confme/*
unittest:
	@pytest -v --cov=nsp --cov-report term-missing src/**/tests/unit
tests:
	@make qa_check_code
	# @make unittest
	@make clean
