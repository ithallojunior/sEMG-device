# -*- coding: utf-8 -*-
"""
Settings file for the plotters
Author: Ithallo Junior Alves Guimaraes
"""
# serial settings
device = "/dev/cu.wchusbserial1410"  # change accordingly
baud_rate = 115200  # depends on your arduino code
timeout = 5.  # seconds, in order to prevent  the code from holding

# frequency settings
sampling_frequency = 2000.  # Hz
time_window = 500e-3  # second(s),fixed to avoid performance issues on display
time_window_to_show = 4000e-3
frequency_window = 2048  # samples
total_time = 4.  # *60. # seconds, to be used to get the total number of samples
max_expected_frequency = 500.  # Hz
max_expected_frequency_to_show = 2. * max_expected_frequency  # Hz
normalize_spectrum = True  # normalizes to the max


# signal settings
voltage_range = 1.1  # max selected in the attiny85 sampler
offset = 0.  # voltage offset to correct signal
remove_mean = False  # removes mean for the window
always_use_remove_mean_for_spectrum = True  # forces removing mean for spectrum


# data saving settings
format = "%.4f"  # I think 4 values after the point is enough
default_path = 'acquisitions/'  # leave it empty to be on the same folder

# transmitter settings
number_of_channels = 1  # number of channels to be displayed/sampled

# plot settings
colors = ["b", "r", "g", "y"]
xticks = 10

# Filter settings, here a Butterworth will be used.
use_filter = False  # whether to use or not
filter_type = "bandpass"  # lowpass, highpass or bandpass
fc = [2., 500.]  # cutoff frequencies, change depending on the type
order = 4  # order of the filter
