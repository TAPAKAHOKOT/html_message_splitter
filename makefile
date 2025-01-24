format:
	poetry run black . && poetry run isort .

lint:
	poetry run flake8