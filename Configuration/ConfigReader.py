from Configuration.SourceDescription import SourceDescription

def ceate_mock_config_reader():
    return MockConfigReader()

class IConfigReader:
    def __init__(self):
        pass

    def read_data(self):
        pass

    def get_data(self):
        pass


class MockConfigReader(IConfigReader):
    def __init__(self):
        IConfigReader.__init__(self)

    def get_data(self):
        sample = SourceDescription()
        sample.type = 'POST'
        sample.url = 'https://www.doyouspain.com/formulario.asp?idioma=EN'
        sample.headers = {
            'Referer': 'https://www.doyouspain.com/'
            , 'Content-Type': 'application/x-www-form-urlencoded'
        }
        sample.data = {'pais': 'PT'
            , 'destino': 'FNC01'
            , 'chkOneWay': 'SI'
            , 'destino_final': 0
            , 'fechaRecogida': 'Tue, 26/01/2016'
            , 'horarecogida': '9'
            , 'minutosrecogida': '00'
            , 'fechaDevolucion': 'Tue, 02/02/2016'
            , 'horadevolucion': '9'
            , 'minutosdevolucion': '00'
            , 'chkAge': 'SI'
            , 'edad': 35
            , 'send': 'Search'
            , 'booster': 0
            , 'child_seat': 0
            }

        sample1 = SourceDescription()
        sample1.type = 'GET'
        sample1.url = 'http://biletylotnicze.itaka.pl/charter/results-json?departure_date=03.01.2016&adults=2&children=0&sort_type=1&page=1'
        list = {sample1}
        return list
