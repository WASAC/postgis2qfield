import psycopg2
import geopandas as gpd
from osgeo import ogr


class Database(object):
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
        self.conn = None
        self.create_connection()

    def create_connection(self):
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

    def get_gdf_from_postgis(self, sql, parse_dates):
        gdf = gpd.read_postgis(sql, self.conn, coerce_float=True,  parse_dates=parse_dates)
        return gdf

    def getPostGISConnectionString(self):
        return 'PG:dbname={0} host={1} port={2} user={3} password={4}'.format(
            self.database, self.host,self.port, self.user,self.password)

    def get_layer_from_postgis(self, sql):
        pg_connection_string = 'dbname={0} host={1} port={2} user={3} password={4}'.format(self.database, self.host, self.port, self.user, self.password)
        pg_ds = ogr.Open('PG:' + pg_connection_string, update=1)
        sql_lyr = pg_ds.ExecuteSQL(sql)
        return sql_lyr
