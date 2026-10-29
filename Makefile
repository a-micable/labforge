.PHONY: install test oracles run cli docker

install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt && pip install -e .

test:
	. .venv/bin/activate && pytest -q

oracles:
	. .venv/bin/activate && python -m repairloop.eval --oracles-only

run:
	. .venv/bin/activate && streamlit run app.py

cli:
	. .venv/bin/activate && python -m repairloop.cli tasks

docker:
	docker build -t repairloop:local .
