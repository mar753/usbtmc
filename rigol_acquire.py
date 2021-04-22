#!/usr/bin/env python

# Set configuration and auto acquire long memory (1M) from Rigol DS1052E
# (SW version: 00.04.02.01.00, HW version: 58).

import automatedacquisition

def init_settings(write_handle):
    write_handle(':CHAN1:BWL OFF') # CH1 disable BW limit
    write_handle(':CHAN1:COUP DC') # CH1 DC coupling
    write_handle(':CHAN1:DISP ON') # CH1 enable
    write_handle(':CHAN1:INV OFF') # CH1 disable invert
    write_handle(':CHAN1:SCAL .05') # CH1 vertical scale 50mV
    write_handle(':CHAN1:OFFS -0.1') # CH1 offset -100mV
    write_handle(':CHAN2:BWL OFF')
    write_handle(':CHAN2:COUP DC')
    write_handle(':CHAN2:DISP OFF') # CH2 disable
    write_handle(':CHAN2:INV OFF')
    write_handle(':CHAN2:SCAL 1')
    write_handle(':CHAN2:OFFS -2')
    write_handle(':TIM:SCAL .01') # Time scale 10ms
    write_handle(':TIM:OFFS 0') # Time offset 0
    write_handle(':TRIG:MODE EDGE') # Trigger on edge
    write_handle(':TRIG:EDGE:SOUR CHAN1') # CH1 trigger source
    write_handle(':TRIG:EDGE:SWE SING') # Sweep single
    write_handle(':TRIG:EDGE:COUP DC') # Trigger DC coupling
    write_handle(':TRIG:EDGE:SLOP POS') # Trigger on rising edge
    write_handle(':TRIG:EDGE:LEV .08') # Trigger level 80mV

aa = automatedacquisition.AutomatedAcquisition(3, init_settings) # 3 traces
aa.start_capturing()
