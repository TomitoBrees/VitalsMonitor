import tkinter as tk
import tkinter.font as tkFont

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import neurokit2 as nk

from enum import Enum


duration = 30  # seconds
sampling_rate = 500  # Hz
ecg_data = nk.ecg_simulate(duration=duration, heart_rate=75, noise=0.01, sampling_rate=sampling_rate)
resp_data = nk.rsp_simulate(duration=duration, respiratory_rate=18, noise=0.01, sampling_rate=sampling_rate)


# --- ENUM --- #
class Vital(Enum):
    ECG = 1
    RESPTEMP = 2
    SPO2 = 3
    NIBP = 4

# --- CLASS --- #
class MonitorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vitals Monitor")
        self.root.configure(background="black")

        self.ecg_font = tkFont.Font(family="Consolas", size=72, weight="bold")
        self.numbers_font = tkFont.Font(family="Consolas", size=36, weight="bold")
        self.text_font = tkFont.Font(family="Consolas", size=18, weight="bold")

        self.heart_rate = tk.StringVar()
        self.blood_pressure = tk.StringVar()
        self.o2_sat = tk.StringVar()
        self.respiration_rate = tk.StringVar()

        # self.content = tk.Frame(root, bg="black")
        # self.content.pack(padx=20, pady=20)

        # Main layout
        self.main_frame = tk.Frame(root, bg="black")
        self.main_frame.pack(fill="both", expand=True)

        # Left: vitals panel
        self.left_frame = tk.Frame(self.main_frame, bg="black")
        self.left_frame.pack(side="left", padx=20, pady=20)

        # Right: waveform panel
        self.right_frame = tk.Frame(self.main_frame, bg="black")
        self.right_frame.pack(side="right", padx=10)

        self._build_vitals_ui()
        self._build_waveform_ui();

    def _build_vitals_ui(self):
        self._add_vitals_row(self.right_frame, Vital.ECG, 0)
        self._add_vitals_row(self.right_frame, Vital.RESPTEMP, 1)
        self._add_vitals_row(self.right_frame, Vital.SPO2, 2)
        self._add_vitals_row(self.right_frame, Vital.NIBP, 3)


    def _build_waveform_ui(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 3), dpi=100)
        self.fig.tight_layout(pad=2)

        self.ax1.set_ylim(-1.5, 1.5)
        self.ax1.set_facecolor("black")

        self.ax2.set_ylim(-1.5, 1.5)
        self.ax2.set_facecolor("black")

        self.line1, = self.ax1.plot(ecg_data[:1000], color='red')
        self.line2, = self.ax2.plot(resp_data[:1000], color='blue')

        self.fig.patch.set_facecolor("black")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.left_frame)
        self.canvas.get_tk_widget().pack()

        self.wave_index = 0
        self.window_size = 1000
        self._update_waveform()


    def _add_vitals_row(self, parent, vital_type, row):
        if vital_type == Vital.ECG or vital_type == Vital.NIBP:
            frame = tk.Frame(parent, bg="black", highlightbackground="blue",
                             highlightthickness=1, bd=0, width=200, height=100)
            frame.grid(row=row, column=0, sticky="ew")
            frame.pack_propagate(False)

            container = tk.Frame(frame, bg="black")
            container.pack(expand=True, fill="both", padx=10)

            if vital_type == Vital.ECG:
                label = tk.Label(container, text="ECG", font=self.text_font, fg="lime", bg="black")
                label.pack(side="left", anchor="nw")

                value = tk.Label(container, textvariable=self.heart_rate, font=self.ecg_font, fg="lime", bg="black")
                value.pack(side="bottom", anchor="sw")

            elif vital_type == Vital.NIBP:
                label = tk.Label(container, text="NIBP", font=self.text_font, fg="white", bg="black")
                label.pack(side="top", anchor="nw")

                value = tk.Label(container, textvariable=self.blood_pressure, font=self.numbers_font, fg="white", bg="black")
                value.pack(side="bottom", anchor="center")

        else:

            frame = tk.Frame(parent, bg="black", highlightbackground="blue",
                             highlightthickness=1, bd=0, width=200, height=80)
            frame.grid(row=row, column=0, sticky="ew")
            frame.pack_propagate(False)

            container = tk.Frame(frame, bg="black")
            container.pack(expand=True, fill="both", padx=10)

            if vital_type == Vital.RESPTEMP:
                label = tk.Label(container, text="RESP", font=self.text_font, fg="yellow", bg="black")
                label.pack(side="left", anchor="w")

                value = tk.Label(container, textvariable=self.respiration_rate, font=self.numbers_font, fg="yellow", bg="black")
                value.pack(side="right", anchor="e")

            elif vital_type == Vital.SPO2:
                label = tk.Label(container, text="SpO₂", font=self.text_font, fg="cyan", bg="black")
                label.pack(side="left", anchor="w")

                value = tk.Label(container, textvariable=self.o2_sat, font=self.numbers_font, fg="cyan", bg="black")
                value.pack(side="right", anchor="e")



    def update_heart_rate(self, value):
        self.heart_rate.set(f"{value}")

    def update_spo2(self, value):
        self.o2_sat.set(f"{value}")

    def update_respiration(self, value):
        self.respiration_rate.set(f"{value}")

    def update_blood_pressure(self, systolic, diastolic):
        self.blood_pressure.set(f"{systolic}/{diastolic}")

    def _update_waveform(self):
        if self.wave_index + self.window_size < len(ecg_data):
            self.line1.set_ydata(ecg_data[self.wave_index:self.wave_index + self.window_size])
            self.line2.set_ydata(resp_data[self.wave_index:self.wave_index + self.window_size])
            self.canvas.draw()
            self.wave_index += 5
        self.root.after(20, self._update_waveform)

