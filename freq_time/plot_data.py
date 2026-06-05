
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import os

def rolling_dominant_frequency(time, signal, window_size=256, step_size=10):
    """
    Compute dominant frequency in a rolling window.

    Parameters
    ----------
    time : array-like
        Timestamps.
    signal : array-like
        Signal values.
    window_size : int
        Number of samples per FFT window.
    step_size : int
        Number of samples to advance between windows.

    Returns
    -------
    freq_times : np.ndarray
        Center time of each window.
    dominant_freqs : np.ndarray
        Dominant frequency (Hz) for each window.
    """

    # Estimate sampling rate
    dt = np.median(np.diff(time))
    # print(f"Estimated sampling interval: {dt:.6f} s")
    fs = 1.0 / dt

    freq_times = []
    dominant_freqs = []

    for start in range(0, len(signal) - window_size, step_size):
        end = start + window_size

        segment = signal[start:end]

        # Remove DC component
        segment = segment - np.mean(segment)
        segment = segment * np.hanning(len(segment))
        # FFT
        fft_vals = np.fft.rfft(segment)
        freqs = np.fft.rfftfreq(window_size, d=1/fs)

        # Ignore 0 Hz
        magnitudes = np.abs(fft_vals)
        magnitudes[0] = 0

        dominant_idx = np.argmax(magnitudes)

        dominant_freqs.append(freqs[dominant_idx])
        freq_times.append(time[start + window_size // 2])

    return np.array(freq_times), np.array(dominant_freqs)


def load_and_compute(filename, window_size=128, step_size=16):
    df = pd.read_csv(filename)

    signal = df["raw_value"].values
    time = df["pc_timestamp"].values

    #If timestamps are in milliseconds, uncomment:
    time = time / 1_000_000

    return rolling_dominant_frequency(
        time,
        signal,
        window_size=window_size,
        step_size=step_size,
    )

folder = Path("base_line_acc_mesaurements")
file3 = "mpu6050_raw_05L_v2.csv"
file1 = Path(folder,"mpu6050_raw_05L.csv" )
file2 = Path(folder, "mpu6050_raw_15L.csv")
# file3 = Path(folder, "mpu6050_raw_2L.csv")
# file4 = Path(folder, "mpu6050_raw_15L.csv")
# file3 = Path(folder, "mpu6050_raw_15L_squ.csv")

t1, f1 = load_and_compute(file1)
t2, f2 = load_and_compute(file2)
t3, f3 = load_and_compute(file3)
# t4, f4 = load_and_compute(file4)

mean1, std1 = np.mean(f1), np.std(f1)
mean2, std2 = np.mean(f2), np.std(f2)
mean3, std3 = np.mean(f3), np.std(f3)
# mean4, std4 = np.mean(f4), np.std(f4)


plt.figure(figsize=(12, 5))
plt.plot(t1, f1, label=f"{os.path.basename(file1)} | μ={mean1:.2f} Hz, σ={std1:.2f}")
plt.plot(t2, f2, label=f"{os.path.basename(file2)} | μ={mean2:.2f} Hz, σ={std2:.2f}")
plt.plot(t3, f3, label=f"{os.path.basename(file3)} | μ={mean3:.2f} Hz, σ={std3:.2f}")
# plt.plot(t4, f4, label=f"{os.path.basename(file4)} | μ={mean4:.2f} Hz, σ={std4:.2f}")

plt.title("Rolling Dominant Frequency")
plt.xlabel("Time")
plt.ylabel("Dominant Frequency (Hz)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()