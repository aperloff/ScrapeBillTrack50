#!/usr/bin/env python3

"""This module contains the pytest tests for the modules:
    1. ScrapeBillTrack50.py
    2. check_for_dependencies.py

    Note: you can use the decorator '@pytest.mark.skip(reason="taskes a long time to run")' to skip over a test
"""

from __future__ import absolute_import
import os
import sys
sys.path.insert(1, os.path.dirname(os.path.realpath(__file__))+'/..')

# pylint: disable=wrong-import-position
import check_for_dependencies
import ScrapeBillTrack50
# pylint: enable=wrong-import-position
# pylint: disable=no-self-use

class TestCheckForDependencies:
    """Class containing the tests for the check_for_dependencies module.
    We want to make sure that the checks for the dependencies will work.
    """

    def test_is_tool(self):
        """Check for a common executable to see if this function even works"""

        assert check_for_dependencies.is_tool("ls")

    def test_check_pip_dependencies(self):
        """Check if we can test for the most basic of pip installed dependencies"""

        dep = {"urllib3" : []}
        assert len(check_for_dependencies.check_pip_dependencies(dep)) == 0

    def test_check_try_dependencies(self):
        """Check if we can test for the most basic of python modules"""

        dep = ["os","sys"]
        assert len(check_for_dependencies.check_try_dependencies(dep)) == 0

    def test_check_system_dependencies(self):
        """Check if we can test for simple system installed dependencies"""

        dep = ["ls"]
        assert len(check_for_dependencies.check_system_dependencies(dep)) == 0

class TestStaffer:
    """Class containing the tests for the Staffer class."""

    def test_staffer(self):
        """Tests the Institution class to make sure that it's attributes are set correctly"""

        staffer = ScrapeBillTrack50.Staffer("Name", "Title", "Role", "Location", "Address", "Phone", "Email")
        assert staffer.name == "Name" and \
               staffer.title == "Title" and \
               staffer.role_description == "Role" and \
               staffer.location == "Location" and \
               staffer.address == "Address" and \
               staffer.phone == "Phone" and \
               staffer.email == "Email"

class TestScrapeBillTrack50:
    """This section covers the integration tests.
    These tests will make sure that all of the code works in harmony.
    """

    def test_scrape_bill_track_50(self):
        """Performs a check on the main function of the code.
        In the end we will be making sure that an image file is created.
        """

        schedulers = ScrapeBillTrack50.scrape_bill_track_50(['-C','test/test_assignments.py'])
        print(schedulers)
        assert schedulers['Richard Durbin'][0].location == "Capitol Office"
