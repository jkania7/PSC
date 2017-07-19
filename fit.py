import csv, scipy.optimize, glob, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from scipy.optimize import curve_fit

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

def orbit(x, amp, phase, offset):
    return amp*np.sin(6.283*x+ phase) + offset

if __name__ == "__main__":
    os.chdir('.')
    for files in glob.glob('*.csv'):
        file = files.split('.')[0]
        
        rd = csv.reader(open(files,'rU'))

        phase=[];period=[]; period_err=[]
        for row in rd:
            phase.append(float(row[0]))
            period.append(float(row[1]))
            period_err.append(float(row[2]))
            
        phase = np.array(phase)
        period = np.array(period)
        period_err = np.array(period_err)
        
        popt, pcov = curve_fit(orbit, phase, period)

        xplot = np.linspace(0, 1, num=1000)
        plt.plot(phase, period,'ro', label='Observed')
        plt.plot(xplot, orbit(xplot, *popt),label='Fit w/$A={0:.2E},\phi={1:.2f}, b={2:.2f}$'.format(popt[0],popt[1],popt[2]))
        plt.title('{0} Bary. $P$ fitted w/ $A\sin(2\pi x+\phi)+b$'.format(file))
        plt.xlabel('Orbital Phase')
        plt.margins(0.02,0.02)
        plt.ylabel('Pulse Period (ms)')
        plt.legend(loc='best')
        plt.savefig("{0}.pdf".format(file))
        plt.show()
