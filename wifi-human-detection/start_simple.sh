#!/bin/bash

# 🔥 Script de Início Rápido - WiFi Sensing
# Execute este arquivo para iniciar o servidor automaticamente

echo "════════════════════════════════════════════════════════"
echo "🏠 Sistema de Detecção de Presença em Casa"
echo "════════════════════════════════════════════════════════"
echo ""

# Verificar se Python3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não está instalado"
    echo "Instale em: https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Python3 encontrado"

# Verificar se está na pasta correta
if [ ! -f "web_server_live.py" ]; then
    echo "❌ Erro: Execute este script dentro da pasta 'wifi-human-detection'"
    echo "Comando correto:"
    echo "  cd ~/Desktop/R0T4S/wifi-human-detection"
    echo "  bash start_simple.sh"
    exit 1
fi

echo "✓ Pasta correta detectada"
echo ""

# Instalar dependências se necessário
echo "📦 Verificando dependências..."
pip3 install -q flask flask-socketio python-socketio python-engineio numpy joblib pyserial 2>/dev/null

echo "✓ Dependências instaladas"
echo ""

# Detectar IP local
IP=$(hostname -I | awk '{print $1}')
if [ -z "$IP" ]; then
    IP="192.168.X.X"
fi

echo "════════════════════════════════════════════════════════"
echo "🌐 SERVIDOR INICIADO!"
echo "════════════════════════════════════════════════════════"
echo ""
echo "📱 Acesse pelo CELULAR:"
echo "   Conecte ao WiFi de casa"
echo "   Abra o navegador e digite:"
echo ""
echo "   http://$IP:5000/thermal"
echo ""
echo "💻 Ou acesse pelo computador:"
echo "   http://localhost:5000/thermal"
echo ""
echo "════════════════════════════════════════════════════════"
echo ""
echo "🔧 Configuração:"
echo "   Porta USB: /dev/ttyUSB0 (você pode mudar em config.txt)"
echo "   Velocidade: 115200 baud"
echo ""
echo "⚡ Pressione Ctrl+C para parar o servidor"
echo ""
echo "════════════════════════════════════════════════════════"
echo ""

# Iniciar servidor
python3 web_server_live.py
