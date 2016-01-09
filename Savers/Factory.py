from MySqlDataSaver import MySqlDataSaver
from Configuration.DbConfiguration import DbConfiguration


class DataSaverFactory:
    @staticmethod
    def create(source_description):
        if source_description is None:
            return None

        config = DbConfiguration('config.ini')
        return MySqlDataSaver(config.host, config.database, config.user, config.password)

