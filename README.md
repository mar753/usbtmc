# Rigol DS1052E long mem automated acquisition (USBTMC)

This repository contains automatedacquisition python script which is used to automate traces acquisition from Rigol DS1052E digital oscilloscope (tested with SW version: 00.04.02.01.00 and HW version: 58) using long memory (1M points) and single sweep or other oscilloscopes which uses USBTMC specification. Oscilloscope must be connected to a PC with USB cable. DS1052E oscilloscope has 8-bit vertical resolution thus output sample files have exactly 1024 bytes of length (when only one channel is used), and 512 bytes (when both channels are used). VISA drivers will be needed. Tested with Windows 10 PRO x64.

If you would like to use it under Linux (like Ubuntu) where driver for usbtmc devices should be already present, the best way will be to write a simple class which reads/writes raw data from '/dev/usbtmc0' (or other number your device was assigned to) instead of PyVISA.

## Requirements

- VISA USBTMC drivers (e.g. NI-VISA)
- Python - tested with Python 2.7.15 and 3.6.5, but older should work as well
- PyVISA - for Windows
- Windows environment (Linux with some modifications)

## Running

Just execute rigol_acquire.py script, which is a sample how to use automatedacquisition.py class in case of Rigol DS1052E.
