import unittest
from models import db
import time
from app import app
from databaseHelpers.level import *


class UpdateLevelTest(unittest.TestCase):
    '''
    Tests get_experience_since_last_level() in level.py.
    '''
    def test_calculate_experience_since_last_level(self):
        '''
        Tests get_experience_since_last_level() using sample input.
        '''
        self.assertEqual(0, get_experience_since_last_level(0, 0))
        self.assertEqual(99, get_experience_since_last_level(0, 99))
        self.assertEqual(0, get_experience_since_last_level(1, 100))
        self.assertEqual(199, get_experience_since_last_level(1, 299))
        self.assertEqual(0, get_experience_since_last_level(2, 300))
        self.assertEqual(299, get_experience_since_last_level(2, 599))
        self.assertEqual(0, get_experience_since_last_level(3, 600))
        self.assertEqual(9999, get_experience_since_last_level(99, 504999))
        self.assertEqual(0, get_experience_since_last_level(100, 505000))


if __name__ == "__main__":
    unittest.main()
