import argparse
from common.tasks import Tasks
from common.taskmanager import TaskManager

def createArgumentParser():
    """
     Create the parameters for the script
    """

    parser = argparse.ArgumentParser(
        description="Create a QField datasets from PostGIS database.",
        epilog="Example usage: python postgis2qfield.py -d yourdatabase -H localhost - p 5432 -u user -w securePassword -l list_of_distID(seperated by comma)"
    )
    parser.add_argument("-d", "--database", dest="database",
                        type=str, required=True,
                        help="The database to connect to")

    # Python doesn't let you use -h as an option for some reason
    parser.add_argument("-H", "--host", dest="host",
                        default="localhost", type=str,
                        help="Database host. Defaults to 'localhost'")

    parser.add_argument("-p", "--port", dest="port",
                        default="5432", type=str,
                        help="Password for the database user")

    parser.add_argument("-u", "--user", dest="user",
                        default="postgres", type=str,
                        help="Database user. Defaults to 'postgres'")

    parser.add_argument("-w", "--password", dest="password",
                        type=str, required=True,
                        help="Password for the database user")

    parser.add_argument("-l", "--dist_id", dest="dist_id",
                        default="", type=str,
                        help="List of district ID which you want to export. For example, '51,52,53'")

    return parser.parse_args()


if __name__ == "__main__":
    args = createArgumentParser()
    t = Tasks(args)
    tasks = t.get_tasks()
    tm = TaskManager(tasks)
    tm.start()
