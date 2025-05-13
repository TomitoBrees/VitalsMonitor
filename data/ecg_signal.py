import wfdb
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Get the ECG voltages from record 100 from MIT-BIH database.
record = wfdb.rdrecord('100', pn_dir='mitdb')

annotation = wfdb.rdann('100', 'atr', pn_dir='mitdb')

# Take the first ECG channel and the sampling frequency
ecg_signal = record.p_signal[:, 0]
fs = record.fs

# Find the heartbeats (peaks in the data) by their sample number
r_peaks = annotation.sample

# Calculate the time difference between each beat
rr_intervals = np.diff(r_peaks) / fs

# Get the bpm
heart_rates = 60 / rr_intervals

# Find the midpoint for each BPM value
times = (r_peaks[1:] + r_peaks[:-1]) / 2 / fs

if heart_rates[0] > 200:
    heart_rates = heart_rates[1:]
    times = times[1:]

# Total time of the record in seconds
duration = record.p_signal.shape[0] / fs
uniform_times = np.arange(0, int(duration))

# Use interpolation to find the number of beats for each second
bpm_interpolator = interp1d(times, heart_rates, kind='linear', fill_value='extrapolate')
bpm_per_second = bpm_interpolator(uniform_times)

print(bpm_per_second)
