#!/bin/bash

# Script de inicialização rápida do Web Server
# Uso: bash start.sh [porta]

PORTA=${1:-5000}
DIRETORIO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 ════════════════════════════════════════════════════════════"
echo "   Wi-Fi CSI Human Activity Detection - Web Server"
echo "🚀 ════════════════════════════════════════════════════════════"
echo ""

# Verificar Python
echo "📌 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale com:"
    echo "   sudo apt-get install python3 python3-pip"
    exit 1
fi
echo "✓ Python $(python3 --version | cut -d' ' -f2)"
echo ""

# Verificar dependências
echo "📌 Verificando dependências..."
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

echo "📦 Ativando ambiente virtual..."
source venv/bin/activate

echo "📦 Instalando/atualizando dependências..."
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt não encontrado!"
    exit 1
fi
pip install -q -r requirements.txt
echo "✓ Dependências instaladas"
echo ""

# Verificar modelo
echo "📌 Verificando modelo ML..."
if [ ! -f "model.pkl" ]; then
    echo "⚠️  Modelo não encontrado (model.pkl)"
    echo "   Você pode carregar pelo web interface ou:"
    echo "   python pipeline.py --data-dir ./data --output model.pkl"
fi
echo ""

# Detectar portas serial disponíveis
echo "📌 Portas seriais disponíveis:"
if [ -d "/dev" ]; then
    ls -la /dev/tty* 2>/dev/null | grep -E "(USB|ACM)" || echo "   Nenhuma encontrada (conecte o ESP32)"
fi
echo ""

# Iniciar servidor
echo "🌐 ════════════════════════════════════════════════════════════"
echo "   Iniciando Web Server na porta ${PORTA}..."
echo "🌐 ════════════════════════════════════════════════════════════"
echo ""
echo "📍 Acesse:"
echo "   http://localhost:${PORTA}"
echo ""
echo "🔌 Conexão Serial:"
echo "   Porta: /dev/ttyUSB0 (Linux/Mac) ou COM3 (Windows)"
echo "   Baud: 115200"
echo ""
echo "💡 Dicas:"
echo "   - Conecte o ESP32 antes de acessar o dashboard"
echo "   - Carregue o modelo ML no dashboard"
echo "   - Verifique o log de eventos para erros"
echo ""
echo "❌ Para parar: Pressione CTRL+C"
echo "🌐 ════════════════════════════════════════════════════════════"
echo ""

# Executar servidor
cd "$DIRETORIO"
python3 web_server.py --port $PORTA
