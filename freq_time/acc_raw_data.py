import serial
import numpy as np
import time
import csv
from datetime import datetime
import sys

PORT = "COM8"          # Change this
BAUD = 921600
SAMPLE_RATE = 1000.0   # Must match Arduino target rate
N = 256                # FFT size, power of 2 is best
READ_FOR_SECONDS = 60      # Total duration to read data
if len(sys.argv) > 1:
    filename = sys.argv[1]
    print(f"Logging raw data to: {filename}")

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

filename = f"mpu6050_raw_{filename}.csv"

print(f"Logging raw data to: {filename}")
print("Listening... Press Ctrl+C to stop.")

csv_file = open(filename, mode="w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["pc_timestamp", "sample_index", "raw_value"])

sample_counter = 0

def read_sample():
    while True:
        line = ser.readline().decode("utf-8", errors="ignore").strip()

        if not line:
            continue

        if line == "START":
            continue

        if line.startswith("ERROR"):
            raise RuntimeError(line)

        try:
            ts_str, val_str = line.split(",")
            timestamp = int(ts_str)
            value = int(val_str)
            return timestamp, value
        
        except ValueError:
            continue

start = time.time()
try:
    while time.time() - start < READ_FOR_SECONDS:
        # samples = []

        # for _ in range(N):
        timestamp, value = read_sample()
            
        csv_writer.writerow([timestamp, sample_counter, value])
        #samples.append(value)
        sample_counter += 1

        csv_file.flush()

        # samples = np.array(samples, dtype=np.float64)

        # # Remove DC offset
        # samples = samples - np.mean(samples)

        # # Apply Hann window
        # window = np.hanning(N)
        # windowed = samples * window

        # # FFT
        # fft_vals = np.fft.rfft(windowed)
        # mags = np.abs(fft_vals)
        # freqs = np.fft.rfftfreq(N, d=1.0 / SAMPLE_RATE)

        # # Ignore DC
        # mags[0] = 0

        # peak_index = np.argmax(mags)
        # dominant_freq = freqs[peak_index]
        # peak_mag = mags[peak_index]

        # print(f"Dominant frequency: {dominant_freq:7.2f} Hz | Magnitude: {peak_mag:.1f}")

except KeyboardInterrupt:
    print("\nStopped.")

finally:
    csv_file.close()
    ser.close()


