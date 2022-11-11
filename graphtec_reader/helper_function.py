import numpy as np
from bs4 import BeautifulSoup
from requests import get
from pandas import DataFrame
from pyvisa import ResourceManager
from datetime import datetime as dt
import pytz
import glob
import time
from custom_logger import CustomLoggerWrapper


class Graphtec():

    # -----------------------------------
    def __init__(self, address, resource_manager):
        self.address = address
        # TCPIP adress to contact
        # self.tcpip_gl = f"TCPIP::{self.address}::8023::SOCKET"
        # self.instrument = resource_manager.open_resource(self.tcpip_gl,
                                                        #  write_termination='\n',
                                                        #  read_termination='\r\n')
        #self.query_id = self.get_graphtec_idn()
        # Holds measurement data
        self.data = []

    # -----------------------------------
    def append_graphtec_readings(self):
        """Find all the measurements of the channels and append to self.data list"""
        # Format URL
        address_channel_data = f"http://{self.address}/digital.cgi?chgrp=13"

        # Get http response
        # Get response from the channel data page
        response = get(address_channel_data)

        # Create response table
        # Create a soup object from this, which is used to create a table
        soup_object = BeautifulSoup(response.text, 'html.parser')
        # Holds all the found data > in format: [('CH 1', '+  10', 'degC'), (CH2 ....]
        channels_data = []
        # Table with all the channels as subtables > based on the HTML table class > example: [table: [table, table, table]]
        for table in soup_object.find_all(border="1"):
            # Tables of all the individual channels > Search for table again to get: [table, table, table], each one corresponds to one channel
            channel_readings_html = table.findAll('table')

        # Loop over table to yield formatted data

            for channel_read_html in channel_readings_html:
                # Returns a row for each measurement channel with relevant data > [<b> CH 1</b>, <b> -------</b>, <b> degC</b>]
                reading_html = channel_read_html.find_all('b')

                # Strips the string of its unicode characters and puts it into a list > ['CH 1', '-------', 'degC']
                reading_list = [read_tag.get_text(
                    strip=True) for read_tag in reading_html]
                channels_data.append(reading_list)

        # Append the data to the list
        self.data.append(channels_data)

    # -----------------------------------
    def get_graphtec_idn(self):
        pass
        # """SCPI command to get IDN"""
        # idn = self.instrument.query("*IDN?")
        # return idn

    # -----------------------------------
    def add_channel_data_to_df(self):
        """Post processing method to format self.data list into a Pandas DataFrame"""

        name_index = 0      # Format is ['CH 1', '23.56', 'degC']
        # so index 0, 1 and 2 are, respectively channel name, value reading and unit.
        reading_index = 1
        unit_index = 2

        # Amount of channels to loop over, might depend on Graphtec device (I have 20)
        channel_count = len(self.data[0])
        df = DataFrame()

        # Loop over each channel
        for channel_ind in range(channel_count):

            # get the channel name
            channel_name = self.data[0][channel_ind][name_index]
            channel_unit = self.data[0][channel_ind][unit_index]    # and unit
            # Format column name "GRPH CH1 [degC]"
            column_name = f"GRPH {channel_name} [{channel_unit}]"

            # Stores the channel data > [0.0, 0.1, 0.0 ....]
            channel_readings = []
            channel_name_del = []
            # only save open channels
            if "CH 1 [degC]" in column_name or "CH 2 [degC]" in column_name or "CH 3 [degC]" in column_name or "GS 2" in column_name:
                # Loop over each row and retrieve channel data
                for row in self.data:
                    # Read the data of channel for this row
                    channel_reading = row[channel_ind][reading_index]

                    # Value formatting
                    if channel_reading == '' or channel_reading == 'BURNOUT' or channel_reading == 'Off':
                        channel_reading = 0
                        channel_name_del.append(channel_name)
                    else:
                        # Float for other values, remove spaces in order to have +/-
                        channel_reading = float(
                            channel_reading.replace(' ', ''))
                    channel_readings.append(channel_reading)
                # Add a new column with data
                df[column_name] = channel_readings
        return df


class GraphtecWithLogger(Graphtec):

    def __init__(self, address, resource_manager):
        super().__init__(address, resource_manager)
    
    def append_graphtec_readings(self):
        _data = super().append_graphtec_readings()()
        print(_data)

def readFromGraphtec(port, time_interval, logfile_name):
    logger_wrapper = CustomLoggerWrapper(
        "Graphtec_logger", log_filename=logfile_name)
    logger_wrapper.InitLogger()
    mylogger = logger_wrapper.GetInitedLogger()
    # Need a resourcemanager to communicate with Graphtec via PyVisa
    rm = ResourceManager("@py")
    # Can be setup on Graphtec with "Menu > I/F > IP ADDRESS" (change with buttons)
    # ip_graphtec = "192.168.10.20"
    # Sometimes errors arise here if you can not connect, restarting the Graphtec or doing "Menu > I/F > Apply Setting" Sometimes helps. Also, try if you can visit the ip address in browser directly.
    graphtec = GraphtecWithLogger(port, rm)

    try:
        while True:
            graphtec.append_graphtec_readings()  # Measure and append to data list
            # Reading every 0.2 seconds
            time.sleep(time_interval)
    except KeyboardInterrupt as error:
        print(error)
        mylogger.warning("End temperature recoding from keyboard")
