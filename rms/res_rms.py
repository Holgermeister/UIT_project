import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
from pathlib import Path
# flask05 = "05L_rms_Lsensor_big.csv"
# flask15 = "15L_rms_Lsensor_big.csv"
# falsk2 = "2L_rms_Lsensor_big.csv"



def analyze_folder(mappe):

    flask05 = Path(mappe,"05L_rms_big.csv")
    flask15 = Path(mappe, "15L_rms_big.csv")
    falsk2 = Path(mappe,"2L_rms_big.csv")


    df05 = pd.read_csv(flask05)
    df15 = pd.read_csv(flask15) if flask15.exists() else None
    df2 = pd.read_csv(falsk2) if falsk2.exists() else None

    lst_df = [df05, df15, df2]

    for df in lst_df:
        # remove first 10 data points
        if df is None:
            continue
        df.drop(index=range(50), inplace=True)    
    
    plt.figure(figsize=(12, 6))
    for df in lst_df:
        
        if df is None:
            continue

        mean_val = df['rms'].mean()
        std_val = df['rms'].std()
        if df.equals(df05):
            label_name = f"flask 0.5L"
        elif df.equals(df15):
            label_name = f"flask 1.5L"
        elif df.equals(df2):
            label_name = f"flask 2L"
        
        p = plt.plot(df['time_ms'] / 1_000_00, df['rms'], label=f"{label_name} (Mean: {mean_val:.2f}, Std: {std_val:.2f}, min: {df['rms'].min():.2f}, max: {df['rms'].max():.2f})")
        plt.axhline(y=mean_val, color=p[0].get_color(), linestyle='--', alpha=0.7)
        plt.fill_between(df['time_ms'] / 1_000_00, mean_val - std_val, mean_val + std_val, color=p[0].get_color(), alpha=0.2)
    plt.title(mappe)
    plt.ylabel('RMS Value')
    plt.xlabel('Time sec')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        print("give folder path")
    else:
        for folder in args:
            analyze_folder(folder)

# df['rms_smooth'] = df['rms'].rolling(window=10).mean()

# rms = df['rms']

# mean = rms.mean()
# std = rms.std()
# maxv = rms.max()
# minv = rms.min()

# peak_ratio = maxv / (mean + 1e-6)
# total_energy = np.trapz(rms)

# stability = mean / (std + 1e-6)

# print("Mean RMS:", mean)
# print("Smoothed mean:", df['rms_smooth'].mean())
# print("Std RMS:", std)
# print("Max RMS:", maxv)
# print("Peak ratio:", peak_ratio)
# print("Total energy:", total_energy)
# print("Stability:", stability)

# plt.figure(figsize=(12, 6))
# plt.plot(df['time_ms'] / 1000, df['rms'], label='RMS')
# plt.ylabel('raw Value')
# plt.xlabel('Time sec')
# plt.show()

