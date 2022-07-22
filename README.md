
# Build or rebuild services,Create and start containers
> docker-compose up --build -d

# make migrations
> docker-compose run --rm web python backend/manage.py makemigrations

# migrate
> docker-compose run --rm web python backend/manage.py migrate

# bash
> docker-compose exec mysql mysql -u root -p
password:(enter password)
mysql> CREATE DATABASE content;
mysql> exit

# create superuser

> docker-compose run --rm web python backend/manage.py createsuperuser --username admin --email admin@localhost
password: (enter 任意)

# To get started:
> cd frontend
> npm run dev

# To build & start for production:
> cd frontend
> npm run build
> npm run start