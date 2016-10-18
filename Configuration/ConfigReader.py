from Configuration.SourceDescription import SourceDescription
from datetime import datetime, timedelta

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

        for url in self._get_wizzair_urls():
            page_list.append(SourceDescription('GET', url))
        for url in self._get_rainbow_urls():
            page_list.append(SourceDescription('GET', url))
        page_list = []
        for url in self._get_ryanair_urls():
            page_list.append(SourceDescription('GET', url))
        return page_list

    def _get_wizzair_urls(self):
            url = 'https://book.wizzair.com/pl-PL/TimeTableAjax?departureIATA=[SRC_AIRPORT_CODE]&arrivalIATA=' \
                  '[DST_AIRPORT_CODE]&year=[YEAR]&month=[MONTH]'
            flight_connections = [['KTW', 'KEF']
                                 # , ['GDN', 'AES'], ['GDN', 'SVG'], ['GDN', 'BGO'], ['GDN', 'TRD']
                                 # , ['GDN', 'HAU'], ['GDN', 'MOL'], ['GDN', 'KRS'], ['GDN', 'KEF']
                                  , ['KTW', 'EIN'], ['KTW', 'KUT'], ['KTW', 'ACE'], ['KTW', 'LIS'], ['KTW', 'DWC']
                                  , ['KTW', 'TFS'], ['KTW', 'TLV'], ['KTW', 'AHO']
                                  ]
            years = ['2016', '2017']
            months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
            for flight in flight_connections:
                for direction in [[0, 1], [1, 0]]:
                    for year in years:
                        for month in months:
                            yield url.replace('[SRC_AIRPORT_CODE]', flight[direction[0]])\
                                .replace('[DST_AIRPORT_CODE]', flight[direction[1]])\
                                .replace('[YEAR]', year)\
                                .replace('[MONTH]', month)

    def _get_rainbow_urls(self):
        # http://biletyczarterowe.r.pl/Wyszukiwanie?&miastaWylotuZ=[%22KTW%22]&miastaWylotuDo=[%22TFS%22]&miastaPowrotuZ=[%22TFS%22]&miastaPowrotuDo=[%22KTW%22]&dataWylotuOd=2017-04-01&liczbaPasazerow=1&dataPowrotuOd=2017-05-01&wObieStrony=1&nowe=1
        date_from = datetime.now().strftime('%Y-%m-%d')
        people_count = str(2)
        src_airports = ['KTW', 'WAW', 'KRK', 'WRO']
        dst_airports = ['TFS','RMF','NBE','SKG','GPA','AGA','AYT','BJV','DLM','OLB','SUF','CTA','NAP','FUE','FAO','AGP'
            ,'LEI','GRO','RHO','KGS','CHQ','HER','PMI','LCA','HRG','SSH','BOJ','VAR'
            ,'TFS','FUE','TRN','NBE','AGA','HRG','JTR','SKG','GPA','SGN','BKK','DPS','AYT','BJV','DLM','OLB','CAG','CMB'
            ,'RMF','SUF','NAP','BJL','CTA','TPS','ACE','FAO','VRA','CCC','CUN','AGP','LEI','GRO','VRN','BUS','RHO','KGS'
            ,'MRU','CHQ','HER','PMI','TNR','LCA','SSH','BOJ','VAR','GNB','FJR','LPA','MBA'
            ,'SKG','AYT','FAO','BCN','RHO','KGS','CHQ','PMI','BOJ','VAR']
        dst_airports = list(set(dst_airports))
        url = 'http://biletyczarterowe.r.pl/Wyszukiwanie?' \
               '&miastaWylotuZ=[%22[SRC_AIRPORT_CODE]%22]&miastaWylotuDo=[%22[DST_AIRPORT_CODE]%22]' \
               '&miastaPowrotuZ=[%22[DST_AIRPORT_CODE]%22]&miastaPowrotuDo=[%22[SRC_AIRPORT_CODE]%22]' \
               '&dataWylotuOd=[DATE_FROM]&liczbaPasazerow=[PEOPLE_COUNT]&dataPowrotuOd=[DATE_FROM]&wObieStrony=1&nowe=1'

        url = url.replace('[PEOPLE_COUNT]', people_count).replace('[DATE_FROM]', date_from)
        for src_airport in src_airports:
            for dst_airport in dst_airports:
                yield url.replace('[SRC_AIRPORT_CODE]', src_airport).replace('[DST_AIRPORT_CODE]', dst_airport)

    def _get_ryanair_urls(self):
        # https://www.ryanair.com/pl/api/2/flights/from/BVA/to/OPO/2015-06-01/2018-07-02/outbound/cheapest-per-day/
        date_from = datetime.now().strftime('%Y-%m-%d')
        date_to = (datetime.now()+timedelta(days=366)).strftime('%Y-%m-%d')
        src_airports = ['KRK', 'WAW', 'KTW']
        dst_airports = ['TFS','OPO','PLM']
        url = 'https://www.ryanair.com/pl/api/2/flights/from/[SRC_AIRPORT_CODE]/to/[DST_AIRPORT_CODE]/[DATE_FROM]/[DATE_TO]/outbound/cheapest-per-day/'
        url = url.replace('[DATE_FROM]', date_from).replace('[DATE_TO]', date_to)
        for src_airport in src_airports:
            for dst_airport in dst_airports:
                yield url.replace('[SRC_AIRPORT_CODE]', src_airport).replace('[DST_AIRPORT_CODE]', dst_airport)
                yield url.replace('[SRC_AIRPORT_CODE]', dst_airport).replace('[DST_AIRPORT_CODE]', src_airport)