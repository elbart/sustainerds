.PHONY: build
build:
	pipenv install --dev

.PHONY: develop
develop:
	pipenv run watchmedo auto-restart \
	--patterns="*.py" \
	--recursive \
	waitress-serve -- --port 8000 sustainerds.api.app:app

.PHONY: mypy
mypy:
	pipenv run mypy \
	--package sustainerds \
	--ignore-missing-imports

.PHONY: test
test: mypy
	pipenv run pytest