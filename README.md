# PostGIS2QField

## postgis2qfield.py

A simple tool for exporting from a PostGIS table to Zipped QField datasets. Assumes [Python 3.6+](http://www.python.org/download/), 
[psycopg2](http://initd.org/psycopg/download/),
[light-progress](https://pypi.org/project/light-progress/),
[geopandas](http://geopandas.org/), 
[GDAL](https://gdal.org/),
[Fiona](https://github.com/Toblerity/Fiona), 
[Shapely](https://github.com/Toblerity/Shapely), 
are already installed and in your ````PATH````.

You can install using pip by requirements.txt as follow.
````
pip install -r requirements.txt
````

The tool was designed for RWSS department of WASAC in Rwanda.

### Example usage:

To export table ````administrative boundary```` and ````water pipeline network````from database ````rwss_assets```` as user ````user```` to zipped QField datasets:

Before running the script, kindly check the database settings at command line parameters.
````
python postgis2qfield.py -d yourdatabase -H localhost -p 5432 -u user -w securePassword
````

If you want to filter only specific dictricts, use ````-l```` parameter to list ID of district by comma(,)

````
python postgis2qfield.py -l 51,52,53
````

## Run on Docker

```zsh
cp .env.example .env
vi .env # modify database connection settings.
docker-compose up
```

The data will be generated under `data` folder.

---
This script was developed by ````Jin IGARASHI, JICA Expert```` from ````The Project for Strengthening Operation and Maintenance of Rural Water Supply Systems in Rwanda- RWASOM````.