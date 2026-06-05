import serial
import csv
import time
import sys

num_runs = 20
num_samples = 1000

file_name = sys.argv[1] if len(sys.argv) > 1 else 'piezo_data.csv'

# Match Arduino baud rate
ser = serial.Serial('COM8', 500000)

with open(file_name, 'w', newline='') as file:
    writer = csv.writer(file)
    # CSV header
    writer.writerow(['time', 'value','run'])
    for run in range(num_runs):
        print(f"Saving data run {run}... Press Ctrl+C to stop.")

        for _ in range(num_samples):  
            line = ser.readline().decode(errors='ignore').strip()

            if not line:
                continue

            try:
                # Arduino sends: timestamp,value
                parts = line.split(',')

                if len(parts) != 2:
                    continue

                arduino_time_us = int(parts[0])
                value = int(parts[1])

                # Convert microseconds -> seconds
                t = arduino_time_us / 1_000_000.0
                # Write to CSV: time, value, run
                writer.writerow([t, value, run])

            except ValueError:
                # Skip malformed lines
                print(f"Warning: Could not parse line: {line}")
                continue

    ser.close()
    print(f"Data saved to {file_name}")
