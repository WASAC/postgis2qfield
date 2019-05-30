from lib.basemap import BaseMap


class BaseMapIntersects(BaseMap):
    def __init__(self, layers):
        super().__init__(layers)

    def get_data(self, _database, _table, _where):
        """
        save geojson file which intersects on target district feature from PostGIS

        Parameters
        ----------
         Object of database class
        _table : str
         table name
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

        return _database.execute(query)
