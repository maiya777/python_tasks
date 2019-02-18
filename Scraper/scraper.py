"""Module contains class Scraper and self test code"""

from datetime import datetime
from decimal import Decimal
import calendar
import requests
from lxml import html

URL = 'https://apps.penguin.bg/fly/quote3.aspx'
DATAPARAMS = {'lang': 'en', 'paxcount': '1', 'infcount': ''}


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
        self.flight_notfound_flag = False
        self.converted_flight_list = None
        self.result_flight_list = None

    class FlightNotFound(Exception):
        """This exception is raised when flights are not found in at least
        one direction."""

        pass

    class WrongContentException(Exception):
        """This exception is raised when unexpected content received"""
        pass

    def get_response(self):
        """This function receives and returns a response from the site"""

        response = requests.get(self.url, params=self.data_params)
        response.raise_for_status()
        return response

    def parse_flights_table(self):
        """This function finds and saves all the cells of the table with available
        flights to the list, and also sets the flag "flight_notfound_flag" in case
        finding the message 'No available flights found.'"""

        parsed = html.fromstring(self.get_response().text)
        tr_elements_list = parsed.xpath('//tr')
        tr_list = []
        try:
            for tr_element in tr_elements_list:
                td_list = []
                tr_list.append(td_list)
                for t_d in tr_element.xpath('td/text()'):
                    if 'No available flights found.' in t_d:
                        raise self.FlightNotFound
                    td_list.append(t_d.strip())

        except Scraper.FlightNotFound:
            self.flight_notfound_flag = True

        return tr_list

    @staticmethod
    def normalize_flights_list(row_lst):
        """This function deletes all empty cells and cells with empty elements
        and also combines lines of two, so that one list item corresponds
        to one flight"""

        tr_list = [tr for tr in row_lst if tr and all(tr)]
        tr_list = [tr + tr_list[tr_list.index(tr) + 1] for tr in tr_list[::2]]
        return tr_list

    def get_flights_list(self):
        """This function gets and returns flight list"""
        return Scraper.normalize_flights_list(self.parse_flights_table())

    def sort_flights_list(self, flights_lst):
        """This function converts string data to date objects for date
        and decimal format for money and saves this list in class attribute.
        Then it trying to find all the options for round-trip flights and
        saves them in the second list """

        months_dict = dict((v, k) for k, v in enumerate(calendar.month_abbr))
        converted_flight_list = []
        result_flight_list = []

        for flight in flights_lst:
            date = flight[0].split(',')[1].split()
            for flight_time in (flight[1], flight[2]):
                flight.append(datetime(int('20' + date[2]),
                                       int(months_dict[date[1]]),
                                       int(date[0]), int(flight_time[:2])))
            flight[5] = flight[5].split()[1:]
            flight[5][0] = Decimal(flight[5][0])
            del flight[:3]
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

        print ("From: {:<25} Departure: {} \nTo: {:<27} Arrival:   {}\n\
Flight duration: {}".format(dep_airport,
                            dep_time.strftime('%a, %d %B %Y, %H:%M'),
                            arr_airport,
                            arr_time.strftime('%a, %d %B %Y, %H:%M'),
                            str(flight_dur)[:-3]))

    def print_flights(self):
        """This function calls other functions for building flight list,
        displays all found flight options in sorted order, and
        handles arising errors """

        try:
            self.sort_flights_list(self.get_flights_list())
            if self.flight_notfound_flag:
                mes1 = "Flights found only in one direction:\n"
                mes2 = "No available flights found!\n"
                mes = mes1 if self.converted_flight_list else mes2
                print mes

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
            elif not self.flight_notfound_flag:
                raise self.WrongContentException
        except requests.exceptions.HTTPError:
            print 'HTTP Error occured!'
        except requests.exceptions.ConnectionError:
            print 'Connection Error occured!'
        except requests.exceptions.RequestException:
            print 'Network Connection Error!'
        except self.WrongContentException:
            print "Unexpected content. \n\
Apparently, incorrect request parameters\n"


if __name__ == '__main__':

    FLIGHTS_DATA = [['BOJ', 'BLL', '22.07.2019', '29.07.2019'],
                    ['CPH', 'BOJ', '17.07.2019'],
                    ['BOJ', 'CPH', '26.06.2019', '02.07.2030'],
                    ['##', '^^^', '$$$$', '&&&&&'],
                    ['BOJ', 'BLL', '12.12.1734'],
                    ['SOD', 'VAD', '22.07.2019', '29.07.2019'],
                    ['BOJ', 'BLL', '22.07.2019', '23.07.2019'],
                    ['BOJ', 'BLL', '22.07.2019', '29.07.2019', '30.08.2019']]

    for flight_data in FLIGHTS_DATA:
        try:
            scrp = Scraper(*flight_data).print_flights()
            print "-" * 40 + '\n'
        except TypeError:
            print 'You entered incorrect number of parameters, try again!'
