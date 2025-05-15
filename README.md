
# Vitals Monitor Application

This is a Python application that simulates and displays vital signs data in a real-time dashboard interface. It uses simulated physiological signals as well as real patient data from the BIDMC dataset.

---

## Features

- Real-time visualization of ECG, Respiration, and SpO2 waveforms using Matplotlib embedded in a Tkinter GUI.
- Displays numerical values for heart rate, respiration rate, SpO2, and non-invasive blood pressure (NIBP).
- Uses NeuroKit2 to simulate physiological signals (ECG, respiration, SpO2).
- Fetches real patient vital signs data from the BIDMC PhysioNet dataset.

---

## Requirements

- Python 3.8+
- Pandas
- Matplotlib
- Tkinter (usually included with Python)
- NeuroKit2
- Pygame

Install the required packages via pip:

```bash
pip install pandas matplotlib neurokit2 pygame
```

---

## Usage

Run the main Python script to launch the GUI application:

```bash
python main.py
```

You can change the BIDMC data source by changing this line:
```
DATA_SOURCE = 3
```
The source file number can range from 1 to 53.

The application will:

- Fetch and load BIDMC CSV data for heart rate, respiration, and SpO2.
- Simulate ECG, respiration, and SpO2 signals.
- Display real-time waveform plots and numeric values.
- Play beep sounds every second.

---

## Project Structure

- `main.py` - Main application script to start the GUI and run simulation.
- `monitor_ui.py` - Contains the `MonitorUI` class for the GUI components.
- `data/bidmc.py` - Function to download and process BIDMC CSV data.
- `assets/beep.wav` - Beep sound file used for alert sound.

---

## Data Source

The BIDMC dataset is sourced from PhysioNet:

https://www.physionet.org/content/bidmc/

---

## License

This project is open-source and free to use.

---

## Author

Created by Tom L'HOTELLIER

