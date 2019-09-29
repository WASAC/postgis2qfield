import os
import shutil
import datetime
from common.database import Database
from common.districts import Districts
from layers.admin import District, Sector, Cell, Village
from layers.basemap import River, Lake, Road, Forest, NationalPark
from layers.waterfacilities import WaterFacilities
from layers.chamber import Chamber
from layers.pipeline import Pipeline
from layers.pumping_station import PumpingStation
from layers.reservoir import Reservoir
from layers.water_connection import WaterConnection
from layers.watersource import WaterSource
from layers.wss import WaterSupplySystem


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
            self.folder = "{0}_{1}".format(self.folder, datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
            self.datafolder = "/".join([self.folder, 'data'])

        def load_layers(self, layers, output, filter):
            for lyr in layers:
                lyr.set_filter(filter)
                lyr.read(self.database)
                lyr.export2gpkg(output)

        def execute(self):
            os.makedirs( self.folder, exist_ok=True)

            basemap_file = "{0}/{1}".format(self.folder, "basemap.gpkg")
            existing_file = "{0}/{1}".format(self.folder, "existing_gis_database.gpkg")

            shutil.copy("./template/water_network_for_qfield.qgs", self.folder + "/water_network_for_qfield_{0}.qgs".format(self.district.district))
            shutil.copy("./template/template_gis_database.gpkg", self.folder + "/template_gis_database.gpkg")
            shutil.copytree("./template/images", self.folder + "/images")

            self.load_layers([District()], basemap_file, None)
            self.load_layers([Sector(), Cell(), Village(), River(), Lake(), Road(), Forest(),NationalPark()],
                             basemap_file, "dist_id=" + str(self.district.dist_id))
            self.load_layers([WaterFacilities()], existing_file, "dist_id=" + str(self.district.dist_id))
            self.load_layers([Chamber(), Pipeline(), PumpingStation(), Reservoir(),
                              WaterConnection(), WaterSource(), WaterSupplySystem()],
                             existing_file, "wss_id IN (" + self.district.wss_id_list + ")")

            shutil.make_archive("/".join(
                [self.main_dir, "{0}_{1}_{2}".format(
                    str(self.district.dist_id), self.district.district,
                    datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))]), 'zip',
                root_dir=self.folder)
            shutil.rmtree(self.folder)
