"""
Fits and plots sine wave to period vs orbital phase. Created for PSC 2017.
"""
import csv, scipy.optimize, glob, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from scipy.optimize import curve_fit

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

def orbit(x, amp, phase, offset): #sine fucntion to fit to
    return amp*np.sin(2.0*np.pi*x+ phase) + offset

if __name__ == "__main__":
    if not os.path.exists('./plots/'): #makes dir to put plots and fits
        os.makedirs('./plots/')
    print('\033[33mRed Warning: This program will overwite files in ./plots/\033[0m')
    for files in glob.glob('*.csv'):#opens all *.csv in directory
        file = files.split('.')[0]
        
        rd = csv.reader(open(files,'rU'))

        phase=[];period=[]; period_err=[]
        for row in rd:#CSV file should be orbital phase | period | period error
            phase.append(float(row[0]))
            period.append(float(row[1]))
            period_err.append(float(row[2]))
            
        phase = np.array(phase)
        period = np.array(period)
        period_err = np.array(period_err)
        
        popt, pcov = curve_fit(orbit, phase, period, sigma=period_err)#fits the sine wave to the points, taking into account errors in period

        out = open('./plots/{0}.txt'.format(file),'w')#writes fits and uncertainties out into a .txt file 
        out.write('A={0}, phi={1}, b={2}\n'.format(popt[0],popt[1],popt[2]))
        out.write('std_dev A={0}, std_dev phi={1}, std_dev b={2}'.format(np.sqrt(np.diag(pcov))[0], np.sqrt(np.diag(pcov))[1],np.sqrt(np.diag(pcov))[2]))
        out.close()
        
        phase_dense = np.linspace(0, 1, num=1000)
        plt.plot(phase, period,'ro', label='Observed')
        plt.plot(phase_dense, orbit(phase_dense, *popt),label='Fit w/$A={0:.2E},\phi={1:.2f}, b={2:.2f}$'.format(popt[0],popt[1],popt[2]))
        plt.title(r'{0} Bary. $P$ fitted w/ $A\sin(2\pi \theta+\phi)+b$'.format(file))
        plt.errorbar(phase, period,  yerr=period_err, linestyle='None')
        plt.xlabel(r'Orbital Phase $(\theta)$')
        plt.margins(0.02,0.02)
        plt.ylabel('Pulse Period (ms)')
        plt.legend(loc='best')
        plt.savefig("./plots/{0}.pdf".format(file))
        plt.show()
