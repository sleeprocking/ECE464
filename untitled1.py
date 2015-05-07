#!/usr/bin/python

import time, signal, sys
import numpy
import pylab as pl
import scipy
from scipy import fftpack
from scipy.io.wavfile import write
from Adafruit_ADS1x15 import ADS1x15
from ftplib import FTP

def signal_handler(signal, frame):
        #print 'You pressed Ctrl+C!'
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
#print 'Press Ctrl+C to exit'

ADS1015 = 0x00	# 12-bit ADC
ADS1115 = 0x01	# 16-bit ADC

# Initialise the ADC using the default mode (use default I2C address)
# Set this to ADS1015 or ADS1115 depending on the ADC you are using!
adc = ADS1x15(ic=ADS1015)
fs = 3300
ch01 = numpy.zeros([50,1])
ch23 = numpy.zeros([50,1])

for i in range(len(ch01)): 
    ch01[i]= adc.readADCDifferential01(4096,fs)
    ch23[i]= adc.readADCDifferential23(4096,fs)

a = {}
a['ch01'] = ch01
a['ch23'] = ch23

#ch03=numpy.concatenate([ch0,ch1,ch2,ch3], axis=1)
#print ch03
#CH0 = scipy.fftpack.fft(ch0)
#CH0 = numpy.absolute(CH0)
#t = numpy.linspace(0, len(ch0)/fs,len(ch0))
#f = numpy.linspace(0,fs,len(CH0))
#pl.plot(ch0,t)
#pl.show()
#ch0 = numpy.int32(ch0)
filename = 'test'
scipy.io.savemat(filename, {'a':a})

#host = '192.168.43.43'

#ftp = FTP(host)
#ftp.connect(host,2121)
#ftp.login()
#ftp.cwd("/")
#ftp.transfercmd("STOR "+filename)
#ftp.quit()
