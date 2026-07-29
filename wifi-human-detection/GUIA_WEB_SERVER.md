# 🌐 Guia Completo - Web Server Wi-Fi Sensing

Aprenda a acessar e controlar o projeto Wi-Fi CSI Human Activity Detection através de um navegador web!

---

## 📋 Pré-requisitos

### Hardware
- ✅ ESP32 com firmware compilado (main.cc)
- ✅ Conectado via USB (porta serial)
- ✅ OLED Display SSD1306 (opcional, mas recomendado)

### Software Instalado
- ✅ Python 3.8+
- ✅ pip (gerenciador de pacotes Python)
- ✅ Navegador web moderno (Chrome, Firefox, Edge, Safari)

---

## 🚀 Instalação Passo a Passo

### 1️⃣ Instalar Dependências

```bash
cd /home/user/R0T4S/wifi-human-detection
pip install -r requirements.txt
```

**O que será instalado:**
- Flask (servidor web)
- Flask-CORS (comunicação entre cliente/servidor)
- NumPy, Pandas, SciPy (processamento de dados)
- scikit-learn (Machine Learning)
- pyserial (comunicação com ESP32)

### 2️⃣ Treinar o Modelo ML (Opcional)

Se você já tiver dados de treinamento:

```bash
python pipeline.py --data-dir ./data --output model.pkl
```

Se não tiver, use o `example_csi.csv` como teste:

```bash
python pipeline.py --data-dir ./data --output model.pkl
```

### 3️⃣ Iniciar o Servidor Web

```bash
python web_server.py
```

**Saída esperada:**
```
🚀 Iniciando Web Server...
📍 Acesse: http://localhost:5000
✓ Modelo carregado: model.pkl
✓ Conectado em /dev/ttyUSB0 @ 115200 baud
```

### 4️⃣ Acessar no Navegador

Abra seu navegador e acesse:
```
http://localhost:5000
```

**Ou de outro computador na rede:**
```
http://seu-ip-aqui:5000
```

Para descobrir seu IP:
```bash
# Linux/Mac
ifconfig | grep "inet " | grep -v 127.0.0.1

# Windows
ipconfig
```

---

## 📊 Dashboard - Guia de Uso

### 🎯 Tela Principal

```
┌─────────────────────────────────────────┐
│  🛰️  Wi-Fi CSI Human Activity Detection  │
│                                          │
│  ✓ Conectado  |  Atividade: WALKING     │
│  Buffer: 42 amostras                    │
└─────────────────────────────────────────┘
```

### 🔌 Seção de Conexão Serial

**Campos:**
- **Porta Serial:** `/dev/ttyUSB0` (Linux/Mac) ou `COM3` (Windows)
- **Baud Rate:** `115200` (padrão para ESP32)

**Botões:**
- 🔴 **Conectar:** Estabelece conexão com ESP32
- ✓ **Desconectar:** Finaliza conexão

**Status:**
- Verde (✓ Online) = Conectado
- Vermelho (✗ Offline) = Desconectado

#### Encontrar sua Porta Serial

**Linux/Mac:**
```bash
ls /dev/tty* | grep USB
# Resultado: /dev/ttyUSB0 ou /dev/ttyACM0
```

**Windows:**
- Abra Gerenciador de Dispositivos
- Procure em "Portas COM e LPT"
- Exemplo: COM3, COM4, etc.

---

### 🤖 Seção de Machine Learning

**Caminho do Modelo:** Localização do arquivo `.pkl`

Exemplos válidos:
```
model.pkl              # Mesmo diretório
./models/model.pkl     # Subpasta
/home/user/model.pkl   # Caminho absoluto
```

**Status ML:**
- ✓ Pronto = Modelo carregado e pronto
- ✗ Off = Modelo não carregado

**Predições:** Contador de atividades detectadas

---

### 📈 Gráficos em Tempo Real

#### CSI Amplitude
- **Exibe:** Amplitude do sinal de cada subportadora Wi-Fi
- **Cores:** Azul (degradê)
- **Atualiza:** A cada 500ms

#### RSSI (Signal Strength)
- **Exibe:** Força do sinal recebido em dBm
- **Range Típico:** -40 a -80 dBm
- **Mais negativo = mais fraco**

---

### 🎮 Controle ESP32

Botões para enviar comandos:

| Botão | Comando | LEDs |
|-------|---------|------|
| 🚶 Walking | `LABEL:walking` | Vermelho |
| 🪑 Sitting | `LABEL:sitting` | Verde |
| 🧍 Standing | `LABEL:standing` | Amarelo |
| 🗑️ Limpar | Limpa buffer | --- |

---

### 📋 Log de Eventos

Exibe histórico de operações:

```
[14:32:15] ✓ Conectado com sucesso
[14:32:18] ✓ Modelo carregado: model.pkl
[14:32:45] 📤 Enviado: walking
[14:35:22] ✓ Histórico baixado
```

---

### 📥 Baixar Histórico

Botão **⬇️ Baixar Histórico CSV**

Exporta dados em formato CSV:
```
timestamp,rssi,amplitudes
14:32:15,-45,10 20 15 18 22 19 21 18 17 20
14:32:16,-46,12 21 16 19 23 20 22 19 18 21
...
```

Use para análise posterior em Excel/Python!

---

## 🔧 API REST - Documentação Técnica

### Endpoints Disponíveis

#### 1. GET `/` - Dashboard
```
Retorna: HTML do dashboard
Status: 200 OK
```

#### 2. GET `/api/status` - Status do Sistema
```json
{
  "connected": true,
  "activity": "walking",
  "buffer_size": 42,
  "timestamp": "2025-07-29T14:32:15.123456"
}
```

#### 3. GET `/api/data` - Últimos Dados
```json
{
  "data": [
    {
      "amplitudes": [10, 20, 15, ...],
      "rssi": -45,
      "timestamp": 1234567890.123,
      "time": "14:32:15"
    }
  ],
  "activity": "walking"
}
```

#### 4. GET `/api/csi` - Último Dado CSI
```json
{
  "amplitudes": [10, 20, 15, 18, 22, ...],
  "rssi": -45,
  "time": "14:32:15"
}
```

#### 5. POST `/api/connect` - Conectar Serial
```json
{
  "port": "/dev/ttyUSB0",
  "baud": 115200
}
```
Resposta: `{"success": true, "message": "Conectado..."}`

#### 6. POST `/api/send` - Enviar Comando
```json
{
  "command": "LABEL:walking"
}
```
Resposta: `{"success": true}`

#### 7. POST `/api/model/load` - Carregar Modelo
```json
{
  "path": "model.pkl"
}
```
Resposta: `{"success": true}`

#### 8. GET `/api/history` - Exportar Histórico
```
Content-Type: text/csv
Retorna: Arquivo CSV com todos os dados
```

---

## 🐍 Código Personalizado

### Exemplo 1: Coletar Dados Programaticamente

```python
import requests

# Obter status
response = requests.get('http://localhost:5000/api/status')
status = response.json()
print(f"Atividade: {status['activity']}")
print(f"Buffer: {status['buffer_size']} amostras")
```

### Exemplo 2: Enviar Comandos

```python
import requests
import time

# Enviar comando
payload = {"command": "LABEL:standing"}
requests.post('http://localhost:5000/api/send', json=payload)
time.sleep(2)

# Verificar status
status = requests.get('http://localhost:5000/api/status').json()
print(f"Atividade: {status['activity']}")
```

### Exemplo 3: Processar Dados em Tempo Real

```python
import requests
import time

while True:
    # Buscar dados
    data = requests.get('http://localhost:5000/api/data').json()
    
    if data['data']:
        latest = data['data'][-1]
        print(f"RSSI: {latest['rssi']} dBm")
        print(f"Amplitude média: {sum(latest['amplitudes'])/len(latest['amplitudes']):.2f}")
    
    time.sleep(0.5)
```

---

## 🐛 Solução de Problemas

### ❌ "Conexão recusada" na porta serial

**Problema:** ESP32 não conecta ou porta errada

**Solução:**
```bash
# Listar portas disponíveis
ls -l /dev/tty* | grep USB

# Dar permissão de acesso (Linux)
sudo chmod 666 /dev/ttyUSB0

# Ou adicionar usuário ao grupo
sudo usermod -a -G dialout $USER
```

### ❌ "Módulo não encontrado" (ImportError)

**Problema:** Dependências não instaladas

**Solução:**
```bash
pip install -r requirements.txt --upgrade
```

### ❌ Modelo não carrega

**Problema:** Arquivo não encontrado ou corrompido

**Solução:**
```bash
# Verificar se existe
ls -la model.pkl

# Treinar novo modelo
python pipeline.py --data-dir ./data --output model.pkl
```

### ❌ Dashboard vazio/sem dados

**Problema:** Nenhuma comunicação com ESP32

**Solução:**
1. Verifique porta serial
2. Verifique baud rate (115200)
3. Reinicie ESP32
4. Verifique com: `minicom -D /dev/ttyUSB0 -b 115200`

### ❌ "Port already in use"

**Problema:** Porta 5000 já em uso

**Solução:**
```bash
# Usar porta diferente
# Edite web_server.py: app.run(..., port=5001)

# Ou mate processo na porta 5000
lsof -i :5000
kill -9 <PID>
```

---

## 📱 Acessar de Outro Computador

### Na Mesma Rede Local

1. **Descubra o IP do servidor:**
   ```bash
   ifconfig | grep "inet "
   # Procure por algo como: 192.168.1.100
   ```

2. **Acesse no outro computador:**
   ```
   http://192.168.1.100:5000
   ```

### Pela Internet (Port Forwarding)

⚠️ **Requer configuração de roteador!**

1. Configure port forwarding no roteador para a porta 5000
2. Descubra seu IP público: https://whatismyipaddress.com
3. Acesse: `http://seu-ip-publico:5000`

---

## 📊 Processando Dados Offline

### Exportar e Analisar em Python

```python
import pandas as pd
import matplotlib.pyplot as plt

# Baixar histórico do web server
import requests
response = requests.get('http://localhost:5000/api/history')
with open('data.csv', 'w') as f:
    f.write(response.text)

# Carregar e analisar
df = pd.read_csv('data.csv')
print(df.head())
print(df.describe())

# Plotar
plt.figure(figsize=(12, 6))
plt.plot(df['timestamp'], df['rssi'])
plt.xlabel('Tempo')
plt.ylabel('RSSI (dBm)')
plt.title('Força do Sinal Wi-Fi')
plt.show()
```

---

## 🚀 Deployment em Servidor

### Usar Gunicorn (Produção)

```bash
pip install gunicorn

# Iniciar com 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 web_server:app
```

### Com Nginx (Proxy Reverso)

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## ✨ Recursos Avançados

### Real-time WebSocket (Futuro)

Para atualizações mais rápidas, você pode adicionar WebSockets:

```python
from flask_socketio import SocketIO
io = SocketIO(app)

@io.on('connect')
def handle_connect():
    print('Cliente conectado')
```

### Dashboard Customizado

Edite `templates/dashboard.html` para adicionar seus próprios gráficos e funcionalidades!

---

## 📚 Referências Úteis

- **Flask Docs:** https://flask.palletsprojects.com
- **Chart.js:** https://www.chartjs.org
- **scikit-learn ML:** https://scikit-learn.org
- **ESP32 Docs:** https://docs.espressif.com

---

## 🎯 Próximos Passos

1. ✅ Web server funcionando
2. ⬜ Treinar modelo com seus dados
3. ⬜ Personalizar dashboard
4. ⬜ Adicionar novas atividades
5. ⬜ Deploy em servidor

---

**Parabéns! 🎉 Você agora tem acesso completo ao seu projeto Wi-Fi Sensing via web!**

Para mais informações, veja `WIFI_SENSING_PROJECT.md`
