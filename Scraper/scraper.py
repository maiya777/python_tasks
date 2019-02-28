"""Module contains class Scraper and self test code"""

from datetime import datetime
from decimal import Decimal
import re
import requests
from lxml import html


URL = 'https://apps.penguin.bg/fly/quote3.aspx'
AIRPORTS_URL = 'http://www.flybulgarien.dk/en/'
DATAPARAMS = {'lang': 'en', 'paxcount': '1', 'infcount': ''}

class DataError(Exception):
    """This exception is raised when requested airports are not available
    on site or incorrect date requested"""

    pass

class FlightNotFound(Exception):
    """This exception is raised when flights are not found in at least
    one direction"""

    pass

class Scraper(object):
    """This class receives, sort and print
    flight data from the site 'http://www.flybulgarien.dk/en/' which receives
    data from the site 'https://apps.penguin.bg/fly/quote3.aspx'"""

    def __init__(self, dep_code, arr_code, dep_date, rt_date=None):

        self.data_params = dict(DATAPARAMS)
        self.data_params['aptcode1'] = dep_code
        self.data_params['aptcode2'] = arr_code
        self.data_params['depdate'] = dep_date
        if rt_date:
            self.data_params['rtdate'] = rt_date
            self.data_params['rt'] = ''
        else:
            self.data_params['ow'] = ''
        self.url = URL
        self.airports_url = AIRPORTS_URL
        self.flight_notfound_flag = False
        self.converted_flight_list = None
        self.result_flight_list = None

    @staticmethod
    def get_response_text(url, parametres=''):
        """This function receives and returns a response from the site"""

        response = requests.get(url, params=parametres)
        response.raise_for_status()
        return html.fromstring(response.text)

    def check_available_airports(self):
        """This function get a list of available airports from the site and
        checks the requested data on the list"""

        parsed = Scraper.get_response_text(self.airports_url)
        path = '/html/body/div/div/div/form/dl/dd/select/option/@value'
        airports_list = parsed.xpath(path)
        depature_airports_set = set(filter(None, airports_list))
        if self.data_params['aptcode1'] not in depature_airports_set:
            raise DataError('Requested airports '
                            'are not available or do not exist\n')
        arr_airports_url = (self.airports_url[:-3] + 'script/getcity/2-' +
                            self.data_params['aptcode1'])
        arrival_airports = Scraper.get_response_text(arr_airports_url)
        arrival_airports = arrival_airports.xpath('text()')[0].split(',')
        arrival_airports_list = []
        for airport in arrival_airports:
            arrival_airports_list.append(airport.strip('{}\n\t"')[:3])
        if self.data_params['aptcode2'] not in arrival_airports_list:
            raise DataError('Requested airports '
                            'are not available or do not exist\n')

    def check_date_format(self):
        """This function checks the fotmat of the requested date and
        time to flight less than a year"""

        exp = r'[0123]\d\.[01]\d\.20\d\d'
        dates = [self.data_params['depdate']]
        now = datetime.now()
        if 'rtdate' in self.data_params:
            dates.append(self.data_params['rtdate'])
        for date in dates:
            if re.match(exp, date):
                flight_delta = datetime.strptime(date, '%d.%m.%Y') - now
                if flight_delta.days > 365 or flight_delta.days < 0:
                    raise DataError('Incorrect date format\n')
            else:
                raise DataError('Incorrect date format\n')

    def parse_flights_table(self):
        """This function finds and saves all the cells of the table with available
        flights to the list, and also sets the flag "flight_notfound_flag"
        in case finding the message 'No available flights found.'"""

        parsed = Scraper.get_response_text(self.url, self.data_params)
        path = '/html/body/form/div/table[@id="flywiz"]/tr/td/table/tr'
        tr_elements_list = parsed.xpath(path)
        tr_list = []
        try:
            for tr_element in tr_elements_list:
                td_list = []
                tr_list.append(td_list)
                for t_d in tr_element.xpath('td/text()'):
                    if 'No available flights found.' in t_d:
                        raise FlightNotFound
                    td_list.append(t_d.strip())

        except FlightNotFound:
            self.flight_notfound_flag = True

        return tr_list

    @staticmethod
    def normalize_flights_list(row_lst):
        """This function deletes all empty cells, cells with empty elements
        and extra messages and also combines lines of two, so that one list
        item corresponds to one flight"""

        tr_list = [tr for tr in row_lst if tr and all(tr)]
        tr_list = [tr + tr_list[tr_list.index(tr) + 1] for tr in tr_list[::2]]
        luggage_mes = 'NO LUGGAGE INCLUDED IN THE PRICE'
        for i, t_r in enumerate(tr_list):
            if luggage_mes in t_r:
                tr_list[i].remove(luggage_mes)
        return tr_list

    def get_flights_list(self):
        """This function gets and returns flight list"""

        return Scraper.normalize_flights_list(self.parse_flights_table())

    def sort_flights_list(self, flights_lst):
        """This function converts string data to date objects for date
        and decimal format for money and saves this list in class attribute.
        Then it trying to find all the options for round-trip flights and
        saves them in the second list """

        converted_flight_list = []
        result_flight_list = []

        for flight in flights_lst:
            date = datetime.strptime(flight[0].split(',')[1].strip(),
                                     '%d %b %y')
            depdate = datetime.strptime(self.data_params['depdate'],
                                        '%d.%m.%Y')
            if 'rtdate' in self.data_params:
                rtdate = datetime.strptime(self.data_params['rtdate'],
                                           '%d.%m.%Y')
            else:
                rtdate = None

            is_dep_data_correct = (date == depdate and
                                   self.data_params['aptcode1'] in flight[3]
                                   and self.data_params['aptcode2'] in flight[4])
            is_rt_data_correct = (date == rtdate and
                                  self.data_params['aptcode2'] in flight[3]
                                  and self.data_params['aptcode1'] in flight[4])
            if is_dep_data_correct or is_rt_data_correct:

                for flight_time in (flight[1], flight[2]):
                    date = date.replace(hour=int(flight_time[:2]),
                                        minute=int(flight_time[3:]))
                    flight.append(date)
                if flight[-1].time() < flight[-2].time():
                    flight[-1] = flight[-1].replace(day=(flight[-1].day + 1))
                flight[5] = flight[5].split()[1:]
                flight[5][0] = Decimal(flight[5][0])
                del flight[:3]  # deleting old format data from flight the list
                converted_flight_list.append(flight)
        self.converted_flight_list = converted_flight_list

        for i, flight in enumerate(converted_flight_list):
            if self.data_params['aptcode1'] in flight[0]:
                for flight2 in converted_flight_list[i + 1:]:
                    if (self.data_params['aptcode2'] in flight2[0]
                            and flight2[3] > flight[3]):
                        result_flight = (flight, flight2, flight[2][0]
                                         + flight2[2][0])
                        result_flight_list.append(result_flight)
        self.result_flight_list = result_flight_list

    @staticmethod
    def print_flight(dep_airport, dep_time, arr_airport,
                     arr_time, flight_dur):
        """This function prints one formatted line from the flight table"""

        print ('From: {:<25} Departure: {} \nTo: {:<27} Arrival:   {}\n'
               'Flight duration: {}'.format(dep_airport,
                                            dep_time.strftime('%a, %d %B %Y, %H:%M'),
                                            arr_airport,
                                            arr_time.strftime('%a, %d %B %Y, %H:%M'),
                                            str(flight_dur)[:-3]))

    def print_flights(self):
        """This function calls other functions for building flight list,
        displays all found flight options in sorted order, and
        handles arising errors """

        try:
            self.check_available_airports()
            self.check_date_format()
            self.sort_flights_list(self.get_flights_list())

            if 'rtdate' not in self.data_params:
                if (not self.converted_flight_list
                        or self.flight_notfound_flag):
                    print "No available flights found!\n"
            elif (self.converted_flight_list and
                  not self.result_flight_list):
                print "Flights found only in one direction:\n"
            elif not self.converted_flight_list:
                print "No available flights found!\n"

            if self.result_flight_list:
                for flight in sorted(self.result_flight_list,
                                     key=lambda x: x[-1]):
                    for i in range(2):
                        Scraper.print_flight(flight[i][0], flight[i][3],
                                             flight[i][1], flight[i][4],
                                             flight[i][4] - flight[i][3])
                    print "Total cost: {} {}\n".format(flight[-1],
                                                       flight[0][2][1])
            elif self.converted_flight_list:
                for flight in sorted(self.converted_flight_list,
                                     key=lambda x: x[2][0]):
                    Scraper.print_flight(flight[0], flight[3], flight[1],
                                         flight[4], flight[4] - flight[3])
                    print "Total cost: {} {}\n".format(flight[2][0],
                                                       flight[2][1])
        except requests.exceptions.RequestException as exp:
            print exp
        except DataError as exp:
            print exp


if __name__ == '__main__':

    FLIGHTS_DATA = [['BOJ', 'BLL', '22.07.2019', '29.07.2019'],
                    ['CPH', 'BOJ', '17.07.2019'],
                    ['BOJ', 'CPH', '27.06.2019', '02.07.2019'],
                    ['##', '^^^', '$$$$', '&&&&&'],
                    ['BOJ', 'BLL', '12.2019'],
                    ['SOD', 'VAD', '22.07.2019', '29.07.2019'],
                    ['BOJ', 'BLL', '10.07.2019', '11.07.2019'],
                    ['BOJ', 'BLL', '22.07.2019', '23.07.2019'],
                    ['BOJ', 'BLL', '22.07.2019', '29.07.2019', '30.08.2019']]

    for flight_data in FLIGHTS_DATA:
        try:
            scrp = Scraper(*flight_data).print_flights()
            print "-" * 40 + '\n'
        except TypeError:
            print 'You entered incorrect number of parameters, try again!\n'
            print "-" * 40 + '\n'
