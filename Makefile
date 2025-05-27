dev:
	fastapi dev src/main.py

dev-uvicorn:
	uvicorn src.main:app --reload