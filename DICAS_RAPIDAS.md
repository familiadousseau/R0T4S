# ⚡ Dicas Rápidas

## 🚀 Iniciar em 3 Passos

### Passo 1: Conectar ESP32 e Abrir Terminal
```bash
# Vá até a pasta do projeto
cd ~/Desktop/R0T4S/wifi-human-detection

# Veja qual porta USB o ESP32 está usando
ls /dev/tty*  # Linux/Mac
# ou abra Gerenciador de Dispositivos (Windows)
```

### Passo 2: Iniciar o Servidor
```bash
python3 web_server_live.py
```

Você vai ver:
```
🌐 IP Local: 192.168.1.100
✓ Servidor iniciado!
```

### Passo 3: Abrir no Celular
1. Conecte o celular ao WiFi de casa
2. Abra o navegador
3. Digite: **http://192.168.1.100:5000/thermal**
4. Pronto! 🔥

---

## 📱 Pelo Celular: 4 Cliques

1. **Clique em "🔌 CONECTAR"** → Aguarde "✓ Serial conectado"
2. **Clique em "🤖 CARREGAR"** → Aguarde "✓ Modelo carregado"
3. **Veja a câmera térmica** → Silhueta = pessoa em casa
4. **Para testar**: Clique em 🚶 ou 🪑 ou 🧍

---

## 🔧 Mudando a Porta USB

Se o ESP32 não conectar:

**Editar arquivo `web_server_live.py`:**

Procure por:
```python
SERIAL_PORT = '/dev/ttyUSB0'
```

Mude para a porta correta:
- Windows: `COM3` (abra Gerenciador de Dispositivos)
- Mac: `/dev/tty.usbserial-xxxxx`
- Linux: `ls /dev/tty*`

Depois:
```bash
python3 web_server_live.py
```

---

## 🌐 Acessar de Fora de Casa

### Opção 1: VPN (FÁCIL)
1. Instale VPN no celular (ExpressVPN, etc)
2. Conecte à VPN
3. Acesse: http://192.168.1.100:5000/thermal

### Opção 2: ngrok (SEM CONFIGURAR ROTEADOR)
```bash
# Terminal NEW (não feche o servidor!)
ngrok http 5000

# Você vai ver:
# http://abc123def456.ngrok.io/thermal

# Use esse link de qualquer lugar!
```

### Opção 3: Port Forwarding (Técnico)
1. Acesse: http://192.168.1.1 (seu roteador)
2. Procure "Port Forwarding"
3. Configure:
   - Porta Externa: 5000
   - IP Interno: 192.168.1.100
   - Porta Interna: 5000
4. Descubra seu IP externo: https://whatismyipaddress.com
5. Acesse: http://SEUIP:5000/thermal

---

## 📊 Entendendo as Cores

| Cor | Significado | Distância |
|-----|-------------|-----------|
| 🔴 Vermelho | Pessoa MUITO perto | < 1m |
| 🟠 Laranja | Pessoa perto | 1-3m |
| 🟡 Amarelo | Pessoa distância normal | 3-5m |
| 🟢 Verde | Pessoa longe | 5-10m |
| 🔵 Azul | Pessoa MUITO longe | 10m+ |

---

## 🎮 Botões de Teste

**Antes de tudo estar conectado, teste clicando:**

- 🚶 = Simula movimento (caminhando)
- 🪑 = Simula parado (sentado)
- 🧍 = Simula em pé

A câmera térmica vai mostrar a silhueta mesmo sem ESP32!

---

## ❌ Erros Comuns

### "Porta /dev/ttyUSB0 não encontrada"
```bash
# Descubra qual é a porta certa:
ls /dev/tty*

# Depois edite web_server_live.py linha 35
# e coloque a porta correta
```

### "Não consigo acessar de fora de casa"
1. Tente VPN primeiro (mais fácil)
2. Se não funcionar, use ngrok
3. Port Forwarding é o último recurso

### "O servidor fecha quando fecho o terminal"
Use `screen` ou `tmux`:
```bash
screen -S wifi-sensing
python3 web_server_live.py

# Para desconectar: Ctrl+A depois D
# Para reconectar: screen -r wifi-sensing
```

### "A câmera térmica não mostra nada"
1. Verifique se "✓ Serial conectado" apareceu
2. Clique em "🚶 Simular" para testar
3. Mova a mão perto do ESP32

---

## 🎯 Checklist Rápido

```
⬜ ESP32 conectado ao PC via USB
⬜ Terminal: python3 web_server_live.py
⬜ Celular conectado ao WiFi de casa
⬜ Acessei: http://192.168.X.X:5000/thermal
⬜ Cliquei "🔌 CONECTAR"
⬜ Cliquei "🤖 CARREGAR"
⬜ Vi a câmera térmica 3D funcionando
⬜ Testei com 🚶 Simular
⬜ Consegui acessar de fora de casa
```

---

## 📞 Mensagens do Sistema

| Mensagem | Significa |
|----------|-----------|
| ✓ Serial conectado | ESP32 está plugado e respondendo |
| ✓ Modelo carregado | AI está pronta para detectar |
| 📊 WALKING | Detectou alguém caminhando |
| 📊 SITTING | Detectou alguém sentado |
| 📊 STANDING | Detectou alguém em pé |
| ✗ Serial desconectado | ESP32 não está respondendo |

---

## 💡 Pro Tips

1. **IP Fixo**: Configure IP fixo no PC/Raspberry para não mudar todo dia

2. **Iniciar automaticamente**: Use `cron` (Linux):
   ```bash
   crontab -e
   # Adicione:
   @reboot cd /home/user/R0T4S/wifi-human-detection && python3 web_server_live.py &
   ```

3. **Log de acesso**: Todos os acessos ficam salvos no terminal

4. **Testar em localhost**: http://localhost:5000/thermal

5. **Usar HTTPS**: Se expor na internet, configure SSL/TLS

---

**Mais dúvidas? Leia `GUIA_COMPLETO_INICIO.md`**
