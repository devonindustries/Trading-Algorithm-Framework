import unittest
from trading_algorithm_framework import portfolio as pf

class Test_Portfolio(unittest.TestCase):

    def store_share(self):
        
        test_share = pf.Share(1, 1, '2021-03-05')
        test_share.set_id(1)

        test_share.set_id(2)

        temp_id = test_share.get_id()

        self.assertEqual(temp_id, 1)