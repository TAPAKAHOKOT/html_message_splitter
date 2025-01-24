format:
	poetry run black . && poetry run isort .

lint:
	poetry run flake8

test:
	poetry run python -m unittest discover -s tests
