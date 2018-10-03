import unittest
from unittest import mock
import buttons

class test_buttons(unittest.TestCase):

    def test_buttons_intitialzed_to_false(self):
        with mock.patch('buttons.RPi.GPIO') as mocked_GPIO:
            mybuttons = mocked_GPIO.buttons(35, 40, 38)
            return not mybuttons.read_interval_state()[0]


if __name__ == '__main__':
    unittest.main()