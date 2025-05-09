import tkinter as tk
from monitor_ui import MonitorUI
import random

def simulate_data():
    monitor_ui.update_heart_rate(random.randint(60, 100))
    monitor_ui.update_spo2(random.randint(95, 100))
    monitor_ui.update_temperature(random.randint(10, 30))
    monitor_ui.update_blood_pressure(random.randint(110, 130), random.randint(70, 90))

    root.after(3000, simulate_data)

root = tk.Tk()
monitor_ui = MonitorUI(root)

simulate_data()
root.mainloop()