#!/usr/bin/python3
"""Test cases for creating objects with parameters in the console."""

import os
import sys
import unittest


class TestParamsCreate(unittest.TestCase):
    """Test cases for creating objects with parameters."""

    def test_create_states(self):
        """Test creating instances of the State class."""
        with os.popen('./console.py', 'w') as console:
            console.write('create State name="California"\n')
            console.write('create State name="Arizona"\n')
            console.write('all State\n')
            console.close()

        with os.popen('./console.py') as console:
            output = console.read()
            self.assertIn('[State]', output)
            self.assertIn('California', output)
            self.assertIn('Arizona', output)

    def test_create_place(self):
        """Test creating instances of the Place class."""
        with os.popen('./console.py', 'w') as console:
            console.write('create Place city_id="0001" user_id="0001" '
                          'name="My_little_house" number_rooms=4 '
                          'number_bathrooms=2 max_guest=10 '
                          'price_by_night=300 latitude=37.773972 '
                          'longitude=-122.431297\n')
            console.write('all Place\n')
            console.close()

        with os.popen('./console.py') as console:
            output = console.read()
            self.assertIn('[Place]', output)
            self.assertIn('My little house', output)


if __name__ == '__main__':
    unittest.main()
