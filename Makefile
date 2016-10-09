all: lint unit

export PYTHONPATH:=${PWD}
version=`python -c 'import pock;print pock.version'`
filename=pock-`python -c 'import pock;print pock.version'`.tar.gz

lint:
	@flake8 .

test: clean lint
	@echo "Running tests ..."
	# @python -m unittest discover
	@py.test

clean:
	@printf "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do find . -name "$$pattern" -delete; done
	@echo "OK!"

release: clean docs deploy-documentation publish
	@printf "Exporting to $(filename)... "
	@tar czf $(filename) pock setup.py README.md LICENSE
	@echo "DONE!"

publish:
	@python setup.py sdist register upload
