export TZ=UTC

.PHONY: build
build:
	LDFLAGS='-L/usr/local/lib -L/usr/local/opt/openssl/lib -L/usr/local/opt/readline/lib' \
	pipenv install --dev

.PHONY: develop
develop: env.start
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
test: mypy env.start
	pipenv run pytest \
		--disable-pytest-warnings

.PHONY: fmt
fmt: test
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

.PHONY: env.start
env.start:
	docker-compose up -d

.PHONY: env.teardown
env.teardown:
	docker-compose stop