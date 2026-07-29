import numpy as np
import pandas as pd
from scipy import signal
from scipy.stats import skew, kurtosis
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os
import glob

def parse_csi_amplitude(raw_csi_string):
    vals = list(map(int, raw_csi_string.strip('[]').split()))
    amplitudes = []
    for i in range(0, len(vals) - 1, 2):
        imag = vals[i]
        real = vals[i + 1]
        amp = np.sqrt(real**2 + imag**2)
        amplitudes.append(amp)
    return np.array(amplitudes)

def load_csv(filepath, label):
    records = []
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Join lines so split CSI data comes together
    content = content.replace('\n', ' ')
    
    # Split by CSI_DATA entries
    entries = content.split('CSI_DATA,')
    
    for entry in entries[1:]:  # skip first empty split
        try:
            bracket_start = entry.index('[')
            bracket_end = entry.index(']')
            raw_csi = entry[bracket_start:bracket_end+1]
            amp = parse_csi_amplitude(raw_csi)
            if len(amp) > 10:
                records.append((amp, label))
        except:
            continue
    
    return records

def load_all_data(data_dir):
    all_records = []
    activity_folders = [f for f in os.listdir(data_dir)
                        if os.path.isdir(os.path.join(data_dir, f))]
    for activity in activity_folders:
        folder_path = os.path.join(data_dir, activity)
        csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
        for csv_file in csv_files:
            records = load_csv(csv_file, label=activity)
            all_records.extend(records)
            print(f"Loaded {len(records)} samples from {csv_file}")
    return all_records

def bandpass_filter(data, lowcut=1.0, highcut=50.0, fs=100.0, order=4):
    nyq = fs / 2.0
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    return signal.filtfilt(b, a, data, axis=0)

def sliding_window(records, window_size=100, step=50):
    windows = []
    labels = []
    from itertools import groupby
    records_sorted = sorted(records, key=lambda x: x[1])
    for label, group in groupby(records_sorted, key=lambda x: x[1]):
        group = list(group)
        min_len = min(len(r[0]) for r in group)
        group_amps = np.array([r[0][:min_len] for r in group])
        if len(group_amps) < window_size:
            continue
        try:
            group_amps = bandpass_filter(group_amps)
        except:
            pass
        for start in range(0, len(group_amps) - window_size, step):
            window = group_amps[start:start + window_size]
            windows.append(window)
            labels.append(label)
    return windows, labels

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

def build_feature_matrix(windows, labels):
    X = np.array([extract_features(w) for w in windows])
    y = np.array(labels)
    print(f"Feature matrix shape: {X.shape}")
    print(f"Labels: {np.unique(y)}")
    return X, y

def train_model(X, y):
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    print("\n── Classification Report ──")
    print(classification_report(y_test, y_pred,
                                target_names=le.classes_))
    print("── Confusion Matrix ──")
    print(confusion_matrix(y_test, y_pred))
    return rf, le

def save_model(rf, le, path='model/'):
    os.makedirs(path, exist_ok=True)
    joblib.dump(rf, os.path.join(path, 'random_forest.pkl'))
    joblib.dump(le, os.path.join(path, 'label_encoder.pkl'))
    print(f"\nModel saved to {path}")

if __name__ == "__main__":
    print("Loading data...")
    records = load_all_data('data/')

    print("\nCreating windows...")
    windows, labels = sliding_window(records, window_size=100, step=50)
    print(f"Total windows: {len(windows)}")

    print("\nExtracting features...")
    X, y = build_feature_matrix(windows, labels)

    print("\nTraining Random Forest...")
    rf, le = train_model(X, y)

    save_model(rf, le)