from bs4 import BeautifulSoup
from DataParser import DataParser


class NorwegianFlightParser(DataParser):
    def __init__(self, timestamp):
        columns = ['TIMESTAMP', 'DEPARTURE', 'DEPARTURE_DATE', 'DESTINATION', 'ARRIVAL_DATE'
            , 'PRICE_STANDARD', 'PRICE_STANDARD_PLUS', 'PRICE_FLEX']
        table_name = 'NORWEGIAN_FLIGHT'
        DataParser.__init__(self, timestamp, table_name, columns)

    def parse_data(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        #flights = soup.find_all("tbody")
        #data = soup.select("tbody tr")
        #data = soup.select('tbody tr[class]')
        data = soup.select('tbody tr[class*="row"]')
        for row in data:
            if row.attrs['class'] is not None:
                if 'rowinfo1' in row.attrs['class']:
                    row1 = row
                elif 'rowinfo2' in row.attrs['class']:
                    row2 = row
                elif 'lastrow' in row.attrs['class']:
                    last_row = row
                    self._parse_flight(row1, row2, last_row)
                    row1 = row2 = last_row = None
                pass
        pass

    def _parse_flight(self, row1, row2, last_row):
        if row1 is None or row2 is None:
            return
        #departure_hour = row1.select('td[class="depdest"]')[0].string
        departure_hour = row1.find_all('td', attrs={'class': 'depdest'})[0].text
        departure_city = row2.select('td[class="depdest"]')[0].text
        arrival_hour = row1.select('td[class="arrdest"]')[0].text
        arrival_city = row2.select('td[class="arrdest"]')[0].text
        price_standardlowfare = ''
        price_standardlowfareplus = ''
        price_standardflex = ''

        price_data = row1.find_all('td', attrs={'class': 'fareselect standardlowfare'})
        if len(price_data) == 0:
            price_data = row1.find_all('td', attrs={'class': 'fareselect standardlowfare selectedfare'})
        if len(price_data) > 0:
            price_standardlowfare = price_data[0].text

        price_data = row1.find_all('td', attrs={'class': 'fareselect standardlowfareplus'})
        if len(price_data) == 0:
            price_data = row1.find_all('td', attrs={'class': 'fareselect standardlowfareplus selectedfare'})
        if len(price_data) > 0:
            price_standardlowfareplus = price_data[0].text

        price_data = row1.find_all('td', attrs={'class': 'fareselect standardflex endcell'})
        if len(price_data) == 0:
            price_data = row1.find_all('td', attrs={'class': 'fareselect standardflex endcell selectedfare'})
        if len(price_data) > 0:
            price_standardflex = price_data[0].text

        self._data.add_row([self._timestamp
                           , departure_city
                           , departure_hour
                           , arrival_city
                           , arrival_hour
                           , self._format_price(price_standardlowfare)
                           , self._format_price(price_standardlowfareplus)
                           , self._format_price(price_standardflex)
                        ])

    def _format_price(self, price):
        price = price.replace(u'\xa0', u' ')
        return price.strip()
