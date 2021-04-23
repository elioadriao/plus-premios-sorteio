install:
	@python3 -m pipenv install --dev

lock-requirements:
	@python3 -m pipenv lock -r > requirements.txt

run:
	@python3 -m pipenv run ./manage.py runserver

makemigrations:
	@python3 -m pipenv run ./manage.py makemigrations

migrate:
	@python3 -m pipenv run ./manage.py migrate

createsuperuser:
	@python3 -m pipenv run ./manage.py createsuperuser
