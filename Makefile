install:
	pip install -r requirements.txt

run:
	python manage.py runserver 0.0.0.0:11000


pipe:
	make install
	make run
