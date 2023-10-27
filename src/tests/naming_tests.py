import unittest

from src.sb_serializer import Naming


class NamingTests(unittest.TestCase):
    def setUp(self):
        self.naming = Naming("../../dictionary.txt", "../../bigworddictionary.txt")

    def test_name(self):
        name_value = "Stephen"
        result = self.naming.string_to_name(name_value)
        self.assertEqual(result.lower(), "stephen")
        self.assertEqual(result.upper(), "STEPHEN")
        self.assertEqual(result.pascal(), "Stephen")
        self.assertEqual(result.camel(), "stephen")
        self.assertEqual(result.snake(), "stephen")

    def test_complex_name(self):
        name_value = "currentemployeerecord"
        result = self.naming.string_to_name(name_value)
        self.assertEqual(result.lower(), "currentemployeerecord")
        self.assertEqual(result.upper(), "CURRENTEMPLOYEERECORD")
        self.assertEqual(result.pascal(), "CurrentEmployeeRecord")
        self.assertEqual(result.camel(), "currentEmployeeRecord")
        self.assertEqual(result.snake(), "current_employee_record")

    def test_bigword_name(self):
        name_value = "scaninterestrates"
        result = self.naming.string_to_name(name_value)
        self.assertEqual(result.lower(), "scaninterestrates")
        self.assertEqual(result.upper(), "SCANINTERESTRATES")
        self.assertEqual(result.pascal(), "ScanInterestRates")
        self.assertEqual(result.camel(), "scanInterestRates")
        self.assertEqual(result.snake(), "scan_interest_rates")
        self.assertEqual(result.upper_snake(), "SCAN_INTEREST_RATES")

