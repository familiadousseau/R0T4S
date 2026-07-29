"""
Web Server para Wi-Fi CSI Human Activity Detection
Acesso via browser: http://localhost:5000
"""
import os
import json
import threading
import time
from datetime import datetime
from collections import deque
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import numpy as np
import joblib
import serial
import re
from parse_csi import parse_csi_amplitude

app = Flask(__name__)
CORS(app)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Configuração
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200
BUFFER_SIZE = 100  # Últimos 100 dados

# Armazenam dados para exibir no dashboard
data_buffer = deque(maxlen=BUFFER_SIZE)
latest_activity = "Waiting..."
model = None
ser = None
connected = False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Carregar Modelo ML
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def load_model(model_path="model.pkl"):
    global model
    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            print(f"✓ Modelo carregado: {model_path}")
            return True
        except Exception as e:
            print(f"✗ Erro ao carregar modelo: {e}")
            return False
    print(f"⚠ Modelo não encontrado: {model_path}")
    return False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Conexão Serial com ESP32
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def init_serial(port=SERIAL_PORT, baudrate=BAUD_RATE):
    global ser, connected
    try:
        ser = serial.Serial(port, baudrate, timeout=0.1)
        connected = True
        print(f"✓ Conectado em {port} @ {baudrate} baud")
        return True
    except Exception as e:
        print(f"✗ Erro conexão serial: {e}")
        connected = False
        return False

def parse_csi_data(line):
    """Extrai dados CSI da linha CSV"""
    try:
        csi_match = re.findall(r'\[(.*?)\]', line)
        if not csi_match:
            return None

        raw_csi = csi_match[0]
        amplitudes = parse_csi_amplitude(f"[{raw_csi}]")

        parts = line.split(',')
        rssi = int(parts[2]) if len(parts) > 2 else 0
        timestamp = float(parts[-2]) if len(parts) > 1 else 0

        return {
            'amplitudes': amplitudes.tolist(),
            'rssi': rssi,
            'timestamp': timestamp,
            'time': datetime.now().strftime("%H:%M:%S")
        }
    except:
        return None

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Thread de Leitura Serial
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def serial_reader_thread():
    global ser, latest_activity, data_buffer, connected

    while True:
        try:
            if not connected or not ser:
                time.sleep(1)
                continue

            if ser.in_waiting:
                line = ser.readline().decode('utf-8', errors='ignore').strip()

                if not line or line.startswith('type,'):
                    continue

                # Parse dados CSI
                csi_data = parse_csi_data(line)
                if csi_data:
                    data_buffer.append(csi_data)

                    # Tenta fazer predição com ML
                    if model and len(csi_data['amplitudes']) > 10:
                        try:
                            X = np.array(csi_data['amplitudes']).reshape(1, -1)
                            prediction = model.predict(X)[0]
                            latest_activity = prediction
                        except:
                            pass

            time.sleep(0.01)
        except Exception as e:
            print(f"Serial read error: {e}")
            time.sleep(0.5)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Rotas Flask
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/status')
def get_status():
    return jsonify({
        'connected': connected,
        'activity': latest_activity,
        'buffer_size': len(data_buffer),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/data')
def get_data():
    """Retorna últimos dados do buffer"""
    return jsonify({
        'data': list(data_buffer),
        'activity': latest_activity
    })

@app.route('/api/csi')
def get_csi():
    """Retorna CSI do último dado"""
    if data_buffer:
        latest = data_buffer[-1]
        return jsonify({
            'amplitudes': latest['amplitudes'],
            'rssi': latest['rssi'],
            'time': latest['time']
        })
    return jsonify({'error': 'No data'}), 404

@app.route('/api/connect', methods=['POST'])
def connect_serial():
    global connected
    port = request.json.get('port', SERIAL_PORT)
    baud = request.json.get('baud', BAUD_RATE)

    if init_serial(port, baud):
        return jsonify({'success': True, 'message': f'Conectado em {port}'})
    return jsonify({'success': False, 'message': 'Falha ao conectar'}), 400

@app.route('/api/send', methods=['POST'])
def send_command():
    global ser, connected
    if not connected or not ser:
        return jsonify({'error': 'Not connected'}), 400

    command = request.json.get('command', '')
    try:
        ser.write(f"{command}\n".encode())
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/model/load', methods=['POST'])
def load_model_endpoint():
    path = request.json.get('path', 'model.pkl')
    if load_model(path):
        return jsonify({'success': True})
    return jsonify({'success': False}), 400

@app.route('/api/history')
def get_history():
    """Retorna histórico em formato CSV"""
    if not data_buffer:
        return "timestamp,rssi,amplitudes\n", 200

    csv = "timestamp,rssi,amplitudes\n"
    for item in data_buffer:
        amps = ','.join(map(str, item['amplitudes'][:10]))  # Primeiras 10 subportadoras
        csv += f"{item['time']},{item['rssi']},{amps}\n"

    return csv, 200, {'Content-Type': 'text/csv'}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Inicialização
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == '__main__':
    print("🚀 Iniciando Web Server...")
    print("📍 Acesse: http://localhost:5000")

    # Carrega modelo ML
    load_model()

    # Inicia conexão serial
    init_serial()

    # Inicia thread de leitura
    reader_thread = threading.Thread(target=serial_reader_thread, daemon=True)
    reader_thread.start()

    # Inicia servidor
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
