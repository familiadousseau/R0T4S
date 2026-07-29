# 📱 Comandos SSH Para Copiar/Colar no iPhone

## Como Usar Este Arquivo

1. Abra **Terminus** app no iPhone
2. Conecte ao Raspberry Pi (IP: 192.168.1.50, user: pi, pass: raspberry)
3. **COPIE E COLE** cada comando abaixo, UM POR VEZ
4. Aguarde terminar (aparece `pi@raspberrypi`), depois do próximo

---

## 🔧 PARTE 1: Preparação Inicial

### 1. Atualizar o Sistema
```bash
sudo apt update && sudo apt upgrade -y
```
⏳ Pode demorar 5-10 minutos. Seja paciente!

### 2. Instalar Ferramentas Necessárias
```bash
sudo apt install -y python3 python3-pip git wget curl
```

### 3. Instalar Screen (Para deixar rodando 24/7)
```bash
sudo apt install -y screen
```

---

## 📦 PARTE 2: Clonar o Projeto

### 1. Ir para a Pasta Home
```bash
cd ~
```

### 2. Clonar o Repositório
```bash
git clone https://github.com/familiadousseau/R0T4S.git
```

### 3. Entrar na Pasta
```bash
cd R0T4S/wifi-human-detection
```

### 4. Verificar se Entrou Certo
```bash
pwd
```
Deve aparecer: `/home/pi/R0T4S/wifi-human-detection`

---

## ⚙️ PARTE 3: Instalar Dependências

### 1. Instalar Dependências Python
```bash
pip3 install -r requirements.txt
```
⏳ Pode demorar 5-10 minutos. Deixe terminar!

### 2. Verificar Se Funcionou
```bash
python3 -c "import flask; import flask_socketio; print('✓ OK!')"
```
Deve aparecer: `✓ OK!`

---

## 🚀 PARTE 4: Deixar Rodando 24/7

### 1. Criar uma Sessão Screen
```bash
screen -S wifi
```
*A tela muda! Isso é normal!*

### 2. Iniciar o Servidor
```bash
python3 web_server_live.py
```

**Você vai ver:**
```
🌐 Web Server Wi-Fi Sensing
📍 Acesse: http://192.168.1.50:5000
```

### 3. SAIR SEM PARAR O SERVIDOR
```
Pressione: Ctrl + A
Depois: D
```
(Não é Ctrl + D!)

**Você voltou ao terminal normal!** ✓ O servidor continua rodando!

---

## 📱 PARTE 5: Testar Pelo iPhone

### 1. Abrir Safari
- Toque no ícone do Safari

### 2. Digitar o Endereço
```
http://192.168.1.50:5000/thermal
```

### 3. Clicar em "🔌 CONECTAR"
- Aguarde aparecer "✓ Serial conectado"

### 4. Clicar em "🤖 CARREGAR"
- Aguarde aparecer "✓ Modelo carregado"

### 5. Ver a Câmera Térmica!
- A silhueta vai aparecer
- Teste com 🚶 🪑 🧍

---

## 🌐 PARTE 6: Acessar de Fora de Casa (ngrok)

### 1. Reconectar ao Servidor (Se Saiu)
```bash
screen -r wifi
```

### 2. Instalar ngrok
```bash
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo apt-key add -
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update
sudo apt install -y ngrok
```

### 3. Configurar ngrok
Vá em https://dashboard.ngrok.com/ e pegue seu token, depois:
```bash
ngrok config add-authtoken SEU_TOKEN_AQUI
```
*(Substitua SEU_TOKEN_AQUI pelo token real)*

### 4. Sair da Sessão Screen
```
Ctrl + A
D
```

### 5. Criar Nova Sessão para ngrok
```bash
screen -S ngrok
```

### 6. Iniciar ngrok
```bash
ngrok http 5000
```

**Você vai ver algo assim:**
```
Forwarding    http://abc123def456.ngrok.io -> http://localhost:5000
```

**COPIE ESSE LINK!** (abc123def456.ngrok.io)

---

## 📋 Comandos Úteis

### Ver Todas as Sessões Screen
```bash
screen -ls
```
Mostra: `wifi` (rodando), `ngrok` (rodando), etc

### Voltar ao Servidor
```bash
screen -r wifi
```

### Ver Logs do Servidor
```bash
screen -r wifi
# Scroll up com dois dedos para ver histórico
```

### Parar o Servidor
```bash
screen -r wifi
# Pressione: Ctrl + C
```

### Reiniciar o Servidor
```bash
screen -r wifi
# Ctrl + C
# python3 web_server_live.py
# Ctrl + A, D
```

### Mudar a Porta USB (Se Necessário)
```bash
nano web_server_live.py
# Procure: SERIAL_PORT = '/dev/ttyUSB0'
# Mude se necessário
# Ctrl + X, Y, Enter para salvar
```

### Ver IP do Raspberry Pi
```bash
hostname -I
```

### Ver Espaço em Disco
```bash
df -h
```

### Reiniciar o Raspberry Pi
```bash
sudo reboot
```

### Desligar o Raspberry Pi
```bash
sudo poweroff
```

---

## 🔐 Segurança Básica

### Mudar Senha do Usuário Pi
```bash
passwd
```
Digite a senha nova 2 vezes

### Ver Processos Rodando
```bash
ps aux | grep python
```

### Matar um Processo
```bash
kill -9 NUMERO_DO_PROCESSO
```

---

## 🆘 Solução de Problemas

### "Comando não encontrado"
- Verifique a digitação
- **Melhor:** Copie e cole em vez de digitar

### "Permissão negada"
- Coloque `sudo` no começo:
```bash
sudo apt install algo
```

### "Conexão recusada"
- O servidor não está rodando
- Crie uma sessão screen: `screen -S wifi`
- Inicie: `python3 web_server_live.py`

### "Arquivo não encontrado"
- Verifique se está na pasta correta:
```bash
pwd
# Deve mostrar: /home/pi/R0T4S/wifi-human-detection
```

### "Screen não funciona"
- Instale de novo:
```bash
sudo apt install -y screen
```

---

## ✅ Checklist de Sucesso

```bash
# Execute estes comandos para verificar:

# 1. Python instalado?
python3 --version

# 2. Flask instalado?
python3 -c "import flask; print('✓ Flask OK')"

# 3. Projeto clonado?
ls ~/R0T4S/wifi-human-detection/web_server_live.py

# 4. Screen instalado?
screen --version

# 5. Servidor pode rodar?
cd ~/R0T4S/wifi-human-detection && python3 web_server_live.py &
sleep 2
curl http://localhost:5000/api/status
```

Se tudo mostrar "✓ OK", está pronto!

---

## 📞 Ordem Correta Para Iniciar Tudo

1. Ligar o Raspberry Pi
2. Conectar ESP32 ao Raspberry Pi
3. Esperar 30 segundos para tudo carregar
4. Conectar via SSH (Terminus)
5. Criar screen: `screen -S wifi`
6. Iniciar servidor: `python3 web_server_live.py`
7. Sair: `Ctrl + A`, `D`
8. Abrir Safari no iPhone
9. Digitar: `http://192.168.1.50:5000/thermal`
10. Clique "🔌 CONECTAR" e "🤖 CARREGAR"
11. Pronto!

---

## 🎓 Para Entender Melhor

- `sudo` = Executar como administrador
- `apt` = Gerenciador de pacotes
- `pip3` = Instalador de pacotes Python
- `cd` = Mudar pasta
- `pwd` = Ver pasta atual
- `ls` = Listar arquivos
- `screen` = Executar em background
- `Ctrl + C` = Parar o programa
- `Ctrl + A, D` = Sair do screen SEM PARAR

---

**Copie e cole! Você consegue! 💪**
