.PHONY: build
build:
	pipenv install --dev

.PHONY: develop
develop:
	pipenv run watchmedo auto-restart \
		--patterns="*.py" \
		--recursive \
		waitress-serve -- --port 8000 --call 'sustainerds.api.app:get_app'

.PHONY: mypy
mypy:
	pipenv run mypy \
		--package sustainerds \
		--ignore-missing-imports \
		--show-traceback

.PHONY: validate_openapi_spec
validate_openapi_spec:
	pipenv run openapi_spec > sustainerds_openapi.yml
	pipenv run openapi-spec-validator sustainerds_openapi.yml

.PHONY: test
test: mypy
	pipenv run pytest \
		--disable-pytest-warnings

.PHONY: fmt
fmt: mypy test
	# remove unused imports
	pipenv run autoflake \
		--remove-all-unused-imports \
		--in-place \
		--recursive sustainerds/

	# organize imports
	pipenv run importanize sustainerds/
	
	# reformat code
	pipenv run black \
		--target-version py37 \
		sustainerds/