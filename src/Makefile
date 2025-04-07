# Makefile para Spotify to Vinyl (desde src)

VENV_DIR=../venv
PYTHON=$(VENV_DIR)/Scripts/python.exe
PIP=$(VENV_DIR)/Scripts/pip.exe

install:
	python -m venv $(VENV_DIR)
	$(PIP) install Flask Flask-MySQLdb requests PyMySQL

run:
	$(PYTHON) app.py

test:
	$(PYTHON) test_apis.py
	$(PYTHON) test_database.py
	$(PYTHON) test_funcional.py

init-db:
	mysql -u root -proot musicfinder < ../musicfinderdb.sql


clean:
	rm -rf $(VENV_DIR) __pycache__ .pytest_cache *.pyc */__pycache__ */*.pyc

