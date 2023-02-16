
migrate:
	python manage.py makemigrations
	python manage.py migrate

runserver:
	python manage.py runserver

shell:
	python manage.py shell

createSU:
	python manage.py createsuperuser
