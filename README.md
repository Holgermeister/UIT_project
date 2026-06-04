# UIT_project
Pneumatic printed haptics

# RMS Data Analysis & Visualization (`res_rms.py`)

This script analyzes and visualizes Root Mean Square (RMS) data from multiple CSV files. It automatically reads data from three different flask volumes (0.5L, 1.5L, and 2.0L), removes initial noisy data points, and generates a time-series plot comparing the RMS values, complete with statistical overlays.

## Prerequisites

Ensure you have Python installed along with the required libraries. You can install the dependencies using `pip`:

```bash
pip install pandas numpy matplotlib
```

## Required Data Files

The script expects the following CSV files to be present in the same directory as the script:
- `05L_rms_ispind_big.csv`
- `15L_rms_ispind_big.csv`
- `2L_rms_ispind_big.csv`

one file for each size bottle.

## How to Run

Navigate to your project directory in the terminal and execute the script using Python:

```bash
python res_rms.py <folder_path>
```
Basicly give it one of the folders in the rms folder and it will plot the data. 
```bash
python res_rms.py Lsensor_260KOhm
```

## Naming: 
ispind -- The setup we have where the sensor is held down by the "ispind"\n
Lsensor -- New setup I made, where a very large piezo sensor is glued to the membrane.
260kOhm -- The resistor connected to the sensor, which is 260k Ohm.
15MOhm -- The resistor connected to the sensor, which is 1,5 Mio Ohm.
4000hz -- The sampling frequency, which is 4000 Hz.
512s -- The number of samples taken, which is 512 samples. standard is 128 samples.
squ -- the falsk is squeezed once during the test. medium and samll refers to the amount of squeezing. 

