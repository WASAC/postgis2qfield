import json
import os
import geopandas as gpd


class BaseMap(object):
    def __init__(self, layers):
        self.layers = layers

    def save_file(self, rows, file):
        """
        save the file from result of SQL

        Parameters
        ----------
        rows : object
            result of SQL execute
        file : string
            output file path
        """
        if len(rows) > 0 and len(rows[0]) > 0:
            # Write it to a file
            jsonfile = open(file + '.geojson', 'w')
            json.dump(rows[0][0], jsonfile)

    def get_data(self, _database, _table, _where):
        """
         save geojson file from PostGIS

         Parameters
         ----------
         _table : str
             table name
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
        if _where is not None:
            query += " WHERE " + _where

        query += ") row) features;"
        return _database.execute(query)

    def save(self, _database, _datafolder, _where):
        for layer in self.layers:
            file_path = "/".join([_datafolder, layer])
            rows = self.get_data(_database, layer, _where)
            self.save_file(rows, file_path)

            file_geojson = file_path + ".geojson"
            try:
                gdf = gpd.read_file(file_geojson)
                gdf.to_file("{0}/existing_gis_database.gpkg".format(_datafolder), layer=layer, driver="GPKG")
            except Exception as exc:
                #print("{0}: Unable to export to Geopackage. Error was {1}".format(layer, str(exc)))
                pass
            os.remove(file_geojson)
