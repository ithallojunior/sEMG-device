# -*- coding: utf-8 -*-
"""
Real time plot
It must be set with the settings.py file
Author: Ithallo Junior Alves Guimaraes
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lfilter
import time
import os

import settings
import modules


def plotter():
    """Plots the acquired signal along the time axis."""

    os.system("clear")

    p = modules.serial_port()

    print("Starting plotter...")

    p.flush()

    time.sleep(0.5)

    plt.ion()
    plt.figure(figsize=(18, 9))

    grid_spacing = np.arange(
        0,
        settings.time_window_to_show,
        settings.time_window_to_show/settings.xticks
    )
    samples = int(
        settings.sampling_frequency * settings.time_window
    )
    buffer_length = int(
        settings.sampling_frequency * settings.time_window_to_show
    )

    t = np.arange(
        0., settings.time_window_to_show,
        1./settings.sampling_frequency
    )

    y = np.zeros((samples, settings.number_of_channels))
    plot_buffer = np.zeros((buffer_length, settings.number_of_channels))

    # filter, getting the coefficients one time for all, as it is kinda slow
    if(settings.use_filter):
        b, a = modules.get_filter_constants()

    while(1):
        try:
            plt.clf()
            plt.ylabel("Volts(v)")
            plt.xlabel("Time(s)")
            plt.xlim(0, settings.time_window_to_show)

            if settings.remove_mean:
                plt.ylim(-0.6, 0.6)
            else:
                plt.ylim(0., settings.voltage_range)

            i = 0
            while i < samples:

                for j in range(settings.number_of_channels):
                    v1 = p.read()
                    v2 = p.read()
                    y[i, j] = modules.convert_input(v1, v2)
                    i += 1

            # circular buffer, simple now
            plot_buffer = plot_buffer[samples:, :]
            plot_buffer = np.vstack((plot_buffer, y[:buffer_length, :]))

            for i in range(settings.number_of_channels):

                # removing DC
                if (settings.remove_mean):
                    yn = plot_buffer[:, i] - plot_buffer[:, i].mean()
                else:
                    yn = plot_buffer[:, i]
                # checking if there is signal
                signal_flag = ''
                if not np.any(yn):
                    signal_flag = '- no signal'

                # filtering signal
                if (settings.use_filter):
                    yn = lfilter(b, a, yn)

                plt.plot(
                    t, yn, c=settings.colors[i],
                    label="Channel %s %s" % (i+1, signal_flag)
                )

                plt.xticks(grid_spacing)
                plt.grid(color='k', linestyle='-', linewidth=.1)
                plt.legend(loc="upper right")
                plt.title("Signal(s) || Fs: %.3f || Filter %s || Range: %smV" % (
                          settings.sampling_frequency,
                          'ON' if settings.use_filter else 'OFF',
                          round(yn.max() - yn.min(), 3)*1000.)
                          )

                plt.pause(1.0/60.0)

        except KeyboardInterrupt:
            plt.close()
            break

    p.close()


if (__name__ == "__main__"):
    plotter()
