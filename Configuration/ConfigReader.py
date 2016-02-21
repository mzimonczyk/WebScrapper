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
        sample1.url = 'http://biletylotnicze.itaka.pl/charter/results-json?departure_date=03.01.2016&dep_name_sel=123%2CKTW&adults=2&children=0&sort_type=1&page=1'

        sample2 = SourceDescription()
        sample2.type = 'GET'
        sample2.url = 'http://oferty.tui.pl/ajax/chartersSearch,12755?dt_length=ln7&adults=2&page=1'

        sample3 = SourceDescription()
        sample3.type = 'GET'
        sample3.url = 'http://oferty.tui.pl/ajax/chartersSearch,12755?dt_length=lt7&adults=2&page=1'

        sample4 = SourceDescription()
        sample4.type = 'GET'
        sample4.url = 'http://oferty.tui.pl/ajax/chartersSearch,12755?dt_length=ln911&adults=2&page=1'

        sample5 = SourceDescription()
        sample5.type = 'GET'
        sample5.url = 'http://oferty.tui.pl/ajax/chartersSearch,12755?dt_length=ln9-13&adults=2&page=1'
        # http://oferty.tui.pl/bilety-lotnicze/wyniki-wyszukiwania#page=1
        # http://oferty.tui.pl/ajax/chartersSearch,12755?adults=2&page=28
        # http://oferty.tui.pl/ajax/chartersSearch,12755?dt_length=lt7&adults=2&page=5
        # http://oferty.tui.pl/ajax/chartersSearch,12755?dt_length=ln7&adults=2&page=5
        # http://oferty.tui.pl/ajax/chartersSearch,12755?dt_length=ln911&adults=2&page=5
        # http://oferty.tui.pl/ajax/chartersSearch,12755?dt_length=ln9-13&adults=2&page=5
        page_list = list()
        page_list.append(sample2)
        page_list.append(sample3)
        page_list.append(sample4)
        page_list.append(sample5)

        for airport_code in {'KTW','GDN', 'KRK', 'WRO', 'POZ', 'WAW', 'LCJ', 'RZE', 'BZG'}:
            sample = SourceDescription()
            sample.type = 'GET'
            sample.url = 'http://biletylotnicze.itaka.pl/charter/results-json?departure_date=03.01.2016&dep_name_sel=123%2C[AIRPORT_CODE]&adults=2&children=0&sort_type=1&page=1'
            sample.url = sample.url.replace('[AIRPORT_CODE]', airport_code)
            page_list.append(sample)

        return page_list
