#!/usr/bin/env python

# Set configuration and auto acquire long memory (1M) from Rigol DS1052E
# (SW version: 00.04.02.01.00, HW version: 58).

import automatedacquisition

def initSettings(writeHandle):
    writeHandle(':CHAN1:BWL OFF') # CH1 disable BW limit
    writeHandle(':CHAN1:COUP DC') # CH1 DC coupling
    writeHandle(':CHAN1:DISP ON') # CH1 enable
    writeHandle(':CHAN1:INV OFF') # CH1 disable invert
    writeHandle(':CHAN1:SCAL .05') # CH1 vertical scale 50mV
    writeHandle(':CHAN1:OFFS -0.1') # CH1 offset -100mV
    writeHandle(':CHAN2:BWL OFF')
    writeHandle(':CHAN2:COUP DC')
    writeHandle(':CHAN2:DISP OFF') # CH2 disable
    writeHandle(':CHAN2:INV OFF')
    writeHandle(':CHAN2:SCAL 1')
    writeHandle(':CHAN2:OFFS -2')
    writeHandle(':TIM:SCAL .01') # Time scale 10ms
    writeHandle(':TIM:OFFS 0') # Time offset 0
    writeHandle(':TRIG:MODE EDGE') # Trigger on edge
    writeHandle(':TRIG:EDGE:SOUR CHAN1') # CH1 trigger source
    writeHandle(':TRIG:EDGE:SWE SING') # Sweep single
    writeHandle(':TRIG:EDGE:COUP DC') # Trigger DC coupling
    writeHandle(':TRIG:EDGE:SLOP POS') # Trigger on rising edge
    writeHandle(':TRIG:EDGE:LEV .08') # Trigger level 80mV

aa = automatedacquisition.AutomatedAcquisition(3, initSettings) # 3 traces
aa.startCapturing()
