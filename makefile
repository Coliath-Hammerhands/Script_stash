env:
	uv sync
	uv tool install .
	uv run pre-commit install