import os
import shutil
import datetime
from lib.database import Database
from lib.district import Districts
from lib.basemap import BaseMap
from lib.basemap_intersects import BaseMapIntersects


class Tasks(object):
    def __init__(self, args):
        self.db = Database(args)
        self.maindir = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + "_RWSS_Assets_data"
        self.districts = Districts(args.dist_id)
        self.district_list = self.districts.get_wss_list_each_district(self.db)

    def get_tasks(self):
        obj_list = []
        for dist in self.district_list:
            obj_list.append(Tasks.Task(self.maindir, dist, self.db))
        return obj_list

    class Task(object):
        def __init__(self, main_dir, district, db):
            self.district = district
            self.database = db
            self.main_dir = main_dir
            self.folder = "/".join([main_dir, str(district.dist_id) + "_" + district.district])
            self.datafolder = "/".join([self.folder, 'data'])

        def execute(self):
            os.makedirs(self.datafolder, exist_ok=True)

            shutil.copy("./template/water_network_for_qfield.qgs", self.folder + "/water_network_for_qfield.qgs")
            shutil.copy("./template/template_gis_database.gpkg", self.folder + "/template_gis_database.gpkg")
            shutil.copytree("./template/images", self.folder + "/images")

            object_list = [
                {"mapObj" : BaseMap(["district", "sector", "cell", "village","waterfacilities"]), "filter" : "dist_id=" + str(self.district.dist_id)},
                {"mapObj": BaseMap(["chamber", "pipeline", "pumping_station", "reservoir", "water_connection", "watersource", "wss"]),
                 "filter": "wss_id IN (" + self.district.wss_id_list + ")"},
                {"mapObj": BaseMapIntersects(["rivers_all_rw92", "lakes_all", "roads_all", "forest_cadastre", "national_parks"]),
                 "filter": "b.dist_id=" + str(self.district.dist_id)}]
            for obj in object_list:
                obj['mapObj'].save(self.database, self.datafolder, obj['filter'])

            shutil.make_archive("/".join(
                [self.main_dir, str(self.district.dist_id) + "_" + self.district.district]),
                'zip',
                root_dir=self.folder)
            shutil.rmtree(self.folder)
            #print("It exported {0}_{1}.zip".format(str(self.district.dist_id), self.district.district))
