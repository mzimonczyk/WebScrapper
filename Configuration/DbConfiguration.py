import ConfigParser


class DbConfiguration:
    def __init__(self, config_file_name):
        config = ConfigParser.RawConfigParser()
        config.read(config_file_name)
        self.host = config.get('connection', 'host')
        self.database = config.get('connection', 'database')
        self.user = config.get('connection', 'user')
        self.password = config.get('connection', 'password')

    host = None
    database = None
    user = None
    password = None
