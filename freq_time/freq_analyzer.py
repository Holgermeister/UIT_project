import pandas as pd 
import numpy as np 
from scipy.signal import find_peaks 
from scipy.fft import rfft, rfftfreq 
import sys

def dominant_frequency_over_time(times, values, window_seconds=0.7, step_seconds=0.02, min_freq=5):
    values = values - np.mean(values)

    results = []

    start = times[0]
    end = times[-1]

    current = start

    while current + window_seconds <= end:
        window_start = current
        window_end = current + window_seconds

        mask = (times >= window_start) & (times < window_end)

        t_win = times[mask]
        v_win = values[mask]

        if len(v_win) < 4:
            current += step_seconds
            continue

        dt = np.mean(np.diff(t_win))

        freqs = rfftfreq(len(v_win), dt)
        fft_vals = np.abs(rfft(v_win))

        fft_vals[0] = 0
        fft_vals[freqs < min_freq] = 0

        dominant_freq = freqs[np.argmax(fft_vals)]
        rms = np.sqrt(np.mean(v_win**2))
        variation = np.std(v_win)

        results.append({
            "time": window_start + window_seconds / 2,
            "dominant_freq": dominant_freq,
            "rms": rms,
            "std": variation,
            "max": np.max(v_win),
            "min": np.min(v_win),
        })

        current += step_seconds

    return pd.DataFrame(results)


def analyze_piezo_data(file_path):
    try:
        df = pd.read_csv(file_path)

        for run_id, group in df.groupby("run"):
            group = group.sort_values("time")

            times = group["time"].values
            raw_values = group["value"].values
            values = raw_values - np.mean(raw_values)

            duration = times[-1] - times[0]
            dt = np.mean(np.diff(times))
            sampling_rate = 1 / dt

            mean_value = raw_values.mean()
            std_value = raw_values.std()
            var_value = raw_values.var()
            min_value = raw_values.min()
            max_value = raw_values.max()
            range_value = max_value - min_value

            rms = np.sqrt(np.mean(values**2))
            mean_abs = np.mean(np.abs(values))
            energy = np.sum(values**2)

            freqs = rfftfreq(len(values), dt)
            fft_vals = np.abs(rfft(values))

            fft_vals[0] = 0
            fft_vals[freqs < 5] = 0

            dominant_freq = freqs[np.argmax(fft_vals)]

            peaks, _ = find_peaks(
                values,
                prominence=np.std(values),
                distance=5
            )

            num_peaks = len(peaks)
            peak_rate = num_peaks / duration if duration > 0 else 0

            if num_peaks > 0:
                max_peak = np.max(values[peaks])
                mean_peak = np.mean(values[peaks])
            else:
                max_peak = 0
                mean_peak = 0

            print(f"--- Analysis for Run: {run_id} ---")
            # print(f"\tMean value: {mean_value:.4f}")
            # print(f"\tStd / variation: {std_value:.4f}")
            # print(f"\tVariance: {var_value:.4f}")
            # print(f"\tMean absolute signal: {mean_abs:.4f}")
            print(f"\tDominant frequency: {dominant_freq:.2f} Hz")
            # print(f"\tMean peak height: {mean_peak:.4f}")
            # print(f"\tMax peak height: {max_peak:.4f}")

            #freq_over_time = dominant_frequency_over_time(times, raw_values)

            # print("\t--- Frequency over time preview ---")
            # print(freq_over_time.head())

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

analyze_piezo_data("ispind_2.csv")