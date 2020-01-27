# Bazinga

## Installation
- Install `docker` and `docker-compose` if you don't have it.

 docker - https://docs.docker.com/install/
 
 docker-compose - https://docs.docker.com/compose/install/
- Run command `docker-compose up` in shell and wait for project deployment.

## Project details

After deploy you'll have installed containers:
 - web part based on `django`,
 - `postgresql` database,
 - `celery` and `celery-beat` for managing tasks and schedules,
 - `redis` as broker for `celery`,
 - `flower` - monitoring tool for tasks (will be available here http://127.0.0.1:8888)
 
Now you can open http://127.0.0.1:8000 to see login page.
http://127.0.0.1:8000/admin - here is admin panel.

Default superuser account already created:
- login `Superbazinga`
- password `bazinga1234`

Also migration will create 10 sample bazes, 10 customers, each customer will have 100 targets with random weekday and time.
Customer will have possibility to change interval after login on main page.

Scheduler already added as PeriodicTask in http://127.0.0.1:8000/admin/django_celery_beat/periodictask/

You can change executing time there.
After executing task `prepare-tomorrow-tasks` new tasks for sending emails to targets will be created.

Bazinga!!!
