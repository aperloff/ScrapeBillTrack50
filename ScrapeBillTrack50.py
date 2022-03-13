#!/bin/env python3

"""ScrapeBillTrack50

This module allows the user to pull provide a list of legislator names and pull selected information from
the Bill Track 50 website (https://www.billtrack50.com).

Functions
---------
scrape_bill_track_50
    The main function of the module
"""

from argparse import RawTextHelpFormatter
import sys
import urllib

from magiconfig import ArgumentParser, MagiConfigOptions

from googlesearch import search
from bs4 import BeautifulSoup

class Staffer:
    """A class which contains the information about a single Staffer.

    Attributes
    ----------
    name : str
        The name of the staffer
    title : str
        The staffers official title
    role_description : str
        A description of the staffers role
    location : str
        The description of the office at which the staffer works
    address : str
        The address to the office at which the staffer works
    phone : str
        The phone number of the staffer
    email : str
        The email address of the staffer
    """

    def __init__(self, name, title, role_description, location, address, phone, email):
        """This method initializes the data members of the Staffer class.

        Parameters
        ----------
        name : str
            The name of the staffer
        title : str
            The staffers official title
        role_description : str
            A description of the staffers role
        location : str
            The description of the office at which the staffer works
        address : str
            The address to the office at which the staffer works
        phone : str
            The phone number of the staffer
        email : str
            The email address of the staffer
        """

        self.name = name
        self.title = title
        self.role_description = role_description
        self.location = location
        self.address = address
        self.phone = phone
        self.email = email

    def __repr__(self):
        """Return a formated string representation of the Staffer object"""

        formatted_fields = ', '.join(f"{key} = {value}" for key, value in self.__dict__.items())
        return f"Staffer({formatted_fields})"

    def __str__(self):
        """Return a formatted string to print for the Staffer object"""

        return f"Staffer({self.name} | {self.title} | {self.role_description} | {self.email})"

def get_schedulers_from_table(staff_list, quiet = False):
    """From a HTML table, get the list of schedulers

    Parameters
    ----------
    staff_list : list
        A list of HTML table rows
    quiet : bool
        If Ture, silences the printouts
    """

    schedulers = []
    for staff in staff_list:
        fields = staff.find_all('td')
        is_scheduler = any("Scheduler" in field for field in fields)
        if is_scheduler:
            schedulers.append(
                Staffer(name = fields[0].string,
                        title = fields[1].string,
                        role_description = fields[2].string,
                        location = fields[3].string,
                        address = fields[4].string,
                        phone = fields[5].string,
                        email = fields[6].string)
            )
            if not quiet:
                print(f"\t\t{schedulers[-1]}")
    return schedulers

def scrape_bill_track_50(argv = None):
    """The main function for this scrip

    Parameters
    ----------
    argv : str, optional
        A list of command line arguments
    """

    if argv is None:
        argv = sys.argv[1:]

    parser = ArgumentParser(config_options=MagiConfigOptions(),
                            formatter_class=RawTextHelpFormatter,
                            description="Scrape https://www.BillTrack50.com for specific information.",
                            epilog = """examples:
    using a magiconfig file:
        `python3 ScrapeBillTrack50.py -C configs/assignments.py`"""
    )
    parser.add_argument("-d", "--debug", action = "store_true",
                        help = "Shows some extra information in order to debug this program (default=%(default)s)")
    parser.add_argument("-l", "--legislators", nargs = "+",
                        help = "A list of names of legislators (default=%(default)s)")
    parser.add_argument("-q", "--quiet", action = "store_true",
                        help = "Silences the normal outputs (default=%(default)s)")
    args = parser.parse_args(args = argv)

    if args.debug:
        print('Number of arguments:', len(sys.argv), 'arguments.')
        print('Argument List:', str(sys.argv))
        print("Argument", args)

    query_base = "billtrack50"

    results = {}
    for legislator in args.legislators:
        if not args.quiet:
            print("==========")
        query = query_base + " " + legislator
        if args.debug:
            print(f"Search query: \"{query}\"")
        search_result = search(query, num_results = 1).__next__()
        if args.debug:
            print(f"Search result url: \"{search_result}\"")

        soup = None
        with urllib.request.urlopen(search_result) as thepage:
            soup = BeautifulSoup(thepage, "html.parser")

        if soup is not None:
            legislator_name = soup.title.text.split(" | ")[0]
            legislator_number = soup.find_all("img","d-block")[0]['src'].split('/')[-1]
            if not args.quiet:
                print(f"Information for {legislator_name}:")
                print(f"\tBill Track 50 ID: {legislator_number}")
                print("\tSchedulers:")

            staff_table = soup.find('div','tab-pane fade show','staff-tab', id='staff')
            staff_list = staff_table.find_all('tr')
            schedulers = get_schedulers_from_table(staff_list, quiet = args.quiet)
            if len(schedulers) == 0:
                if not args.quiet:
                    print("\t\t<none found>")
            if not args.quiet:
                print("")
            results[legislator] = schedulers
        else:
            raise RuntimeError(f"Unable to open the bill Track 50 page for {legislator}.")

        return results

if __name__ == "__main__":
    scrape_bill_track_50()
