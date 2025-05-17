import tkinter as tk

from data.bidmc import get_bidmc_csv_data
from monitor_ui import MonitorUI
import random

import neurokit2 as nk

import pygame
import threading

DATA_SOURCE = 3

pygame.mixer.init()
beep_sound = pygame.mixer.Sound("assets/beep.wav")

def play_beep():
    threading.Thread(target=beep_sound.play, daemon=True).start()
    root.after(3000, play_beep)


ecg_signal = nk.ecg_simulate(duration=10, sampling_rate=500)
callback_id = None

def simulate_data():
    heart_rates, respiration, spo2 = get_bidmc_csv_data(DATA_SOURCE)

    def update_monitor(i):
        global callback_id
        if i > len(heart_rates):
            return
        monitor_ui.update_heart_rate(heart_rates[i])
        monitor_ui.update_spo2(spo2[i])
        monitor_ui.update_respiration(respiration[i])
        monitor_ui.update_blood_pressure(random.randint(119, 121), random.randint(79, 81))

        callback_id = root.after(1000, lambda: update_monitor(i + 1))

    update_monitor(0)

def stop_pannel():
    global callback_id
    if callback_id is not None:
        root.after_cancel(callback_id)
        root.after_cancel(monitor_ui.waveform_callback)
        monitor_ui.waveform_callback = None
        callback_id = None

def start_pannel():
    global callback_id
    if callback_id is None:
        simulate_data()
        monitor_ui.update_waveform()

root = tk.Tk()
monitor_ui = MonitorUI(root)

monitor_ui.stop_button.configure(command=stop_pannel)
monitor_ui.start_button.configure(command=start_pannel)

simulate_data()
play_beep()
root.mainloop()