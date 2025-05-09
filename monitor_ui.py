import tkinter as tk
import tkinter.font as tkFont

from enum import Enum

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

        self.content = tk.Frame(root, bg="black")
        self.content.pack(padx=20, pady=20)

        self._build_layout()

    def _build_layout(self):
        self._add_vitals_row(self.content, Vital.ECG, 0)
        self._add_vitals_row(self.content, Vital.RESPTEMP, 1)
        self._add_vitals_row(self.content, Vital.SPO2, 2)
        self._add_vitals_row(self.content, Vital.NIBP, 3)

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

    def update_temperature(self, value):
        self.respiration_rate.set(f"{value}")

    def update_blood_pressure(self, systolic, diastolic):
        self.blood_pressure.set(f"{systolic}/{diastolic}")

