from MySqlDataSaver import MySqlDataSaver


class DataSaverFactory:
    @staticmethod
    def create(source_description):
        if source_description is None:
            return None

        return MySqlDataSaver()

