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
    # @param numberOfTraces Number of traces we would like to acquire.
    # @param initSettingsCallback Callback with additional settings for
    # the oscilloscope we would like to apply.
    def __init__(self, numberOfTraces, initSettingsCallback):
        self._initSuccessful = True
        self._numberOfTraces = numberOfTraces
        rm = visa.ResourceManager()
        devices = rm.list_resources()
        pattern = re.compile("USB[0-9]+")
        usbList = filter(pattern.match, devices)
        if (len(usbList) <= 0):
            print("No valid USB device found")
            self._initSuccessful = False
            return

        # Allocate memory (8-bit per sample) for:
        # 1048576 samples + 10 header (1M points fetch);
        # timeout set to 10s (about 6s per one 1M samples fetch)
        self._device = rm.open_resource(usbList[0], timeout=10000, chunk_size=1048586)
        self.__resetSettings(initSettingsCallback)

    ## Begin capturing method.
    def startCapturing(self):
        if (self._initSuccessful == False):
            return
        ch2State = self._device.query(":CHAN2:DISP?")
        self.__write(":RUN")

        for i in range(0, self._numberOfTraces):
            self.__waitForTriggerToBeFired()
            self.__channelAcquire(1, i)
            if (ch2State == "1"):
                self.__channelAcquire(2, i)
            self.__write(":RUN")
        self.closeConnection()

    ## Close connection to the device.
    def closeConnection(self):
        if (self._initSuccessful == False):
            return
        self.__write(":KEY:FORCE") # Disables 'Rmt' mode in Rigol
        self._device.close()

    def __channelAcquire(self, channelNumber, i):
        self.__write(":WAV:DATA? CHAN" + str(channelNumber))
        channelRawData = self._device.read_raw()
        channelRawData = channelRawData[10:] # Cut header
        print("CH" + str(channelNumber) + " data size:", len(channelRawData))
        f = open("dataCH" + str(channelNumber) + "_" + str(i) + ".txt", "w")
        f.write(channelRawData)
        f.close()

    def __resetSettings(self, initSettingsCallback):
        self.__write(":STOP")
        self.__write(":ACQ:MEMD LONG") # Memory depth: long memory
        self.__write(":WAV:POIN:MODE RAW") # Get raw samples
        initSettingsCallback(self.__write)

    def __waitForTriggerToBeFired(self):
        time.sleep(.1)
        trigger = self._device.query(":TRIG:STAT?")
        while (trigger == "WAIT"):
            time.sleep(1)
            trigger = self._device.query(":TRIG:STAT?")

    def __write(self, command):
        self._device.write(command)
        time.sleep(.1) # Wait additional 100ms for write
