import numpy
import scipy
import matplotlib.pyplot as plt
from scipy import signal
from scipy import io
from scipy.io import wavfile
from scipy import fftpack
fc = 1000
sensor_dist = 200
filename = 'C:/Users/C15Trevor.Moore/Music/samples/buzz2.wav'
filtcoeffs = 'C:/Users/C15Trevor.Moore/Documents/MATLAB/capstone1.mat'
filtnum = scipy.io.loadmat(filtcoeffs)['Num']
filtden = scipy.io.loadmat(filtcoeffs)['Den']
fs, data = scipy.io.wavfile.read(filename)
data = data[0:50000,0]
a1 = numpy.concatenate((numpy.zeros((50)),data,numpy.zeros((50))))
a2 = numpy.concatenate((numpy.zeros((40)),data,numpy.zeros((60))))
b1 = numpy.concatenate((numpy.zeros((50)),data,numpy.zeros((50))))
b2 = numpy.concatenate((numpy.zeros((40)),data,numpy.zeros((60))))
filtnum =filtnum.transpose()
filtden = filtden.transpose()

datafa1 = scipy.signal.lfilter(filtnum[:,0], filtden[:,0], a1)
datafa2 = scipy.signal.lfilter(filtnum[:,0], filtden[:,0], a2)
datafb1 = scipy.signal.lfilter(filtnum[:,0], filtden[:,0], b1)
datafb2 = scipy.signal.lfilter(filtnum[:,0], filtden[:,0], b2)

Data0 = scipy.absolute(scipy.fftpack.fft(data))

Datafa1 = scipy.absolute(scipy.fftpack.fft(datafa1))
Datafa2 = scipy.absolute(scipy.fftpack.fft(datafa2))
Datafb1 = scipy.absolute(scipy.fftpack.fft(datafb1))
Datafb2 = scipy.absolute(scipy.fftpack.fft(datafb2))
#t = scipy.linspace(0,len(data)/fs, len(data))
#f = scipy.linspace(0,fs, len(data))

#z, axarr = plt.subplots(2, sharex=True)
#axarr[0].plot(f[0:len(Data0)/100],Data0[0:len(Data0)/100])
#axarr[1].plot(f[0:len(Dataf0)/100],Dataf0[0:len(Dataf0)/100])

r1 = numpy.correlate(datafa1, datafa2, "full")
r1 = r1/max(r1)
lag1 = numpy.argmax(r1)-int(len(r1)/2)
number1 = 2*float(lag1)*fc/fs;
rad1 = scipy.arccos(number1);
theta1 = rad1*180/numpy.pi;

r2 = numpy.correlate(datafb1, datafb2, "full")
r2 = r2/max(r2)
lag2 = numpy.argmax(r2)-int(len(r2)/2)
number2 = 2*float(lag2)*fc/fs;
rad2 = scipy.arccos(number2);
theta2 = 180-rad2*180/numpy.pi;

theta3 = theta2-theta1;
rad3 = rad2-rad1;
L1 = sensor_dist*numpy.sin(rad1)/numpy.sin(rad3);
L2 = sensor_dist*numpy.sin(rad2)/numpy.sin(rad3);
x = sensor_dist*numpy.cos(rad1);
y = sensor_dist*numpy.sin(rad1);

m = numpy.array([[0,0],[200,0],[x,y],[0,0]]);
m[3,:] = m[0,:];

plt.plot(m[:,0],m[:,1])
plt.title('TDOA Triangulation')
plt.xlabel('x(ft)')
plt.ylabel('y(ft)')