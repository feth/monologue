COVER_HTML_DIR = ./cover/
PKG_NAME = monologue

OPT_DOCTEST=--with-doctest --with-coverage --doctest-tests

help:
	@echo "'make test' to run all tests contained in this package."

test:
	PYTHONPATH=.:$(PYTHONPATH) nosetests -x -s $(OPT_DOCTEST)\
		--cover-html --cover-html-dir=$(COVER_HTML_DIR) \
		--cover-package=$(PKG_NAME) --cover-package=$(PKG_NAME).tests \
		$(PKG_NAME) $(PKG_NAME).tests

clean:
	-rm -rf $(COVER_HTML_DIR) .coverage
	-find $(PKG_NAME) -name "*.pyc" -delete
