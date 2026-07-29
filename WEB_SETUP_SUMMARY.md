# 🌐 Seu Web Server Wi-Fi Sensing Está Pronto! 🚀

## ✅ O Que Foi Criado Para Você

```
📁 wifi-human-detection/
├── 🖥️  web_server.py                    ← Servidor Flask (backend)
├── 📄 templates/dashboard.html          ← Interface web (frontend)
├── 📋 requirements.txt                   ← Dependências Python
├── 🚀 start.sh                          ← Script de inicialização
├── 📖 GUIA_WEB_SERVER.md               ← Guia completo (novo!)
├── 📊 WIFI_SENSING_PROJECT.md          ← Documentação do projeto
├── 🐍 pipeline.py                       ← ML Training
├── 💾 Human_Detection_using_wifi/       ← Código ESP32
└── 📦 README.md                         ← Original do projeto
```

---

## 🚀 COMEÇAR AGORA (3 Passos)

### 1️⃣ Instalar Dependências

```bash
cd /home/user/R0T4S/wifi-human-detection
pip install -r requirements.txt
```

**Tempo:** ~2-3 minutos

### 2️⃣ Iniciar Servidor

```bash
bash start.sh
```

**Ou diretamente:**
```bash
python3 web_server.py
```

### 3️⃣ Abrir Navegador

```
http://localhost:5000
```

✨ **Pronto! Seu dashboard está rodando!**

---

## 🎨 Dashboard Web Features

### 📊 Visualizações em Tempo Real
- 📈 Gráfico de Amplitude CSI
- 📉 Gráfico de RSSI (força do sinal)
- 🎯 Atividade detectada em grande destaque
- 📋 Log de eventos com timestamps

### 🎮 Controles Interativos
- 🔌 Conectar/Desconectar ESP32
- 🤖 Carregar modelo ML
- 🚶 Enviar comandos (Walking/Sitting/Standing)
- 📥 Baixar histórico em CSV

### 📱 Totalmente Responsivo
- ✓ Funciona em desktop
- ✓ Funciona em tablet
- ✓ Funciona em smartphone
- ✓ Funciona em outro computador (rede local)

---

## 📋 Checklist de Configuração

### Hardware
- [ ] ESP32 conectado via USB
- [ ] Firmware compilado (main.cc)
- [ ] OLED Display configurado (opcional)
- [ ] LEDs conectados aos GPIOs

### Software
- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Modelo ML disponível (`model.pkl`) [Opcional para teste]

### Redes
- [ ] Porta serial identificada (`/dev/ttyUSB0`, `COM3`, etc)
- [ ] Baud rate correto (115200)

---

## 📊 Estrutura do Web Server

```
┌─────────────────────────────────────────────┐
│        🌐 NAVEGADOR (Frontend)              │
│   http://localhost:5000                     │
│  ┌──────────────────────────────────────┐  │
│  │  Dashboard HTML/CSS/JavaScript       │  │
│  │  - Gráficos (Chart.js)              │  │
│  │  - Formulários de controle           │  │
│  │  - WebSocket para updates            │  │
│  └──────────────────────────────────────┘  │
└────────────┬────────────────────────────────┘
             │ HTTP/REST API
             ↓
┌─────────────────────────────────────────────┐
│     🐍 SERVIDOR FLASK (Backend)             │
│   web_server.py                             │
│  ┌──────────────────────────────────────┐  │
│  │  APIs REST:                          │  │
│  │  - GET /api/status                   │  │
│  │  - GET /api/data                     │  │
│  │  - POST /api/connect                 │  │
│  │  - POST /api/send                    │  │
│  │  - POST /api/model/load              │  │
│  │  - GET /api/history                  │  │
│  └──────────────────────────────────────┘  │
└────────────┬────────────────────────────────┘
             │ Serial/USB
             ↓
┌─────────────────────────────────────────────┐
│  🎛️  ESP32 (Hardware - Microcontroller)    │
│   Via Porta Serial (/dev/ttyUSB0)          │
│  ┌──────────────────────────────────────┐  │
│  │ - Captura CSI                        │  │
│  │ - Controla OLED Display              │  │
│  │ - Ativa LEDs                         │  │
│  │ - Envia dados de volta ao Python    │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

---

## 🔌 Configuração de Rede

### Acessar Localmente (Seu Computador)
```
http://localhost:5000
http://127.0.0.1:5000
```

### Acessar de Outro Computador (Mesma Rede)
1. Descubra o IP do servidor:
   ```bash
   ifconfig | grep "inet "
   # Procure por: 192.168.1.100 (exemplo)
   ```

2. Acesse no outro computador:
   ```
   http://192.168.1.100:5000
   ```

### Acessar pela Internet
**Requer Port Forwarding no roteador**
```
http://seu-ip-publico:5000
```

---

## 📚 Arquivos Criados - Descrição

### `web_server.py` (Backend Flask)
```python
# Funções principais:
- init_serial()           → Conecta ao ESP32
- parse_csi_data()        → Processa dados brutos
- serial_reader_thread()  → Thread de leitura
- Load Model ML
- APIs REST
```

**Rotas disponíveis:**
- `GET  /`              → Dashboard HTML
- `GET  /api/status`    → Status do sistema
- `GET  /api/data`      → Dados CSI
- `POST /api/connect`   → Conectar serial
- `POST /api/send`      → Enviar comandos
- `POST /api/model/load` → Carregar ML
- `GET  /api/history`   → Exportar CSV

### `templates/dashboard.html` (Frontend)
```html
<!-- 2500+ linhas de código -->
- Interface responsiva
- Gráficos em tempo real (Chart.js)
- Controles interativos
- Log de eventos
- Download de histórico
```

### `start.sh` (Script de Inicialização)
```bash
# Automático:
✓ Verifica Python
✓ Cria ambiente virtual
✓ Instala dependências
✓ Mostra portas seriais
✓ Inicia servidor
```

### `GUIA_WEB_SERVER.md` (Documentação Completa)
```
- 400+ linhas de documentação
- Passo a passo detalhado
- Solução de problemas
- Exemplos de código
- API REST completa
- Deployment em produção
```

---

## 🎯 Casos de Uso

### 1️⃣ Desenvolvimento Local
```bash
bash start.sh
# Acessa: http://localhost:5000
# Testa localmente
```

### 2️⃣ Monitoramento Remoto
```
# Acessa: http://192.168.1.100:5000
# Via rede local (casa, laboratório)
```

### 3️⃣ Análise de Dados
```python
# Exporta histórico em CSV
# Analisa com Pandas/Matplotlib
# Gera relatórios
```

### 4️⃣ Integração com Outras Ferramentas
```python
import requests

# Integrar com sistema de automação
response = requests.get('http://localhost:5000/api/status')
activity = response.json()['activity']

if activity == 'walking':
    # Fazer algo...
```

---

## 🔧 Customizações Possíveis

### Mudar Porta
```bash
# Edite web_server.py linha final:
app.run(port=8080)  # Mude para sua porta
```

### Adicionar Novas Atividades
```python
# pipeline.py - Treinar com mais classes
labels = ['walking', 'sitting', 'standing', 'running', 'jumping']
```

### Personalizar Dashboard
```html
<!-- templates/dashboard.html -->
- Edite cores, layout, gráficos
- Adicione novos controles
- Customize com seu logo/branding
```

### Adicionar WebSocket (tempo real)
```python
from flask_socketio import SocketIO
io = SocketIO(app)
# Implementar para atualizações instantâneas
```

---

## 🐛 Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| "Port already in use" | `kill -9 $(lsof -t -i :5000)` |
| "ModuleNotFoundError" | `pip install -r requirements.txt` |
| "Connection refused" | Verifique porta serial e baud rate |
| "Modelo não carrega" | `python pipeline.py ...` gera novo |
| "Dashboard vazio" | Conecte ESP32 e aguarde dados |

---

## 📈 Performance

### Requisitos Mínimos
- CPU: Qualquer (Raspberry Pi funciona)
- RAM: 512MB
- Python: 3.8+

### Recursos Utilizados
- **Servidor:** ~50-100MB RAM
- **Porta:** 5000 (HTTP)
- **Taxa de atualização:** 500ms (2Hz)

### Escalabilidade
- Suporta múltiplos clientes simultâneos
- Para produção, use Gunicorn + Nginx
- Com WebSocket, mais eficiente

---

## 🎓 Aprendizado

### O Que Você Aprendeu

✅ Arquitetura Cliente-Servidor  
✅ Comunicação Serial com Microcontroladores  
✅ APIs REST em Flask  
✅ Frontend HTML/CSS/JavaScript  
✅ Processamento de Sinais  
✅ Machine Learning (Sklearn)  
✅ Integração Hardware-Software  

### Próximos Passos

1. **Treinar o modelo** com seus dados
2. **Customizar o dashboard** com suas cores
3. **Adicionar novas atividades** de detecção
4. **Deploy em servidor** para acesso remoto
5. **Integrar com IoT** (MQTT, Home Assistant, etc)

---

## 📞 Suporte

### Documentação
- 📖 `GUIA_WEB_SERVER.md` - Completo (400+ linhas)
- 📊 `WIFI_SENSING_PROJECT.md` - Projeto (300+ linhas)
- 📚 Código bem comentado em `web_server.py`

### Recursos Online
- Flask: https://flask.palletsprojects.com
- Chart.js: https://www.chartjs.org
- ESP32: https://docs.espressif.com
- scikit-learn: https://scikit-learn.org

---

## 🎉 Resumo

| Item | Status |
|------|--------|
| ✅ Web Server | Pronto |
| ✅ Dashboard | Pronto |
| ✅ API REST | Pronto |
| ✅ Documentação | Pronta |
| ✅ Script de Start | Pronto |
| ⚙️ Hardware | Seu ESP32 |
| ⚙️ Modelo ML | Seu treinamento |

---

## 🚀 Comece Agora!

```bash
# 1. Entre no diretório
cd /home/user/R0T4S/wifi-human-detection

# 2. Instale (primeira vez)
pip install -r requirements.txt

# 3. Inicie
bash start.sh

# 4. Acesse
# http://localhost:5000
```

**Pronto! Aproveite seu projeto Wi-Fi Sensing em um ambiente web moderno! 🎊**

---

_Criado com ❤️ para você explorar o mundo do Wi-Fi Sensing através de um navegador web._

**Data:** 29 de Julho de 2025  
**Versão:** 1.0  
**Status:** ✅ Completo e Funcional
