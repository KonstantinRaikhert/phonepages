run:
	python manage.py runserver
migrate:
	python manage.py makemigrations
	python manage.py migrate
static:
	python manage.py collectstatic
admin:
	python manage.py createadmin
deldb:
	python manage.py flush
