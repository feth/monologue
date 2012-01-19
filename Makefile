COVER_HTML_DIR = ./cover/
PKG_NAME = monologue

OPT_DOCTEST=--with-doctest --with-coverage --doctest-tests

help:
	@echo "usage: make help|clean|test"

clean:
	rm -rf $(COVER_HTML_DIR) .coverage
	find $(PKG_NAME) -name "*.pyc" -delete

test:
	PYTHONPATH=.:$(PYTHONPATH) nosetests -x -s $(OPT_DOCTEST)\
		--cover-html --cover-html-dir=$(COVER_HTML_DIR) \
		--cover-package=$(PKG_NAME) --cover-package=$(PKG_NAME).tests \
		$(PKG_NAME) $(PKG_NAME).tests

pdf: README.pdf

README.pdf: README.rst
	rst2pdf README.rst

.PHONY: clean help test pdf
.IGNORE: clean help
