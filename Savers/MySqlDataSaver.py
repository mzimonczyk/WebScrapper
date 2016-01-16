from DataSaver import IDataSaver
import mysql.connector
import logging


class MySqlDataSaver(IDataSaver):
    def __init__(self, host, database, user, password):
        IDataSaver.__init__(self)
        self._host = host
        self._database = database
        self._user = user
        self._password = password

    _host = None
    _database = None
    _user = None
    _password = None

    def save_data(self, data):
        saved = False
        try:
            connection = mysql.connector.connect(host=self._host
                                                 , database=self._database
                                                 , user=self._user
                                                 , password=self._password)
            try:
                cursor = connection.cursor()
                cursor.executemany(self.get_add_query(data), data.get_rows())
                connection.commit()
                cursor.close()
                saved = True
            except mysql.connector.Error as err:
                logging.error(err.msg)
            finally:
                connection.close()
        except mysql.connector.Error as err:
            logging.error(err.msg)

        return saved

    def get_add_query(self, data):
        columns = data.get_columns()
        values = ["%s"] * len(columns)
        add_query = "INSERT INTO " \
                    + data.get_table_name() \
                    + " (" + ", ".join(columns) + ")" \
                    + " VALUES (" + ", ".join(values) + ")"

        return add_query
