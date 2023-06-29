"""
Unit & Integration test suite
"""

import unittest


# create a test loader
brave_test_loader = unittest.TestLoader()
# find all test modules
brave_unit_test_suite = brave_test_loader.discover("tests/")


# execute test suite
unittest.TextTestRunner(verbosity=3, descriptions=False).run(
    brave_unit_test_suite
)
