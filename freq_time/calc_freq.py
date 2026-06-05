import serial
import numpy as np
from collections import deque

PORT = "COM8"          # change this (Linux: /dev/ttyACM0)
BAUD = 500_000

SAMPLE_RATE = 1000     # MUST match Arduino

ser = serial.Serial(PORT, BAUD)
BUFFER_SIZE = 1024 
STEP = 64

buffer = deque(maxlen=BUFFER_SIZE)
time_buffer = deque(maxlen=BUFFER_SIZE)

while True:
    line = ser.readline().decode().strip()

    try:
        t_str, v_str = line.split(",")
        t = int(t_str)
        v = int(v_str)

        buffer.append(v)
        time_buffer.append(t)

        if len(buffer) < BUFFER_SIZE:
            continue

        x = np.array(buffer)
        x = x - np.mean(x)
        x = x * np.hanning(BUFFER_SIZE)

        # time_diff = (time_buffer[-1] - time_buffer[0]) / 1e6
        # fs = (BUFFER_SIZE - 1) / time_diff
        fs = SAMPLE_RATE
        fft = np.fft.rfft(x)
        freqs = np.fft.rfftfreq(BUFFER_SIZE, d=1/fs)

        mag = np.abs(fft)
        mag[0] = 0
        idx = np.argmax(mag)
        # local quadratic interpolation (VERY effective)
        
        dominant = freqs[idx]
        
        print(f"{dominant:.2f} Hz")

        # rolling shift
        for _ in range(STEP):
            buffer.popleft()
            time_buffer.popleft()

    except:
        continue
# buffer = deque(maxlen=BUFFER_SIZE)
# time_buffer = deque(maxlen=BUFFER_SIZE)
# lst = []
# print("Reading...")

# for _ in range(10*BUFFER_SIZE):  # Arbitrary large number to keep reading until interrupted
#     line = ser.readline().decode().strip()

#     try:
#         t_str, v_str = line.split(",")
#         t = int(t_str)
#         v = int(v_str)

#         buffer.append(v)
#         time_buffer.append(t)

#         if len(buffer) == BUFFER_SIZE:
#             x = np.array(buffer)
#             x = x - np.mean(x)
#             x = x * np.hanning(BUFFER_SIZE) # Apply a Hanning window
#             # FFT
#             # time_diff_sec = (time_buffer[-1] - time_buffer[0]) / 1_000_000.0
#             # actual_sample_rate = (BUFFER_SIZE - 1) / time_diff_sec
#             fs = SAMPLE_RATE
#             fft = np.fft.rfft(x)
#             freqs = np.fft.rfftfreq(BUFFER_SIZE, d=1/fs)

#             mag = np.abs(fft)
#             mag[0] = 0  # Ignore DC component
#             mag[freqs < 5] = 0
#             idx = np.argmax(mag)
#             window = 5

#             start = max(0, idx - window)
#             end = min(len(mag), idx + window)

#             dominant = np.sum(freqs[start:end] * mag[start:end]) / np.sum(mag[start:end])
#             dominant = freqs[np.argmax(mag)]
#             #dominant = freqs[np.argmax(mag)]

#             print(f"Dominant frequency: {dominant:.2f} Hz")
#             buffer.clear()
#             time_buffer.clear()
#             lst.append(dominant)

#     except:
        
#         continue

# res = np.array(lst)
# print(f"Mean frequency: {np.mean(res):.2f} Hz")
# print(f"Std frequency: {np.std(res):.2f} Hz")
# print(f"Max frequency: {np.max(res):.2f} Hz")
# print(f"Min frequency: {np.min(res):.2f} Hz")
