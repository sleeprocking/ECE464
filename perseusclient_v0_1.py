# -*- coding: utf-8 -*-
"""
Created on Thu Apr 02 20:59:44 2015

@author: C15Trevor.Moore
"""
import serial, time, sys, os, win32file, win32event, win32con, numpy, scipy
import matplotlib.pyplot as plt
from scipy import signal
from scipy import io
from scipy.io import wavfile
from scipy import fftpack

def tdoaangle(path, added, fc):
    filename = path+''.join(added)
    fs, data = scipy.io.wavfile.read(filename)
    dataf0 = scipy.signal.lfilter(filtnum[:,0], filtden[:,0], data[:,0])
    dataf1 = scipy.signal.lfilter(filtnum[:,0], filtden[:,0], data[:,1])
    r = numpy.correlate(dataf0, dataf1, "full")
    r = r/max(r)
    lag = numpy.argmax(r)-int(len(r)/2)
    number = 2*float(lag)*fc/fs;
    rad = scipy.arccos(number);
    theta = rad*180/numpy.pi;
    return (rad, theta)
    
def tdoa(rad1, rad2, sensor_dist):
    rad3 = rad2-rad1;
    L1 = sensor_dist*numpy.sin(rad1)/numpy.sin(rad3);
    L2 = sensor_dist*numpy.sin(rad2)/numpy.sin(rad3);
    x = sensor_dist*numpy.cos(rad1);
    y = sensor_dist*numpy.sin(rad1);
    return (x, y)
    
def steerservo(x,num):
    if x == 0 :
        ser.write(b"\xFF"+num+"\x00")
    elif x==1:
        ser.write(b"\xFF"+num+"\xa0")
    else:
         ser.write(b"\xFF"+num+"\xf0")   
    return
    
ser = serial.Serial(14)
ser.baudrate=9600
i=0 
fc = 1000
sensor_dist = 200
filtcoeffs = 'C:/Users/C15Trevor.Moore/Documents/MATLAB/capstone1.mat'
filtnum = scipy.io.loadmat(filtcoeffs)['Num']
filtden = scipy.io.loadmat(filtcoeffs)['Den']
path = 'C:/Users/C15Trevor.Moore/Documents/My_Received_Files/'
path_to_watch = os.path.abspath ("C:/Users/C15Trevor.Moore/Documents/My_Received_Files")

#
# FindFirstChangeNotification sets up a handle for watching
#  file changes. The first parameter is the path to be
#  watched; the second is a boolean indicating whether the
#  directories underneath the one specified are to be watched;
#  the third is a list of flags as to what kind of changes to
#  watch for. We're just looking at file additions / deletions.
#
change_handle = win32file.FindFirstChangeNotification (
  path_to_watch,
  0,
  win32con.FILE_NOTIFY_CHANGE_FILE_NAME
)

#
# Loop forever, listing any file changes. The WaitFor... will
#  time out every half a second allowing for keyboard interrupts
#  to terminate the loop.
#
try:

  old_path_contents = dict ([(f, None) for f in os.listdir (path_to_watch)])
  while 1:
    result = win32event.WaitForSingleObject (change_handle, 500)

    #
    # If the WaitFor... returned because of a notification (as
    #  opposed to timing out or some error) then look for the
    #  changes in the directory contents.
    #
    if result == win32con.WAIT_OBJECT_0:
      new_path_contents = dict ([(f, None) for f in os.listdir (path_to_watch)])
      added = [f for f in new_path_contents if not f in old_path_contents]
      if (added and i==0): 
          rad1, theta1 = tdoaangle(path, added, fc)
          i+=1
      elif (added and i==1):
          rad2, theta2 = tdoaangle(path, added, fc)
          i=2
      else:
          x, y = tdoa(rad1, rad2, sensor_dist)
          i=0
          
      old_path_contents = new_path_contents
      win32file.FindNextChangeNotification (change_handle)

finally:
  win32file.FindCloseChangeNotification (change_handle)
