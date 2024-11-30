check:
	mypy --show-error-codes .
	
format:
	ruff check --fix
	isort .