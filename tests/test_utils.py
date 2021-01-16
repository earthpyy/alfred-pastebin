from unittest import TestCase

from alfred_pastebin.utils import *
from alfred_pastebin.variables import DEFAULT_NAME


class GetNameTextTestCase(TestCase):
    def test_simple(self):
        query = 'test'
        self.assertEqual(get_name_text(query), 'test')

    def test_empty(self):
        query = ''
        self.assertEqual(get_name_text(query), DEFAULT_NAME)

    def test_none(self):
        query = None
        self.assertEqual(get_name_text(query), DEFAULT_NAME)
