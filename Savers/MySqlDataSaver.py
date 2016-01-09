from DataSaver import IDataSaver
import mysql.connector

class MySqlDataSaver(IDataSaver):
    def __init__(self, host, database, user, password):
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
        except:
            print 'MySqlDataSaver.save_data. FAIL.'
            assert 0
        finally:
            connection.close()
        return saved

    def get_add_query(self, data):
        columns = data.get_columns()
        values = ["%s"] * len(columns)
        add_query = "INSERT INTO " \
                    + data.get_table_name() \
                    + " (" + ", ".join(columns) + ")" \
                    + " VALUES (" + ", ".join(values) + ")"

        return add_query