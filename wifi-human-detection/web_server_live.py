"""
🌐 Web Server ao Vivo - Wi-Fi CSI Human Activity Detection
Versão otimizada para rede local com WebSocket
Acesse: http://SEU-IP:5000 (ex: http://192.168.1.100:5000)
"""
import os
import json
import threading
import time
import socket
from datetime import datetime
from collections import deque
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import numpy as np
import joblib
import serial
import re
from parse_csi import parse_csi_amplitude

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Inicialização Flask + SocketIO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wifi-sensing-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
CORS(app)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Configuração
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200
BUFFER_SIZE = 200

# Estado Global
data_buffer = deque(maxlen=BUFFER_SIZE)
latest_activity = "Waiting..."
model = None
ser = None
connected = False
clients_connected = 0

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Utilidades de Rede
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_local_ip():
    """Obtém IP local da máquina"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

LOCAL_IP = get_local_ip()
print(f"🌐 IP Local: {LOCAL_IP}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Carregar Modelo ML
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def load_model(model_path="model.pkl"):
    global model
    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            print(f"✓ Modelo carregado: {model_path}")
            socketio.emit('model_loaded', {'success': True}, broadcast=True)
            return True
        except Exception as e:
            print(f"✗ Erro ao carregar modelo: {e}")
            socketio.emit('model_loaded', {'success': False, 'error': str(e)}, broadcast=True)
            return False
    print(f"⚠ Modelo não encontrado: {model_path}")
    return False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Conexão Serial
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def init_serial(port=SERIAL_PORT, baudrate=BAUD_RATE):
    global ser, connected
    try:
        ser = serial.Serial(port, baudrate, timeout=0.1)
        connected = True
        print(f"✓ Serial conectado: {port} @ {baudrate}")
        socketio.emit('connection_status', {
            'connected': True,
            'port': port,
            'baud': baudrate
        }, broadcast=True)
        return True
    except Exception as e:
        print(f"✗ Erro serial: {e}")
        socketio.emit('connection_status', {
            'connected': False,
            'error': str(e)
        }, broadcast=True)
        connected = False
        return False

def parse_csi_data(line):
    """Processa linha CSI bruta"""
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
            'time': datetime.now().strftime("%H:%M:%S"),
            'datetime': datetime.now().isoformat()
        }
    except:
        return None

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Thread de Leitura Serial (com WebSocket)
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

                # Parsear dados CSI
                csi_data = parse_csi_data(line)
                if csi_data:
                    data_buffer.append(csi_data)

                    # Fazer predição ML
                    if model and len(csi_data['amplitudes']) > 10:
                        try:
                            X = np.array(csi_data['amplitudes']).reshape(1, -1)
                            prediction = model.predict(X)[0]
                            latest_activity = prediction

                            # Emitir em tempo real via WebSocket
                            socketio.emit('activity_detected', {
                                'activity': prediction,
                                'rssi': csi_data['rssi'],
                                'time': csi_data['time'],
                                'buffer_size': len(data_buffer)
                            }, broadcast=True)
                        except:
                            pass

            time.sleep(0.01)
        except Exception as e:
            print(f"Serial error: {e}")
            connected = False
            time.sleep(1)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Rotas HTTP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/')
def index():
    return render_template('dashboard_live.html', local_ip=LOCAL_IP)

@app.route('/api/status')
def get_status():
    return jsonify({
        'connected': connected,
        'activity': latest_activity,
        'buffer_size': len(data_buffer),
        'timestamp': datetime.now().isoformat(),
        'clients': clients_connected,
        'local_ip': LOCAL_IP
    })

@app.route('/api/data')
def get_data():
    return jsonify({
        'data': list(data_buffer)[-50:],
        'activity': latest_activity
    })

@app.route('/api/connect', methods=['POST'])
def connect_serial():
    port = request.json.get('port', SERIAL_PORT)
    baud = request.json.get('baud', BAUD_RATE)

    if init_serial(port, baud):
        return jsonify({'success': True})
    return jsonify({'success': False}), 400

@app.route('/api/send', methods=['POST'])
def send_command():
    global ser, connected
    if not connected or not ser:
        return jsonify({'error': 'Not connected'}), 400

    command = request.json.get('command', '')
    try:
        ser.write(f"{command}\n".encode())
        socketio.emit('command_sent', {'command': command}, broadcast=True)
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
    if not data_buffer:
        return "timestamp,rssi,amplitudes\n", 200

    csv = "timestamp,rssi,amplitudes\n"
    for item in data_buffer:
        amps = ','.join(map(str, item['amplitudes'][:10]))
        csv += f"{item['time']},{item['rssi']},{amps}\n"

    return csv, 200, {'Content-Type': 'text/csv'}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# WebSocket Events (Tempo Real)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@socketio.on('connect')
def handle_connect():
    global clients_connected
    clients_connected += 1
    print(f"✓ Cliente conectado. Total: {clients_connected}")

    emit('connection_response', {
        'data': 'Conectado ao servidor Wi-Fi Sensing',
        'connected': connected,
        'activity': latest_activity,
        'buffer_size': len(data_buffer),
        'local_ip': LOCAL_IP
    })

@socketio.on('disconnect')
def handle_disconnect():
    global clients_connected
    clients_connected -= 1
    print(f"✗ Cliente desconectado. Total: {clients_connected}")

@socketio.on('request_update')
def handle_update_request():
    """Cliente requisita atualização de estado"""
    if data_buffer:
        latest = data_buffer[-1]
        emit('data_update', {
            'activity': latest_activity,
            'rssi': latest['rssi'],
            'time': latest['time'],
            'buffer_size': len(data_buffer),
            'amplitudes': latest['amplitudes'][:20]
        })

@socketio.on('send_command')
def handle_send_command(data):
    """WebSocket para enviar comando"""
    command = data.get('command', '')
    result = send_command_internal(command)
    emit('command_response', {'success': result})

def send_command_internal(command):
    global ser, connected
    if not connected or not ser:
        return False
    try:
        ser.write(f"{command}\n".encode())
        return True
    except:
        return False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Inicialização
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌐 Web Server Wi-Fi Sensing - Versão ao Vivo")
    print("="*60)
    print(f"\n📍 Acesse no navegador:")
    print(f"   http://localhost:5000")
    print(f"   http://{LOCAL_IP}:5000  (rede local)")
    print(f"\n📱 No celular (mesma rede):")
    print(f"   Abra: http://{LOCAL_IP}:5000")
    print(f"\n🔌 Conexão Serial:")
    print(f"   Porta: /dev/ttyUSB0 (Linux/Mac) ou COM3 (Windows)")
    print(f"   Baud: 115200")
    print("\n" + "="*60)
    print("Carregando modelo...")

    # Carrega modelo se existir
    load_model()

    # Tenta conectar ESP32 automaticamente
    init_serial()

    # Inicia thread de leitura
    reader_thread = threading.Thread(target=serial_reader_thread, daemon=True)
    reader_thread.start()

    # Inicia servidor SocketIO
    print(f"✓ Servidor iniciado!\n")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
