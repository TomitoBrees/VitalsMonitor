import tkinter as tk
import tkinter.font as tkFont

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import neurokit2 as nk

from enum import Enum


duration = 30
sampling_rate = 500
ecg_data = nk.ecg_simulate(duration=duration, heart_rate=75, noise=0.01, sampling_rate=sampling_rate, random_state=42)
resp_data = nk.rsp_simulate(duration=duration, sampling_rate=sampling_rate, method="sinusoidal", respiratory_rate=100)
spo2_data = nk.ppg_simulate(duration=duration, sampling_rate=sampling_rate, heart_rate=75, random_state=42)


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

        # Main layout
        self.main_frame = tk.Frame(root, bg="black")
        self.main_frame.pack(fill="both", expand=True)

        # Left: vitals panel
        self.left_frame = tk.Frame(self.main_frame, bg="black", height=500, width=700)
        self.left_frame.pack(side="left", fill="x", anchor="n", pady=15)
        self.left_frame.pack_propagate(False)

        # Right: waveform panel
        self.right_frame = tk.Frame(self.main_frame, bg="black")
        self.right_frame.pack(side="right")

        # Buttons
        self.button_panel = tk.Frame(self.left_frame, height=50, bg="black")
        self.button_panel.pack(side="bottom", pady=(45, 0))

        self.start_button = tk.Button(self.button_panel, text="Start", width=5, height=2)
        self.start_button.pack(side="left", padx=20, pady=10)

        self.stop_button = tk.Button(self.button_panel, text="Stop", width=5, height=2)
        self.stop_button.pack(side="left", padx=20, pady=10)

        self._build_vitals_ui()
        self._build_waveform_ui()

    def _build_vitals_ui(self):
        self._add_vitals_row(self.right_frame, Vital.ECG, 0)
        self._add_vitals_row(self.right_frame, Vital.RESPTEMP, 1)
        self._add_vitals_row(self.right_frame, Vital.SPO2, 2)
        self._add_vitals_row(self.right_frame, Vital.NIBP, 3)


    def _build_waveform_ui(self):
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(7, 5), dpi=100)
        self.fig.tight_layout(pad=0)

        self.ax1.set_ylim(-1.2, 1.2)
        self.ax1.set_facecolor("black")

        self.ax1.set_xticks([])
        self.ax1.set_yticks([])
        self.ax1.set_xticklabels([])
        self.ax1.set_yticklabels([])

        for spine in self.ax1.spines.values():
            spine.set_visible(False)

        self.ax2.set_ylim(-1, 1)
        self.ax2.set_facecolor("black")

        self.ax2.set_xticks([])
        self.ax2.set_yticks([])
        self.ax2.set_xticklabels([])
        self.ax2.set_yticklabels([])

        for spine in self.ax2.spines.values():
            spine.set_visible(False)

        self.ax3.set_ylim(-0.5, 2)
        self.ax3.set_facecolor("black")

        self.ax3.set_xticks([])
        self.ax3.set_yticks([])
        self.ax3.set_xticklabels([])
        self.ax3.set_yticklabels([])

        for spine in self.ax3.spines.values():
            spine.set_visible(False)


        self.line1, = self.ax1.plot(ecg_data[:1000], color='lime')
        self.line2, = self.ax2.plot(resp_data[:1500], color='yellow')
        self.line3, = self.ax3.plot(spo2_data[:1000], color='cyan')

        self.fig.patch.set_facecolor("black")
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0, hspace=0, wspace=0)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.left_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.window_size_ecg = 1000
        self.ax1.set_xlim(0, self.window_size_ecg)

        self.window_size_resp = 1500
        self.ax2.set_xlim(0, self.window_size_resp)

        self.window_size_spo2 = 1000
        self.ax3.set_xlim(0, self.window_size_spo2)

        self.index_ecg = 0
        self.index_resp = 0
        self.index_spo2 = 0

        self.update_waveform()


    def _add_vitals_row(self, parent, vital_type, row):
        if vital_type == Vital.ECG:
            frame = tk.Frame(parent, bg="black", highlightbackground="blue",
                             highlightthickness=1, bd=0, width=200, height=150)
            frame.grid(row=row, column=0, sticky="ew")
            frame.pack_propagate(False)

            container = tk.Frame(frame, bg="black")
            container.pack(expand=True, fill="both", padx=10)

            if vital_type == Vital.ECG:
                label = tk.Label(container, text="ECG", font=self.text_font, fg="lime", bg="black")
                label.pack(side="left", anchor="nw")

                value = tk.Label(container, textvariable=self.heart_rate, font=self.ecg_font, fg="lime", bg="black")
                value.pack(side="bottom", anchor="sw")


        else:

            frame = tk.Frame(parent, bg="black", highlightbackground="blue",
                             highlightthickness=1, bd=0, width=200, height=120)
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

            elif vital_type == Vital.NIBP:
                label = tk.Label(container, text="NIBP", font=self.text_font, fg="white", bg="black")
                label.pack(side="top", anchor="nw")

                value = tk.Label(container, textvariable=self.blood_pressure, font=self.numbers_font, fg="white", bg="black")
                value.pack(side="bottom", anchor="center")



    def update_heart_rate(self, value):
        self.heart_rate.set(f"{value}")

    def update_spo2(self, value):
        self.o2_sat.set(f"{value}")

    def update_respiration(self, value):
        self.respiration_rate.set(f"{value}")

    def update_blood_pressure(self, systolic, diastolic):
        self.blood_pressure.set(f"{systolic}/{diastolic}")

    def update_waveform(self):
        if self.index_ecg + self.window_size_ecg < len(ecg_data):
            self.line1.set_ydata(ecg_data[self.index_ecg:self.index_ecg + self.window_size_ecg])
            self.index_ecg += 5

        if self.index_resp + self.window_size_resp < len(resp_data):
            self.line2.set_ydata(resp_data[self.index_resp:self.index_resp + self.window_size_resp])
            self.index_resp += 5

        if self.index_spo2 + self.window_size_spo2 < len(spo2_data):
            self.line3.set_ydata(spo2_data[self.index_spo2:self.index_spo2 + self.window_size_spo2])
            self.index_spo2 += 5


        self.canvas.draw()
        self.waveform_callback = self.root.after(20, self.update_waveform)

