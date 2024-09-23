# Copyright 2024 The Spin Authors. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

precommit:
	make fmt
	make lint
	make types
	make test
build:
	python3 -m build
deploy:
	python3 -m twine upload dist/*
install:
	pip install -e .
fmt:
	python -m ruff format .
lint:
	python -m ruff check .
types:
	mypy spinsys
test:
	pytest
freeze:
	pip freeze > requirements.txt

.PHONY: setupenv
setupenv:
	python3 -m venv spinpy_env
	. spinpy_env/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt && \
	make install
