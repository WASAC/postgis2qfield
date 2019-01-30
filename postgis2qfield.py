import os
import shutil
import datetime
import json
import psycopg2

class database:
    def __init__(self):
        self.host = 'localhost'
        self.port = 5432
        self.user = 'postgres'
        self.password = 'your password'
        self.database = 'rwss_gis'

    def createConnection(self):
        try:
            self.conn = psycopg2.connect(host=self.host, port=self.port, database=self.database, user=self.user, password=self.password)

        except:
            print("Unable to connect to the database. Please check your options and try again.")
            exit()

    def execute(self,query):
        with self.conn.cursor() as cur:
            # Execute the query
            try:
                cur.execute(query)
            except Exception as exc:
                print("Unable to execute query. Error was {0}".format(str(exc)))
                exit()
            rows = cur.fetchall()
            return rows

def getWssListEachDistrict():
    query = "SELECT "
    query += "  a.dist_id, "
    query += "  b.district, "
    query += "  ARRAY_TO_STRING(ARRAY_AGG(a.wss_id),',') as wss_id_list "
    query += "FROM wss a "
    query += "INNER JOIN district b "
    query += "ON a.dist_id = b.dist_id "
    query += "GROUP BY a.dist_id, b.district "

    db = database()
    db.createConnection()
    return db.execute(query)

def saveGeoJsonData(_table, _file, _where):
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

    db = database()
    db.createConnection()
    rows = db.execute(query)
    if len(rows) > 0 and len(rows[0]) > 0:
        # Write it to a file
        jsonfile = open(_file + '.geojson', 'w')
        json.dump(rows[0][0], jsonfile)

def create_qfield_data():
    base_layers = ["district", "sector", "cell", "village"]
    wss_layers = ["chamber", "pipeline", "pumping_station", "reservoir", "water_connection", "watersource", "wss"]

    maindir = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + "_RWSS_Assets_data"
    districts = getWssListEachDistrict()
    for dist in districts:
        dist_id, district, wss_id_list = dist

        _folder = "/".join([maindir, str(dist_id) + "_" + district])
        _datafolder = "/".join([_folder, 'data'])
        os.makedirs(_datafolder, exist_ok=True)

        #copy template qfield file to district folder
        shutil.copy("./template/water_network_for_qfield.qgs", _folder + "/water_network_for_qfield.qgs")
        shutil.copytree("./template/images", _folder + "/images")

        for layer in base_layers:
            filepath = "/".join([_datafolder, layer])
            saveGeoJsonData(layer, filepath, "dist_id=" + str(dist_id))

        for layer in wss_layers:
            filepath = "/".join([_datafolder, layer])
            saveGeoJsonData(layer, filepath, "wss_id IN (" + wss_id_list + ")")

        shutil.make_archive("/".join([maindir,str(dist_id) + "_" + district]), 'zip', root_dir=_folder)
        shutil.rmtree(_folder)
    print("It created QField dataset at folder(" + os.path.abspath(maindir) + ")")


if __name__ == "__main__":
    create_qfield_data()