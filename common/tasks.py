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
from layers.valve import Valve
from layers.wtp import Wtp


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

        def load_layers_ogr(self, layers, output, filter):
            for lyr in layers:
                lyr.set_filter(filter)
                lyr.export2gpkg_ogr(self.database, output)

        def load_layers_pandas(self, layers, output, filter):
            for lyr in layers:
                lyr.set_filter(filter)
                lyr.export2gpkg_pandas(self.database, output)

        def execute(self):
            basemap_file = "{0}/{1}".format(self.folder, "basemap.gpkg")
            existing_file = "{0}/{1}".format(self.folder, "existing_gis_database.gpkg")

            os.makedirs(self.folder, exist_ok=True)
            shutil.copy("./template/water_network_for_qfield.qgs",
                        "{0}/water_network_for_qfield_{1}.qgs".format(self.folder, self.district.district))
            shutil.copy("./template/water_network_for_qfield.qgs.cfg",
                        "{0}/water_network_for_qfield_{1}.qgs.cfg".format(self.folder, self.district.district))
            shutil.copy("./template/template_gis_database.gpkg", "{0}/template_gis_database.gpkg".format(self.folder))
            shutil.copytree("./template/images", "{0}/images".format(self.folder))

            self.load_layers_pandas([District()], basemap_file, None)
            self.load_layers_pandas([Sector(), Cell(), Village(), River(), Lake(), Road(), Forest(), NationalPark()],
                             basemap_file, "dist_id=" + str(self.district.dist_id))
            self.load_layers_pandas([WaterFacilities()], existing_file, "dist_id=" + str(self.district.dist_id))
            self.load_layers_pandas([Chamber(), Pipeline(), PumpingStation(), Reservoir(),
                              WaterConnection(), WaterSource(), WaterSupplySystem(), Valve(), Wtp()],
                             existing_file, "wss_id IN (" + self.district.wss_id_list + ")")

            shutil.make_archive(self.folder, 'zip', root_dir=self.folder)
            shutil.rmtree(self.folder)
