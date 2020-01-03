#!/usr/bin/python3
import unittest
import index
from index import *
import index as app

"""
Unit Test for petitions 
"""

class TestSum(unittest.TestCase):


    def test_error_notfound_main(self):
        self.assertEqual(app.render_main_page("asas"), ["NOT FOUND"], "Insert a bad index in main page return failed message")

    def test_error_failed_geting_pict(self):
        self.assertEqual(app.get_person_pict("asas"), [], "Failed getting a pict must return a []")
        
    def test_error_failed_geting_character(self):
        self.assertEqual(app.get_chara_info("asas",""), [], "Failed getting a character info return []")

if __name__ == '__main__':
    unittest.main()