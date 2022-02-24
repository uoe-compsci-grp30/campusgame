
# Campusgame (Needs a better name)

Part of the submission for group 30.
The software side is split into multiple parts:

- The Django backend (this)
- The React frontend ([here](https://github.com/uoe-compsci-grp30/campusgame-react))

## Dependencies

For this project, a few important libraries should be installed.

1. GDAL (Geospatial Data Abstraction Library): This library is for the processing of geographical data.
This is important for processing user locations at a scale. Based in C, and wrapped by Python, this library makes the processing
fast, which is important when there are many users

    GDAL: https://gdal.org/

    GDAL github: https://github.com/OSGeo/gdal


2. Postgres & Postgis: These two libraries are for the storage of geographical data.

   Postgis is a fairly standard library, and is supported by Django.

   PostgreSQL: https://www.postgresql.org/
   
   PostgreSQL Django: https://docs.djangoproject.com/en/4.0/ref/databases/#postgresql-notes

   PostGIS Django: https://docs.djangoproject.com/en/4.0/ref/contrib/gis/install/postgis/
   