import unittest
from unittest import mock


class test_buttons(unittest.TestCase):

    def test_buttons_intitialzed_to_false(self):
        with mock.patch('buttons.RPI.GPIO') as mocked_RPi:
            mybuttons = mocked_RPi(35, 40, 38)
            return not mybuttons.read_interval_state()[0]


if __name__ == '__main__':
    unittest.main()