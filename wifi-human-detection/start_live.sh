#!/bin/bash

# 🚀 Script de Inicialização - Web Server ao Vivo
# Uso: bash start_live.sh

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║     🌐 WiFi CSI Human Activity Detection                   ║"
echo "║     Versão ao Vivo com WebSocket                           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. Verificar Python
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "${BLUE}📌 Verificando Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 não encontrado${NC}"
    echo "  Instale com: sudo apt-get install python3 python3-pip"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python ${PYTHON_VERSION}${NC}"
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. Criar/Ativar Ambiente Virtual
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "${BLUE}📌 Ambiente Virtual...${NC}"
if [ ! -d "venv" ]; then
    echo "  Criando ambiente virtual..."
    python3 -m venv venv
fi
source venv/bin/activate
echo -e "${GREEN}✓ Ativado${NC}"
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. Instalar Dependências
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "${BLUE}📌 Instalando dependências...${NC}"
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}✗ requirements.txt não encontrado!${NC}"
    exit 1
fi
pip install -q -r requirements.txt 2>/dev/null
echo -e "${GREEN}✓ Dependências instaladas${NC}"
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. Descobrir IP Local
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "${BLUE}📌 Descobrindo IP local...${NC}"
LOCAL_IP=$(python3 -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(('8.8.8.8', 80)); print(s.getsockname()[0]); s.close()" 2>/dev/null || echo "127.0.0.1")
echo -e "${GREEN}✓ IP: ${LOCAL_IP}${NC}"
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. Portas Seriais
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "${BLUE}📌 Portas Seriais Disponíveis:${NC}"
if ls /dev/tty* 2>/dev/null | grep -E "USB|ACM" > /dev/null; then
    ls /dev/tty* 2>/dev/null | grep -E "USB|ACM" | sed 's/^/  ✓ /'
else
    echo "  ⚠️  Nenhuma encontrada (conecte o ESP32)"
fi
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. Verificar Modelo ML
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo -e "${BLUE}📌 Verificando Modelo ML...${NC}"
if [ -f "model.pkl" ]; then
    SIZE=$(ls -lh model.pkl | awk '{print $5}')
    echo -e "${GREEN}✓ model.pkl encontrado (${SIZE})${NC}"
else
    echo -e "${YELLOW}⚠️  model.pkl não encontrado${NC}"
    echo "  Você pode carregar pelo dashboard"
fi
echo ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. Iniciar Servidor
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

clear

cat << "EOF"

╔════════════════════════════════════════════════════════════╗
║          🌐 SERVIDOR AO VIVO INICIADO! 🌐                 ║
╚════════════════════════════════════════════════════════════╝

📍 ACESSE NO NAVEGADOR:

   💻 Computador Local:
      http://localhost:5000

   📱 Celular (Mesma Rede WiFi):
      http://192.168.X.X:5000

   🖥️  Outro Computador (Mesma Rede):
      http://OUTRO-IP:5000

EOF

echo -e "   ${GREEN}IP Local: ${LOCAL_IP}:5000${NC}"
echo ""

cat << "EOF"
🔌 CONEXÃO SERIAL:
   Porta: /dev/ttyUSB0 (Linux/Mac) ou COM3 (Windows)
   Baud: 115200

💡 DICAS:
   1. Conecte o ESP32 via USB
   2. Abra http://192.168.X.X:5000 no navegador
   3. Clique em "Conectar"
   4. Carregue o modelo ML
   5. Veja os dados em tempo real!

❌ PARA PARAR: Pressione CTRL+C

╔════════════════════════════════════════════════════════════╗

EOF

# Iniciar o servidor
cd "$(dirname "${BASH_SOURCE[0]}")"
python3 web_server_live.py
