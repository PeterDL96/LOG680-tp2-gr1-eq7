"""This script is used to test the function in main.py"""

import unittest
import os
import sys
import requests
# pylint: disable=wrong-import-position
sys.path.append(os.getcwd())
from src.main import Main
from datetime import datetime
# import mysql.connector as mysql

HOST = os.environ["HVAC_HOST"]
TOKEN = "89103df59ad0cda23c2f"
TICKS = "6"
HOT_LIMIT = "80"
COLD_LIMIT = "20"

class TestStringMethods(unittest.TestCase):


    """Test class for the Main class"""
    def test_simulator_up(self):
        """Function to test if we receive an information from the server"""
        request = requests.get(f"{HOST}/api/health")
        self.assertEqual("All system operational Commander !", request.text)

    def test_token(self):
        """Test if the token in the environment variable is good"""
        hvac = Main()
        self.assertEqual(TOKEN, hvac.token)

    def test_hot_limit(self):
        """Test if the hot limit is different from the default value"""
        hvac = Main()
        self.assertNotEqual(HOT_LIMIT, hvac.hot_limit)


    def test_cold_limit(self):
        """Test if the cold limit is different from the default value"""
        hvac = Main()
        self.assertNotEqual(COLD_LIMIT, hvac.cold_limit)

    def test_ticks(self):
        """Test if the number of ticks is different from the default value"""
        hvac = Main()
        self.assertNotEqual(TICKS, hvac.ticks)

    def test_db(self):
        hvac = Main()

        # Data used for testing
        timestamp = datetime.now()
        temperature = 400.40
        hvacTestEvent = "TestingHVAC"
        testingTicks = 6

        # Get connection to DB
        connection = hvac.connectToDb()

        # Test to see if it is opened
        self.assertEqual(connection.open, True)

        # Test adding temperature to DB
        self.assertEqual(hvac.insert_temperature_toDb(timestamp, temperature), True)

        # Test adding an event to DB
        self.assertEqual(hvac.insert_hvac_event_toDb(timestamp, hvacTestEvent, testingTicks), True)




        # Convert time format into how it is saved in DB
        timeDB = timestamp.strftime("%y-%m-%d %H:%M:%S")

        # Test deleting from DB + also delete rows that were just added for testing purposes
        self.assertEqual(self.__deleteTemperatureFromDB(hvac.connectToDb(), timeDB, temperature), True)
        self.assertEqual(self.__deleteEventFromDB(hvac.connectToDb(), timeDB, hvacTestEvent), True)


    def __deleteTemperatureFromDB(self, connection, timeDB, temperature):
        try:
            with connection:
                with connection.cursor() as cursor:

                    # Delete record used for testing
                    delsql = f"DELETE FROM `TEMPERATURE` WHERE timestamp='{timeDB}' AND temperature='{temperature}'"
                    cursor.execute(delsql)

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()
                return True

        except Exception as err:
            print(err)
            return False

    def __deleteEventFromDB(self, connection, timeDB, hvacTestingEvent):

        try:
            with connection:
                with connection.cursor() as cursor:

                    # Delete record used for testing
                    delsql = f"DELETE FROM `HVAC_EVENT` WHERE timestamp='{timeDB}' AND event='{hvacTestingEvent}'"
                    cursor.execute(delsql)

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()
                return True

        except Exception as err:
            print(err)
            return False


if __name__ == '__main__':
    unittest.main()
