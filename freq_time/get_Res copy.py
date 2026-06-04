import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from scipy.fft import rfft, rfftfreq

import sys

window_size = 500
step_size = 500

def analyze_piezo_data(file_path):
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)


        for run_id, group in df.groupby('run'):
            group = group.reset_index(drop=True)

            for start in range(0, len(group) - window_size + 1, step_size):
                print(f"number of samples: {len(group)}")
                window = group.iloc[start:start + window_size]
        
                # Calculate mean and max
                mean_value = window['value'].mean()
                max_value = window['value'].max()

                # ===== FFT =====
                times = window['time'].values
                values = window['value'].values

                values = values - np.mean(values)

                dt = np.mean(np.diff(times))


                freqs = rfftfreq(len(values), dt)
                fft_vals = np.abs(rfft(values))

                fft_vals[0] = 0
                fft_vals[freqs < 5] =0
                dominant_freq = freqs[np.argmax(fft_vals)]
                
                rms = np.sqrt(np.mean(values**2))


                # ===== OUTPUT =====
                # print(f"--- Analysis for Run: {run_id} ---")
                # print(f"\tNumber of samples: {len(group):_}")
                # print(f"\tMean value: {mean_value:.4f}")
                # print(f"\tLargest value: {max_value:.4f}")
                # print("\t--- fft freq(hz) ---")
                print("\tDominant frequency:", dominant_freq, "Hz")
                #print("\tRMS:", rms)

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

if __name__ == '__main__':
    file = sys.argv[1] if len(sys.argv) > 1 else None
    analyze_piezo_data(file)
 
