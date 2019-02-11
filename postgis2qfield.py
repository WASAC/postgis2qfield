import os
import shutil
import datetime
import json
import psycopg2
import argparse

def createArgumentParser():
    """
     Create the parameters for the script
    """

    parser = argparse.ArgumentParser(
        description="Create a QField datasets from PostGIS database.",
        epilog="Example usage: python postgis2qfield.py -d yourdatabase -H localhost - p 5432 -u user -w securePassword -l list_of_distID(seperated by comma)"
    )
    parser.add_argument("-d", "--database", dest="database",
                        type=str, required=True,
                        help="The database to connect to")

    # Python doesn't let you use -h as an option for some reason
    parser.add_argument("-H", "--host", dest="host",
                        default="localhost", type=str,
                        help="Database host. Defaults to 'localhost'")

    parser.add_argument("-p", "--port", dest="port",
                        default="5432", type=str,
                        help="Password for the database user")

    parser.add_argument("-u", "--user", dest="user",
                        default="postgres", type=str,
                        help="Database user. Defaults to 'postgres'")

    parser.add_argument("-w", "--password", dest="password",
                        type=str, required=True,
                        help="Password for the database user")

    parser.add_argument("-l", "--dist_id", dest="dist_id",
                        default="", type=str,
                        help="List of district ID which you want to export. For example, '51,52,53'")

    return parser.parse_args()

class database:
    def __init__(self, params):
        """
        Constructor

        Parameters
        ----------
        params : object
            List of arguments from command line
        """
        self.host = params.host
        self.port = params.port
        self.user = params.user
        self.password = params.password
        self.database = params.database

    def createConnection(self):
        """
        Create the database connection
        """
        try:
            self.conn = psycopg2.connect(host=self.host, port=self.port, database=self.database, user=self.user, password=self.password)

        except:
            print("Unable to connect to the database. Please check your options and try again.")
            exit()

    def execute(self, query):
        """
        Execute SQL on PostGIS

        Parameters
        ----------
        query : str
            SQL for running
        """
        with self.conn.cursor() as cur:
            # Execute the query
            try:
                cur.execute(query)
            except Exception as exc:
                print("Unable to execute query. Error was {0}".format(str(exc)))
                exit()
            rows = cur.fetchall()
            return rows

def save_file(rows, _file):
    """
    save the file from result of SQL

    Parameters
    ----------
    rows : object
        result of SQL execute
    """
    if len(rows) > 0 and len(rows[0]) > 0:
        # Write it to a file
        jsonfile = open(_file + '.geojson', 'w')
        json.dump(rows[0][0], jsonfile)

def getWssListEachDistrict(db):
    """
    Get the list of WSS each district from PostGIS

    Parameters
    ----------
    db : database class
        Object of database class
    """

    query = "SELECT "
    query += "  a.dist_id, "
    query += "  b.district, "
    query += "  ARRAY_TO_STRING(ARRAY_AGG(a.wss_id),',') as wss_id_list "
    query += "FROM wss a "
    query += "INNER JOIN district b "
    query += "ON a.dist_id = b.dist_id "
    if len(params.dist_id) > 0:
        query += "WHERE a.dist_id IN (" + params.dist_id + ")"
    query += "GROUP BY a.dist_id, b.district "

    return db.execute(query)

def saveGeoJsonData(db,_table, _file, _where):
    """
     save geojson file from PostGIS

     Parameters
     ----------
     db : database class
         Object of database class
     _table : str
         table name
     _file : str
         file name
     _where : str
         where statement of SQL
     """
    query = "SELECT jsonb_build_object("
    query += "    'type',     'FeatureCollection',"
    query += "    'features', jsonb_agg(feature)"
    query += ")"
    query += "FROM ("
    query += "  SELECT jsonb_build_object("
    query += "    'type',       'Feature',"
    query += "    'geometry',   ST_AsGeoJSON(geom)::jsonb,"
    query += "    'properties', to_jsonb(row) - 'gid' - 'geom'"
    query += "  ) AS feature"
    query += "  FROM (SELECT * FROM " + _table

    # If a WHERE statement was provided, add that
    if _where is not None:
        query += " WHERE " + _where

    query += ") row) features;"

    rows = db.execute(query)
    save_file(rows, _file)

def saveGeoJsonDataIntersectsDistrict(db,_table, _file, _where):
    """
    save geojson file which intersects on target district feature from PostGIS

    Parameters
    ----------
    db : database class
     Object of database class
    _table : str
     table name
    _file : str
     file name
    _where : str
     where statement of SQL
    """
    query = "SELECT jsonb_build_object("
    query += "    'type',     'FeatureCollection',"
    query += "    'features', jsonb_agg(feature)"
    query += ")"
    query += "FROM ("
    query += "  SELECT jsonb_build_object("
    query += "    'type',       'Feature',"
    query += "    'geometry',   ST_AsGeoJSON(geom)::jsonb,"
    query += "    'properties', to_jsonb(row) - 'gid' - 'geom'"
    query += "  ) AS feature"
    query += "  FROM (SELECT a.* FROM " + _table + " a "
    query += "        INNER JOIN district b "
    query += "        ON ST_INTERSECTS(b.geom,a.geom) = true "
    # If a WHERE statement was provided, add that
    if _where is not None:
        query += " WHERE " + _where
    query += ") row) features;"

    rows = db.execute(query)
    save_file(rows, _file)

def create_qfield_data(params):
    """
    MAIN FUNCTION: create geojson files each district from PostGIS

    Parameters
    ----------
    params : object
        List of arguments from command line
    """
    base_layers = ["district", "sector", "cell", "village"]
    baseobj_layers = ["rivers_all_rw92", "lakes_all","roads_all","forest_cadastre","national_parks"]
    wss_layers = ["chamber", "pipeline", "pumping_station", "reservoir", "water_connection", "watersource", "wss"]

    db = database(params)
    db.createConnection()

    maindir = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + "_RWSS_Assets_data"
    districts = getWssListEachDistrict(db)
    for dist in districts:
        dist_id, district, wss_id_list = dist

        _folder = "/".join([maindir, str(dist_id) + "_" + district])
        _datafolder = "/".join([_folder, 'data'])
        os.makedirs(_datafolder, exist_ok=True)

        #copy template qfield file to district folder
        shutil.copy("./template/water_network_for_qfield.qgs", _folder + "/water_network_for_qfield.qgs")
        shutil.copy("./template/template_gis_database.gpkg", _folder + "/template_gis_database.gpkg")
        shutil.copytree("./template/images", _folder + "/images")

        for layer in base_layers:
            filepath = "/".join([_datafolder, layer])
            saveGeoJsonData(db,layer, filepath, "dist_id=" + str(dist_id))

        for layer in wss_layers:
            filepath = "/".join([_datafolder, layer])
            saveGeoJsonData(db,layer, filepath, "wss_id IN (" + wss_id_list + ")")

        for layer in baseobj_layers:
            filepath = "/".join([_datafolder, layer])
            saveGeoJsonDataIntersectsDistrict(db,layer, filepath, "b.dist_id=" + str(dist_id))

        shutil.make_archive("/".join([maindir,str(dist_id) + "_" + district]), 'zip', root_dir=_folder)
        shutil.rmtree(_folder)
    print("It created QField dataset at folder(" + os.path.abspath(maindir) + ")")

if __name__ == "__main__":
    params = createArgumentParser()
    create_qfield_data(params)