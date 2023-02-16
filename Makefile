
migrate:
	python manage.py makemigrations
	python manage.py migrate

runserver:
	python manage.py runserver

shell:
	python manage.py shell

createSU:
	python manage.py createsuperuser


#clean_db:
#	@find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
#	@find . -path "*/migrations/*.pyc"  -delete
#	@rm -f db.sqlite3
#	@python manage.py makemigrations --empty myapp
#	@python manage.py migrate myapp
