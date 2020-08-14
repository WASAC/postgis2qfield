from osgeo import ogr, osr
import os


class LayerBase(object):
    def __init__(self, name):
        self.table = name
        self.is_intersects = False
        self.parse_dates = None
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

    def getSQL(self):
        if self.is_intersects is True:
            sql = self.get_sql_intersects_by_district()
        else:
            sql = self.get_sql()
        return sql

    def export2gpkg_pandas(self, db, output):
        _gdf = db.get_gdf_from_postgis(self.getSQL(), self.parse_dates)
        # _gdf.crs = {'init': 'epsg:4326'}
        _gdf = _gdf[_gdf['geom'].notnull()]
        if not _gdf.empty:
            _gdf.to_file(output, layer=self.table, driver="GPKG")

    def export2gpkg_ogr(self, db, output):
        pg_ds = ogr.Open(db.getPostGISConnectionString(), update=1)
        sql_lyr = pg_ds.ExecuteSQL(self.getSQL())
        if sql_lyr is None:
            return
        # if GPKG file does not exist, it will create GPKG file.
        gpkg_dr = ogr.GetDriverByName('GPKG')
        if os.path.exists(output):
            gpkg_ds = gpkg_dr.Open(output, update=1)
        else:
            gpkg_ds = gpkg_dr.CreateDataSource(output)

        # if target layer exists, it will recreate the layer before adding features.
        gpkg_lyr = gpkg_ds.GetLayerByName(self.table)
        if gpkg_lyr is not None:
            gpkg_ds.DeleteLayer(self.table)
        gpkg_lyr = gpkg_ds.CreateLayer(self.table, geom_type=ogr.wkbNone)

        feature_defn = sql_lyr.GetLayerDefn()
        field_cnt = feature_defn.GetFieldCount()
        for f_idx in range(field_cnt):
            field_defn = feature_defn.GetFieldDefn(f_idx)
            if field_defn.GetName() == "geom":
                continue
            gpkg_lyr.CreateField(field_defn)
        geom_defn = feature_defn.GetGeomFieldDefn(feature_defn.GetGeomFieldIndex("geom"))
        gpkg_lyr.CreateGeomField(geom_defn)

        for i in range(sql_lyr.GetFeatureCount()):
            feature = sql_lyr.GetFeature(i)
            gpkg_lyr.CreateFeature(feature)

        pg_ds.ReleaseResultSet(sql_lyr)
