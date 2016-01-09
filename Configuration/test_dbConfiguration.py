from unittest import TestCase
from Configuration.DbConfiguration import DbConfiguration


class TestDbConfiguration(TestCase):
    def test_DbConfiguration_object_returns_correct_configuraton(self):
        config = DbConfiguration('config.example.ini')

        self.assertEqual('your_host', config.host)
        self.assertEqual('your_db', config.database)
        self.assertEqual('your_user', config.user)
        self.assertEqual('your_password', config.password)
