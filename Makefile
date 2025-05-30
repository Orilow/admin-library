dev:
	fastapi dev src/main.py

dev-uvicorn:
	uvicorn src.main:app --reload

lint-all:
	flake8 scr/

fix-all:
	black src/

test-all:
	pytest -v