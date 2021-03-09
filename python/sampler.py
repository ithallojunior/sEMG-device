"""
This code works as a sampler for the EMG system (Arduino).
It must be configured via the settings.py file.
After sampling, it calls the plotter, if the argument
'--plot' was passed. Other possible arguments may be passed,
as detailed in the 'plot.py file'.

Author: Ithallo Junior Alves Guimaraes

"""

import os
import datetime
import time
from sys import argv

import serial
import numpy as np
from scipy.signal import lfilter

import modules
import settings
from plot import plot


# the run of the code
def sampler():
    """Samples the sEMG signal as declared on the settings file."""

    # filter, getting the coefficients one time for all, as it is kinda slow
    if (settings.use_filter):
        b, a = modules.get_filter_constants()

    os.system("clear")
    raw_input("Press enter to start...")

    p = serial.Serial(port=settings.device, baudrate=settings.baud_rate,
                      bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                      timeout=settings.timeout)
    # timeout to be blocking

    time.sleep(0.1)  # settle time
    p.flush()  # deletes buffers

    # control variables and max
    total_samples = int(settings.sampling_frequency * settings.total_time)
    delta_time = 1./settings.sampling_frequency
    broke_out = False

    # allocating
    X = np.zeros((total_samples, 2))

    # sampling
    for i in xrange(total_samples):
        try:
            # reading  value
            v1 = p.read()
            v2 = p.read()

            # converting to
            if (v1 == '') or (v2 == ''):
                print("\nNo data, check your circuits and run again.\n")
                broke_out = True
                break
            else:
                X[i, 0] = i * delta_time
                X[i, 1] = modules.convert_input(v1, v2)

            # loading screen
            percent = 100. * float(i)/total_samples
            print("Running --- %.3f%%" % percent)

        except KeyboardInterrupt:
            print("\nInterrupted\n")
            time.sleep(.5)
            broke_out = True
            break

    if (not broke_out):
        # saving to file
        filepath = settings.default_path + "data_%s.txt" % (
            str(datetime.datetime.now())[:-7]
        ).replace(" ", "_").replace(":", "-")

        # filtering signal
        if (settings.use_filter):
            X[:, 1] = lfilter(b, a, X[:, 1])

        np.savetxt(filepath, X, fmt=settings.format)
        print ("file saved to %s " % filepath)

    else:
        filepath = None

    # closing port
    p.flush()
    p.close

    return filepath


if (__name__ == "__main__"):

    filepath = sampler()
    if filepath is not None:
        plot(filepath, *argv)
