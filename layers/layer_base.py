class LayerBase(object):
    def __init__(self, name):
        self.table = name
        self.is_intersects = False
        self.parse_dates = None
        self.gdf = None
        self.filter = None

    def set_filter(self, filter):
        self.filter = filter

    def get_sql(self):
        query = "SELECT * FROM " + self.table
        if self.filter is not None:
            query += " WHERE " + self.filter
        return query

    def get_sql_intersects_by_district(self):
        query = "SELECT a.* FROM " + self.table + " a "
        query += "        INNER JOIN district b "
        query += "        ON ST_INTERSECTS(b.geom,a.geom) = true "
        if self.filter is not None:
            query += " WHERE " + self.filter
        return query

    def read(self, db):
        if self.is_intersects is True:
            sql = self.get_sql_intersects_by_district()
        else:
            sql = self.get_sql()
        self.gdf = db.get_gdf_from_postgis(sql, self.parse_dates)
        self.gdf.crs = {'init': 'epsg:4326'}

    def export2gpkg(self, output):
        _gdf = self.gdf[self.gdf['geom'].notnull()]
        if not _gdf.empty:
            _gdf.to_file(output, layer=self.table, driver="GPKG")