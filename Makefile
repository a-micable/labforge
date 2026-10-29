.PHONY: run cli install

install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

run:
	. .venv/bin/activate && streamlit run app.py

cli:
	. .venv/bin/activate && python cli.py --task rc_step_response
