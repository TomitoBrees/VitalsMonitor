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

def simulate_data():
    heart_rates, respiration, spo2 = get_bidmc_csv_data(DATA_SOURCE)

    def update_monitor(i):
        if i > len(heart_rates):
            return
        monitor_ui.update_heart_rate(heart_rates[i])
        monitor_ui.update_spo2(spo2[i])
        monitor_ui.update_respiration(respiration[i])
        monitor_ui.update_blood_pressure(random.randint(119, 121), random.randint(79, 81))

        root.after(1000, lambda: update_monitor(i + 1))

    update_monitor(0)


root = tk.Tk()
monitor_ui = MonitorUI(root)

simulate_data()
play_beep()
root.mainloop()