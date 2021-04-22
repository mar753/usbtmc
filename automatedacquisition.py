## @package automatedacquisition
# Oscilloscope automated acquisition.
# Tested with Rigol DS1052E (SW version: 00.04.02.01.00, HW version: 58).
# OS: Windows 10 PRO x64.
#
# Requirements:
# - PyVISA
# - VISA USBTMC driver must be installed on Windows.
#
# Author: mar753 (github.com/mar753)

import re
import time
import visa

## AutomatedAcquisition class.
#
# Used to communicate with USBTMC oscilloscopes using PyVISA. We can
# automate capturing voltage traces for SPA/DPA or other purposes.
# Samples of the traces will be stored into files named 'dataCHX_Y.txt',
# where X is a channel number and Y is a trace number.
class AutomatedAcquisition:

    ## The constructor.
    # Initializes values and connects to the first USBTMC device found.
    # @param number_of_traces Number of traces we would like to acquire.
    # @param init_settings_callback Callback with additional settings for
    # the oscilloscope we would like to apply.
    def __init__(self, number_of_traces, init_settings_callback):
        self._init_successful = True
        self._number_of_traces = number_of_traces
        rm = visa.ResourceManager()
        devices = rm.list_resources()
        pattern = re.compile("USB[0-9]+")
        usb_list = list(filter(pattern.match, devices))
        if (len(usb_list) <= 0):
            print("No valid USB device found")
            self._init_successful = False
            return

        # Allocate memory (8-bit per sample) for:
        # 1048576 samples + 10 header (1M points fetch);
        # timeout set to 10s (about 6s per one 1M samples fetch)
        self._device = rm.open_resource(usb_list[0], timeout=10000, chunk_size=1048586)
        self.__reset_settings(init_settings_callback)

    ## Begin capturing method.
    def start_capturing(self):
        if (self._init_successful == False):
            return
        ch2_state = self._device.query(":CHAN2:DISP?")
        self.__write(":RUN")

        for i in range(0, self._number_of_traces):
            self.__wait_for_trigger_to_be_fired()
            self.__channel_acquire(1, i)
            if (ch2_state == "1"):
                self.__channel_acquire(2, i)
            self.__write(":RUN")
        self.close_connection()

    ## Close connection to the device.
    def close_connection(self):
        if (self._init_successful == False):
            return
        self.__write(":KEY:FORCE") # Disables 'Rmt' mode in Rigol
        self._device.close()

    def __channel_acquire(self, channel_number, i):
        self.__write(":WAV:DATA? CHAN" + str(channel_number))
        channel_raw_data = self._device.read_raw()
        channel_raw_data = channel_raw_data[10:] # Cut header
        print("CH" + str(channel_number) + " data size:", len(channel_raw_data))
        f = open("dataCH" + str(channel_number) + "_" + str(i) + ".txt", "wb")
        f.write(channel_raw_data)
        f.close()

    def __reset_settings(self, init_settings_callback):
        self.__write(":STOP")
        self.__write(":ACQ:MEMD LONG") # Memory depth: long memory
        self.__write(":WAV:POIN:MODE RAW") # Get raw samples
        init_settings_callback(self.__write)

    def __wait_for_trigger_to_be_fired(self):
        time.sleep(.1)
        trigger = self._device.query(":TRIG:STAT?")
        while (trigger == "WAIT"):
            time.sleep(1)
            trigger = self._device.query(":TRIG:STAT?")

    def __write(self, command):
        self._device.write(command)
        time.sleep(.1) # Wait additional 100ms for write
