import serial
import numpy as np
import time

PORT = "COM8"          # Windows example: "COM3"
# PORT = "/dev/ttyACM0"  # Linux example
# PORT = "/dev/cu.usbmodem1101"  # macOS example

BAUD_RATE = 115200
SAMPLES = 512

ser = serial.Serial(PORT, BAUD_RATE, timeout=2)
time.sleep(2)

print("Reading from Arduino...")
print("Press Ctrl+C to stop.")

def read_sample():
    while True:
        line = ser.readline().decode("utf-8", errors="ignore").strip()

        if not line:
            continue

        if line.startswith("START") or line.startswith("ERROR"):
            print(line)
            continue

        parts = line.split(",")

        if len(parts) != 2:
            continue

        try:
            t_us = int(parts[0])
            accel_z = float(parts[1])
            return t_us, accel_z
        except ValueError:
            continue

try:
    while True:
        times = []
        values = []

        while len(values) < SAMPLES:
            t_us, accel_z = read_sample()
            times.append(t_us)
            values.append(accel_z)

        times = np.array(times, dtype=np.float64)
        values = np.array(values, dtype=np.float64)

        # Convert time from microseconds to seconds
        times_s = times / 1_000_000.0

        # Estimate actual sampling frequency from Arduino timestamps
        duration = times_s[-1] - times_s[0]
        sampling_frequency = (SAMPLES - 1) / duration

        # Remove DC offset / gravity component
        values = values - np.mean(values)

        # Apply Hann window
        window = np.hanning(SAMPLES)
        values_windowed = values * window

        # FFT
        fft_values = np.fft.rfft(values_windowed)
        magnitudes = np.abs(fft_values)

        freqs = np.fft.rfftfreq(SAMPLES, d=1.0 / sampling_frequency)

        # Ignore 0 Hz bin
        magnitudes[0] = 0

        peak_index = np.argmax(magnitudes)
        dominant_frequency = freqs[peak_index]
        peak_magnitude = magnitudes[peak_index]

        print(
            f"Dominant frequency: {dominant_frequency:8.2f} Hz | "
            f"Sample rate: {sampling_frequency:7.2f} Hz | "
            f"Magnitude: {peak_magnitude:.2f}"
        )

except KeyboardInterrupt:
    print("\nStopped.")

finally:
    ser.close()
