import csv, scipy.optimize
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from scipy.optimize import curve_fit

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

def orbit(x, amp, phase, offset):
    return amp*np.sin(6.283*x+ phase) + offset

if __name__ == "__main__":
    file=csv.reader(open('J1022+1001.csv','r'))
    x=[];y=[]
    for row in file:
        x.append(float(row[0]))
        y.append(float(row[1]))

    x0 = [.5,0,0]
    x = np.array(x)
    y = np.array(y)
    popt, pcov = curve_fit(orbit, x, y)

    xplot = np.linspace(0, 1, num=1000)
    plt.plot(x, y,'ro', label='Observed')
    plt.plot(xplot, orbit(xplot, *popt),label='Fit w/$A={0:.2E},\phi={1:.2f}, b={2:.2f}$'.format(popt[0],popt[1],popt[2]))
    plt.title('J1022+1001 Bary. $P$ fitted w/ $A\sin(2\pi x+\phi)+b$')
    plt.xlabel('Pulse Phase')
    plt.margins(0.02,0.02)
    plt.ylabel('Pulse Period (ms)')
    plt.legend(loc='best')
    plt.savefig("J1022+1001.pdf")
    plt.show()
