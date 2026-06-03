import serial
import csv
import time
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def analyze(file_path):
    df = pd.read_csv(file_path)
    df['rms_smooth'] = df['rms'].rolling(window=10).mean()
    
    rms = df['rms']

    mean = rms.mean()
    std = rms.std()
    maxv = rms.max()
    minv = rms.min()

    peak_ratio = maxv / (mean + 1e-6)
    total_energy = np.trapz(rms)

    stability = mean / (std + 1e-6)

    print("Mean RMS:", mean)
    print("Smoothed mean:", df['rms_smooth'].mean())
    print("Std RMS:", std)
    print("Max RMS:", maxv)
    print("Peak ratio:", peak_ratio)
    print("Total energy:", total_energy)
    print("Stability:", stability)

    plt.figure(figsize=(12, 6))
    plt.plot(df['time_ms'] / 1000, df['rms'], label='RMS')
    plt.ylabel('raw Value')
    plt.xlabel('Time sec')
    plt.show()
# ===== CONFIG =====
PORT = "COM8"
BAUD = 115200
OUTPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "rms_data.csv"

NUM_SAMPLES = 300  # Number of samples to read (optional, can be removed for infinite reading)

# ===== SERIAL =====
ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

print("Logging RMS data... Ctrl+C to stop.")

# ===== CSV =====
with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["time_ms", "rms"])

    try:
        #for i in range(100):  # Arbitrary large number to keep reading until interrupted
        for _ in range(NUM_SAMPLES):  # Arbitrary large number to keep reading until interrupted
            line = ser.readline().decode(errors="ignore").strip()
            
            if not line:
                continue

            try:
                t, rms = line.split(",")

                writer.writerow([int(t), float(rms)])

            except ValueError:
                print(f"Skipping malformed line: {line}")  # Debug info for malformed lines
                # skips broken lines
                continue

    except KeyboardInterrupt:
        print("\nStopped.")

    finally:
        ser.close()

analyze(OUTPUT_FILE)

