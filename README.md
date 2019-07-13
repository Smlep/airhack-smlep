AirHack 2019
============

For the AirHack Hackathon made possible by Airbnb, we had to create in 12 hours an application to handle task
repartition for a list of taskers.

For this project I used:

- Django
- MySql
- Bootstrap
- Heroku
- Service workers (The app works offline)


To download all required packages, use

```
$ pip install -r requirements.txt
```

You will need to define environment variables for the website to work, since I am using django-environ, you can put
these variables in a .env file:

- DEBUG
- DATABASE_NAME
- DATABASE_USER
- DATABASE_PASSWORD
- DATABASE_HOST
- DATABASE_PORT
- MODE
- SSL
