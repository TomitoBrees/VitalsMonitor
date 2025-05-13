import neurokit2 as nk
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

duration = 30  # seconds
sampling_rate = 500  # Hz
ecg_data = nk.ecg_simulate(duration=duration, heart_rate=75, noise=0.01, sampling_rate=sampling_rate)
resp_data = nk.rsp_simulate(duration=duration, respiratory_rate=18, noise=0.01, sampling_rate=sampling_rate)

# How many points to display at once
window_size = 1000  # 2 seconds if fs=500
index = 0

# Set up GUI
root = tk.Tk()
root.title("Vitals Monitor Simulator")

# Create matplotlib figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Initial plots
line1, = ax1.plot(ecg_data[:window_size], color='red')
ax1.set_title("ECG")
ax1.set_ylim(-1.5, 1.5)

line2, = ax2.plot(resp_data[:window_size], color='blue')
ax2.set_title("Respiration")
ax2.set_ylim(-1.5, 1.5)

plt.tight_layout()


def update_plot():
    global index
    if index + window_size < len(ecg_data):
        # Update ECG
        line1.set_ydata(ecg_data[index:index + window_size])
        # Update Respiration
        line2.set_ydata(resp_data[index:index + window_size])

        # Redraw canvas
        canvas.draw()
        index += 5  # Move window forward (5 points = 10ms if fs=500)

    root.after(20, update_plot)  # Update every 20 ms


update_plot()
root.mainloop()