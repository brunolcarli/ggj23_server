install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver 0.0.0.0:11000

shell:
	python manage.py shell

enemy_daemon:
	python manage.py enemy_daemon

target: enemy_daemon run

pipe:
	make install
	make migrate
	make -j2 target
