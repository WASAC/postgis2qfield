# PostGIS2QField

## postgis2qfield.py

A simple tool for exporting from a PostGIS table to Zipped QField datasets. Assumes [Python 3.6+](http://www.python.org/download/), 
[psycopg2](http://initd.org/psycopg/download/) are already installed and in your ````PATH````.

The tool was designed for RWSS department of WASAC in Rwanda.

####Example usage:

To export table ````administrative boundary```` and ````water pipeline network````from database ````rwss_assets```` as user ````user```` to zipped QField datasets:

````
python postgis2qfield.py
````

Before running the script, kindly check the database settings at ````database```` class on ```` postgis2qfield.py```` .

````
class database:
    def __init__(self):
        self.host = 'localhost'
        self.port = 5432
        self.user = 'postgres'
        self.password = 'your password'
        self.database = 'rwss_gis'
````

This script was developed by ````Jin IGARASHI, JICA Expert```` from ````The Project for Strengthening Operation and Maintenance of Rural Water Supply Systems in Rwanda- RWASOM````.