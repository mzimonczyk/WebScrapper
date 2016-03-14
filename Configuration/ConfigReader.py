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

        page_list = list()
        # sample1.url = 'http://biletylotnicze.itaka.pl/charter/results-json
        # ?departure_date=03.01.2016&adults=2&children=0&sort_type=1&page=1'
        page_list.append(SourceDescription('GET', 'http://biletylotnicze.itaka.pl/charter/'
                                                  'results-json?departure_date=03.01.2016&dep_name_sel=123'
                                                  '%2CKTW&adults=2&children=0&sort_type=1&page=1'))
        page_list.append(SourceDescription('GET', 'http://oferty.tui.pl/ajax/chartersSearch,12755'
                                                  '?dt_length=ln7&adults=2&page=1'))
        page_list.append(SourceDescription('GET', 'http://oferty.tui.pl/ajax/chartersSearch,12755'
                                                  '?dt_length=lt7&adults=2&page=1'))
        page_list.append(SourceDescription('GET', 'http://oferty.tui.pl/ajax/chartersSearch,12755'
                                                  '?dt_length=ln911&adults=2&page=1'))
        page_list.append(SourceDescription('GET', 'http://oferty.tui.pl/ajax/chartersSearch,12755'
                                                  '?dt_length=ln9-13&adults=2&page=1'))

        url = 'http://biletylotnicze.itaka.pl/charter/results-json?departure_date=03.01.2016' \
              '&dep_name_sel=123%2C[AIRPORT_CODE]&adults=2&children=0&sort_type=1&page=1'
        for airport_code in {'KTW','GDN', 'KRK', 'WRO', 'POZ', 'WAW', 'LCJ', 'RZE', 'BZG'}:
            page_list.append(SourceDescription('GET', url.replace('[AIRPORT_CODE]', airport_code)))

        url = 'https://www.norwegian.com/pl/rezerwacja/zarezerwuj-przelot/' \
              'wybierz-lot/?D_City=GDN&A_City=[AIRPORT]&D_SelectedDay=04'\
              '&D_Day=04&D_Month=201607&R_SelectedDay=[RETURN_DAY]&R_Day=14&R_Month=201607'\
              '&dFare=595&rFare=421&AgreementCodeFK=-1&CurrencyCode=PLN'
        for airport in ['EVE', 'BDU']:
            for return_day in ['14', '15']:
                page_list.append(SourceDescription('GET', url.replace('[AIRPORT]', airport)
                                                   .replace('[RETURN_DAY]', return_day)))

        def _get_wizzair_urls():
            url = 'https://wizzair.com/pl-PL/TimeTableAjax?departureIATA=[SRC_AIRPORT_CODE]&arrivalIATA=' \
                  '[DST_AIRPORT_CODE]&year=[YEAR]&month=[MONTH]'
            flight_connections = [['GDN', 'AES']
                                  , ['GDN', 'AES'], ['GDN', 'SVG'], ['GDN', 'BGO'], ['GDN', 'TRD']
                                  , ['GDN', 'HAU'], ['GDN', 'MOL'], ['GDN', 'KRS'], ['GDN', 'KEF']
                                  , ['KTW', 'EIN'], ['KTW', 'KUT']
                                  ]
            years = ['2016']
            months = ['7', '8']
            for flight in flight_connections:
                for direction in [[0, 1], [1, 0]]:
                    for year in years:
                        for month in months:
                            yield url.replace('[SRC_AIRPORT_CODE]', flight[direction[0]])\
                                .replace('[DST_AIRPORT_CODE]', flight[direction[1]])\
                                .replace('[YEAR]', year)\
                                .replace('[MONTH]', month)

        for url in _get_wizzair_urls():
            page_list.append(SourceDescription('GET', url))
        return page_list
