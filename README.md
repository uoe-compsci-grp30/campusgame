# Campusgame (Needs a better name)

Part of the submission for group 30. The software side is split into multiple parts:

- The Django backend (this)
- The React frontend ([here](https://github.com/uoe-compsci-grp30/campusgame-react))

## Dependencies

For this project, a few important libraries should be installed.

1. GDAL (Geospatial Data Abstraction Library): This library is for the processing of geographical data. This is
   important for processing user locations at a scale. Based in C, and wrapped by Python, this library makes the
   processing fast, which is important when there are many users

   GDAL: https://gdal.org/

   GDAL github: https://github.com/OSGeo/gdal

   GDAL brew: https://formulae.brew.sh/formula/gdal

2. GEOS (Geometry Engine – Open Source): This provides the geometry implementation for GeoDjango. This can be installed from source, but if you have homebrew installed, it is much easier

   GEOS docs: https://libgeos.org/usage/install/

3. PROJ: This library provides a way to map coordinates between projections, which is unlikely to be used in our app, but is still a dependency of Postgis

   PROJ docs: https://proj.org/

5. Postgres & Postgis: These two libraries are for the storage of geographical data.
   Postgis is a fairly standard library, and is supported by Django.

   PostgreSQL: https://www.postgresql.org/
   
   PostGIS: https://postgis.net/install/

   PostgreSQL Django: https://docs.djangoproject.com/en/4.0/ref/databases/#postgresql-notes

   PostGIS Django: https://docs.djangoproject.com/en/4.0/ref/contrib/gis/install/postgis/
   

## Setting up the database

__NOTE: Make sure GDAL, GEOS, PROJ, and PostGis are installed (Link to how [here](https://docs.djangoproject.com/en/4.0/ref/contrib/gis/install/geolibs/#geosbuild))__

Make sure you have PostgreSQL installed to your machine, and have it running.
For the time being, make sure it creates a user in the database that is admin, and is accessible from your 
user on your computer.

From your terminal/command line, create a database using:

`$ createdb campusgame`

This will create a database in Postgres (short for PostgreSQL).
To access this database into an SQL prompt simply type:

`$psql campusgame`

Which will open up an SQL shell. 
In this shell we can do all sorts, but for now we want to create an extension in the database, for PostGIS.
Type the command:

`CREATE EXTENSION postgis;`

And hopefully it will work.
This means that your Postgres database has all the tools it needs to perform geographical queries.

## Connecting to the database

Our Django config uses a database url system in order to connect to the database.
This is simply so that we can: 
 - Separate the database configuration from the settings file
 - Hide secrets, such as database credentials behind a .env file
 - Allow collaborators to connect to their own database without changing the code

If you don't already have one, create a `.env` file using:

`vim .env`

While editing, set the variable:

`DATABASE_URL=postgres://<USERNAME>:<PASSWORD>@<DATABASE_URL>/<DATABASE_NAME>`

Substituting the following:
 - USERNAME & PASSWORD: The username, and password for your database
 - DATABASE_URL: The url to your database, optionally with the port, this is usually `localhost`
 - DATABASE_NAME: The name of the database, if you followed these instructions, this will be `campusgame`


## Celery, and the likes

Celery is a Python library that allows for the running of scheduled tasks.
This can be used to send out scheduled emails, and run background tasks.
In our case it will be used for the moving of zones behind the scenes.
Read more [here](https://docs.celeryproject.org/en/stable/getting-started/introduction.html).

For our system we will use `Redis` as a broker, as this is the most widely used.
Redis is a memory based key-value pair database, and in this case it stores the items in queue to be run by Celery.

For setup with Django see [here](https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html).