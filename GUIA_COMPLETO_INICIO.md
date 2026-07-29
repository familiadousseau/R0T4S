# 🏠 Guia Completo: Sistema de Detecção de Presença em Casa

## Objetivo Final
**Ver pelo seu celular se há alguém em casa, mesmo que você esteja na rua.**

Você usa o WiFi como "câmera térmica" para detectar se há movimento dentro de casa.

---

## 📋 Pré-Requisitos

Você vai precisar de:

1. **ESP32** ou **placa similar com WiFi**
   - Custo: ~R$ 30-50
   - Onde comprar: AliExpress, Mercado Livre
   
2. **Raspberry Pi 4** ou **PC/Notebook em casa**
   - Vai rodar o servidor web
   - Pode ser qualquer máquina que fique ligada 24/7
   
3. **Cabo USB** para conectar ESP32 ao Raspberry/PC

4. **WiFi em casa** (que você já tem)

5. **Internet na rua** (qualquer WiFi ou dados móveis)

---

## ⚙️ PARTE 1: Preparar o ESP32

### Passo 1: Baixar o Firmware
1. Acesse: https://github.com/csqwerty/esp32-wifi-csi
2. Clique em **"Code"** → **"Download ZIP"**
3. Extraia a pasta

### Passo 2: Gravar o Firmware no ESP32
1. Baixe o programa **ESP32 Flash Tool**:
   - Windows: https://www.espressif.com/en/support/download/other-tools
   - Mac/Linux: Use `esptool.py`

2. Conecte o ESP32 ao PC com cabo USB

3. Abra o Flash Tool e:
   - Selecione a porta USB do ESP32 (ex: COM3 ou /dev/ttyUSB0)
   - Carregue o arquivo `.bin` do firmware
   - Clique "Start" e aguarde

4. Quando terminar, desconecte o ESP32

**Dica:** Se não souber qual é a porta, abra Gerenciador de Dispositivos (Windows) ou rode no terminal:
```bash
ls /dev/tty* | grep USB  # Linux/Mac
```

---

## ⚙️ PARTE 2: Configurar o Servidor em Casa

### Passo 1: Clonar o Projeto
Abra o terminal/prompt de comando em sua casa (no PC/Raspberry que vai ficar ligado):

```bash
# Vá até uma pasta (exemplo: Desktop)
cd ~/Desktop

# Clone o projeto
git clone https://github.com/familiadousseau/R0T4S.git

# Entre na pasta
cd R0T4S/wifi-human-detection
```

### Passo 2: Instalar as Dependências
```bash
# Instale o Python (se não tiver)
# Windows: https://www.python.org/downloads/
# Mac: brew install python3
# Linux: sudo apt install python3 python3-pip

# Instale as dependências do projeto
pip install -r requirements.txt
```

Se der erro, rode:
```bash
pip install flask flask-socketio python-socketio python-engineio numpy joblib pyserial
```

### Passo 3: Conectar o ESP32
1. Conecte o ESP32 ao PC/Raspberry com o cabo USB
2. Anote a **porta USB** que apareceu (ex: COM3, /dev/ttyUSB0)

### Passo 4: Iniciar o Servidor
```bash
# Entre na pasta do projeto
cd ~/Desktop/R0T4S/wifi-human-detection

# Inicie o servidor
python3 web_server_live.py
```

Você vai ver algo assim:
```
============================================================
🌐 Web Server Wi-Fi Sensing - Versão ao Vivo
============================================================

📍 Acesse no navegador:
   http://localhost:5000
   http://192.168.1.100:5000  (rede local)

📱 No celular (mesma rede):
   Abra: http://192.168.1.100:5000/thermal

🔌 Conexão Serial:
   Porta: /dev/ttyUSB0 (Linux/Mac) ou COM3 (Windows)
   Baud: 115200

============================================================
```

**IMPORTANTE:** Anote o IP que apareceu (ex: 192.168.1.100)

---

## 📱 PARTE 3: Acessar pelo Celular (Mesma Rede WiFi)

### Passo 1: Conecte seu Celular ao WiFi de Casa
1. Vá em **Configurações** → **WiFi**
2. Conecte ao WiFi da sua casa (o mesmo que o PC/Raspberry)

### Passo 2: Abra o Navegador
1. Abra o navegador do celular (Chrome, Safari, etc)
2. Na barra de endereço, digite:
   ```
   http://192.168.1.100:5000/thermal
   ```
   *(substitua 192.168.1.100 pelo IP que apareceu no terminal)*

3. Pressione Enter

### Passo 3: Configure a Conexão
1. Clique em **"🔌 CONECTAR"**
   - Aguarde aparecer: ✓ Serial conectado

2. Clique em **"🤖 CARREGAR"**
   - Aguarde aparecer: ✓ Modelo carregado

### Passo 4: Teste a Simulação
Clique nos botões:
- 🚶 = Simula alguém caminhando
- 🪑 = Simula alguém sentado
- 🧍 = Simula alguém de pé

A **câmera térmica** vai mostrar a silhueta de uma pessoa!

---

## 🌐 PARTE 4: Acessar de Fora de Casa (Via Internet)

### ⚠️ AVISO IMPORTANTE
Para acessar de fora de casa, você precisa "abrir a porta" do seu roteador. Isso é mais complexo.

### Opção 1: Usar uma VPN (MAIS SEGURO)
1. Instale uma VPN no celular (ExpressVPN, NordVPN, etc)
2. Conecte à VPN
3. Sua rede doméstica vai ficar "perto" mesmo estando longe
4. Acesse normalmente: http://192.168.1.100:5000/thermal

### Opção 2: Port Forwarding (MAIS TÉCNICO)
1. Acesse o painel do seu roteador:
   - Geralmente em: http://192.168.1.1
   - Usuário/Senha geralmente é: admin/admin

2. Procure por **"Port Forwarding"** ou **"Encaminhamento de Porta"**

3. Configure:
   - **Porta Externa**: 5000
   - **IP Interno**: 192.168.1.100
   - **Porta Interna**: 5000
   - **Protocolo**: TCP

4. Salve as configurações

5. Descubra seu IP externo:
   - Acesse: https://whatismyipaddress.com
   - Anote o IP público (ex: 123.45.67.89)

6. De fora de casa, acesse:
   ```
   http://123.45.67.89:5000/thermal
   ```

### Opção 3: Usar um Serviço de Tunelamento (MAIS FÁCIL)
1. Instale **ngrok**:
   ```bash
   # Windows: Download em https://ngrok.com/download
   # Mac: brew install ngrok
   # Linux: https://ngrok.com/download
   ```

2. Crie uma conta em: https://ngrok.com

3. Abra um terminal NEW (sem fechar o outro rodando o servidor) e rode:
   ```bash
   ngrok http 5000
   ```

4. Você vai ver algo assim:
   ```
   Forwarding    http://abc123def456.ngrok.io -> http://localhost:5000
   ```

5. De qualquer lugar, acesse:
   ```
   http://abc123def456.ngrok.io/thermal
   ```

---

## 🎮 Como Usar o Sistema

### Tela Principal
A câmera térmica mostra:
- **Silhueta vermelha/laranja** = pessoa perto (sinal forte)
- **Silhueta amarela** = pessoa a distância normal
- **Silhueta azul** = pessoa longe (sinal fraco)
- **Sem silhueta** = ninguém em casa

### Painel de Controle (Direita)
- **ATIVIDADE**: O que a pessoa está fazendo (walking/sitting/standing)
- **RSSI**: Força do sinal WiFi (quanto mais negativo, mais longe)
- **DISTÂNCIA**: Aproximadamente a que distância está
- **ESCALA TÉRMICA**: Mostra o que significa cada cor

### Botões de Teste
Se o ESP32 não conectou ainda:
- 🚶 Testa a visualização com alguém caminhando
- 🪑 Testa com alguém sentado
- 🧍 Testa com alguém de pé

---

## 🐛 Solução de Problemas

### ❌ "Não consigo conectar ao ESP32"
1. Verifique a porta USB:
   ```bash
   # Windows - abra Gerenciador de Dispositivos
   # Linux/Mac:
   ls /dev/tty*
   ```
2. Revise a porta em `web_server_live.py` linha 35:
   ```python
   SERIAL_PORT = '/dev/ttyUSB0'  # Mude se necessário
   ```

### ❌ "Não vejo nada na câmera térmica"
1. Verifique se o ESP32 está enviando dados
2. Mova a mão perto do ESP32
3. Clique em "🚶 Simular" para testar

### ❌ "O IP muda toda hora"
1. Configure um IP fixo para o PC/Raspberry:
   - Windows: Configurações → Rede → Propriedades → IP Estático
   - Linux: `nmtui` ou edite `/etc/network/interfaces`

### ❌ "Não consigo acessar de fora de casa"
1. Tente VPN primeiro (mais fácil)
2. Se usar Port Forwarding, verifique:
   - Roteador permite port forwarding?
   - Firewall do PC está bloqueando?
   - IP externo está correto?

### ❌ "Modelo ML não carrega"
1. Verifique se existe `model.pkl` na pasta
2. Se não existir, o sistema ainda funciona em modo de simulação
3. Você pode treinar um modelo depois

---

## 📊 Como Funciona (Para os Curiosos)

```
        [WiFi da Casa]
               ↓
        [ESP32 mede o sinal]
               ↓
     [Envia força do sinal via Serial]
               ↓
     [Servidor (PC/Raspberry) recebe]
               ↓
    [Processa e identifica atividade]
               ↓
    [Mostra na câmera térmica 3D]
               ↓
    [Seu celular acessa via navegador]
```

---

## 🚀 Próximos Passos (Opcional)

Depois que tudo funcionar:

1. **Treinar o Modelo ML**:
   - Colete dados com o ESP32
   - Use scikit-learn para treinar
   - Salve como `model.pkl`

2. **Automação**:
   - Receba notificações quando detecta alguém
   - Integre com Google Home/Alexa

3. **Banco de Dados**:
   - Guarde histórico de quem entrou/saiu
   - Faça gráficos de uso

---

## 📞 Dúvidas Comuns

**P: Quanto custa tudo?**
R: ~R$ 50-100 (ESP32 + cabos)

**P: Preciso de PC/Raspberry caro?**
R: Não! Um Raspberry Pi Zero (~R$ 30) funciona.

**P: Funciona com WiFi 5G?**
R: Sim, mas o 2.4GHz é mais confiável para Wi-Fi sensing.

**P: Meu vizinho consegue espionar?**
R: Com VPN não. Com Port Forwarding, use senha forte.

**P: Posso deixar rodando 24/7?**
R: Sim! Consome pouca energia (< 10W no Raspberry Pi).

---

## ✅ Checklist de Sucesso

- [ ] ESP32 está conectado ao PC/Raspberry
- [ ] Servidor rodando no terminal: "✓ Servidor iniciado!"
- [ ] Consegui acessar pelo celular: http://192.168.X.X:5000/thermal
- [ ] Vi a câmera térmica funcionando
- [ ] Cliquei em "🚶 Simular" e vi a silhueta se mover
- [ ] Consegui acessar de fora de casa (VPN ou ngrok)

---

**Criado com ❤️ para detectar presença em casa**

Versão: 1.0  
Data: 29 de Julho de 2025  
Status: ✅ Pronto para usar

**Precisa de ajuda? Releia este guia do início! 90% dos problemas são resolvidos aqui.**
