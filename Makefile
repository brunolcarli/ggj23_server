install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver 0.0.0.0:11000

shell:
	python manage.py shell


pipe:
	make install
	make migrate
	make run
