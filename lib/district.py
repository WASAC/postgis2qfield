class Districts(object):
    class District(object):
        def __init__(self, params):
            self.dist_id = params[0]
            self.district = params[1]
            self.wss_id_list = params[2]

    def __init__(self, dist_id_list):
        self.dist_id_list = dist_id_list
        self.district_list = []

    def get_wss_list_each_district(self, db):
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
        if len(self.dist_id_list) > 0:
            query += "WHERE a.dist_id IN (" + self.dist_id_list + ")"
        query += "GROUP BY a.dist_id, b.district "

        result = db.execute(query)
        self.district_list = []
        for data in result:
            self.district_list.append(Districts.District(data))
        return self.district_list
