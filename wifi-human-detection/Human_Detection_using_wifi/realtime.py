import serial
import numpy as np
import joblib
import os
import time
from scipy import signal
from scipy.stats import skew, kurtosis
from collections import deque
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

# ── Configuration ──
PORT = 'COM3'
BAUD = 115200
WINDOW_SIZE = 30
MODEL_DIR = 'model/'
SEND_INTERVAL = 3.0      # send to ESP32 every 3 seconds

# ── Load Model ──
print("Loading model...")
rf = joblib.load(os.path.join(MODEL_DIR, 'random_forest.pkl'))
le = joblib.load(os.path.join(MODEL_DIR, 'label_encoder.pkl'))
print(f"Model loaded. Classes: {le.classes_}")

# ── Feature Extraction ──
def parse_csi_amplitude(raw_csi_string):
    vals = list(map(int, raw_csi_string.strip('[]').split()))
    amplitudes = []
    for i in range(0, len(vals) - 1, 2):
        imag = vals[i]
        real = vals[i + 1]
        amp = np.sqrt(real**2 + imag**2)
        amplitudes.append(amp)
    return np.array(amplitudes)

def bandpass_filter(data, lowcut=1.0, highcut=50.0, fs=100.0, order=4):
    nyq = fs / 2.0
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    return signal.filtfilt(b, a, data, axis=0)

def extract_features(window):
    features = []
    for subcarrier in window.T:
        features.append(np.mean(subcarrier))
        features.append(np.std(subcarrier))
        features.append(np.min(subcarrier))
        features.append(np.max(subcarrier))
        features.append(np.max(subcarrier) - np.min(subcarrier))
        features.append(skew(subcarrier))
        features.append(kurtosis(subcarrier))
        features.append(np.sum(subcarrier**2))
    flat = window.flatten()
    features.append(np.mean(flat))
    features.append(np.std(flat))
    features.append(np.median(flat))
    return np.array(features)

def predict(window):
    try:
        filtered = bandpass_filter(window)
    except:
        filtered = window
    features = extract_features(filtered).reshape(1, -1)
    pred = rf.predict(features)[0]
    confidence = np.max(rf.predict_proba(features)) * 100
    label = le.inverse_transform([pred])[0]
    return label, confidence

def send_label(ser, label):
    """Send label, wait for ACK, drain any junk from serial."""
    try:
        # Drain anything sitting in RX buffer before writing
        ser.reset_input_buffer()
        ser.write(f"LABEL:{label}\n".encode())
        ser.flush()

        # Wait briefly for ACK
        deadline = time.time() + 0.5
        ack_buf = ''
        while time.time() < deadline:
            if ser.in_waiting:
                ack_buf += ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
                if 'ACK:' in ack_buf:
                    print(f">>> ESP32 ACK received")
                    break
            time.sleep(0.01)

        # Drain again after write so CSI resumes cleanly
        time.sleep(0.1)
        ser.reset_input_buffer()
        print(f">>> Sent to ESP32: {label}")
    except Exception as e:
        print(f"Send error: {e}")

# ── Main Loop ──
print(f"Connecting to ESP32 on {PORT}...")
print("Press Ctrl+C to stop\n")

buffer = deque(maxlen=WINDOW_SIZE)
last_send_time = 0
latest_label = ""
raw_buffer = ''

with serial.Serial(PORT, BAUD, timeout=2) as ser:
    print("Connected. Reading CSI...\n")

    while True:
        try:
            # Read all available bytes
            waiting = ser.in_waiting
            if waiting:
                chunk = ser.read(waiting).decode('utf-8', errors='ignore')
                raw_buffer += chunk

            while '\n' in raw_buffer:
                line, raw_buffer = raw_buffer.split('\n', 1)
                line = line.strip()

                if line.startswith('ACK:') or line.startswith('LABEL:'):
                    continue

                if not line.startswith('CSI_DATA'):
                    continue

                if '[' in line and ']' not in line:
                    raw_buffer = line + '\n' + raw_buffer
                    break

                if '[' not in line:
                    continue
                if ']' not in line:
                    raw_buffer = line + raw_buffer
                    continue

                try:
                    b_start = line.index('[')
                    b_end = line.index(']')
                    raw_csi = line[b_start:b_end+1]
                    amp = parse_csi_amplitude(raw_csi)

                    if len(amp) <= 10:
                        continue

                    buffer.append(amp)

                    if len(buffer) < WINDOW_SIZE:
                        print(f"Buffering... {len(buffer)}/{WINDOW_SIZE}")
                        continue

                    min_len = min(len(a) for a in buffer)
                    window_arr = np.array([a[:min_len] for a in buffer])
                    label, confidence = predict(window_arr)
                    latest_label = label

                    print(f"Activity: {label:12s} | Confidence: {confidence:.1f}%")

                except Exception as e:
                    print(f"Parse error: {e}")
                    continue

            # Send to ESP32 at interval — only after processing current buffer
            now = time.time()
            if latest_label and (now - last_send_time) >= SEND_INTERVAL:
                last_send_time = now
                send_label(ser, latest_label)

            time.sleep(0.005)

        except KeyboardInterrupt:
            print("\nStopped.")
            break