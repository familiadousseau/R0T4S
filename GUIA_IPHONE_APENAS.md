# 📱 Guia Completo: APENAS iPhone (Sem Notebook)

## ⚠️ Realidade Importante

**iPhone SOZINHO não consegue:**
- ❌ Conectar ao ESP32 via USB
- ❌ Rodar Python/servidor web
- ❌ Ficar 24/7 rodando em background

**MAS você precisa de ALGO em casa que fique ligado 24/7:**
- Raspberry Pi Zero (R$ 30-50)
- Raspberry Pi 4 (R$ 150-200)
- Velho PC/Notebook com Linux
- Mac Mini ou iMac já que você tem iPhone

**Bom é que você configura e acessa TUDO pelo iPhone!**

---

## 🎯 Solução: Raspberry Pi + iPhone

```
[ESP32] ←→ [Raspberry Pi 24/7] ←→ [Seu iPhone em qualquer lugar]
            (em casa, ligado)    (via ngrok/VPN)
```

---

## 🛒 O Que Comprar

| Item | Preço | Onde |
|------|-------|------|
| **Raspberry Pi Zero W** | R$ 30-50 | AliExpress, Mercado Livre |
| **Cartão SD 32GB** | R$ 20-30 | Amazon, Mercado Livre |
| **Cabo USB Type-A para Micro-USB** | R$ 5-15 | Qualquer loja |
| **Fonte USB 5V 2A** | R$ 15-25 | Qualquer loja |
| **Adaptador HDMI (opcional)** | R$ 20-40 | Qualquer loja |
| **ESP32** | R$ 30-50 | AliExpress, Mercado Livre |
| **Cabo USB para ESP32** | R$ 5-10 | AliExpress |

**Total mínimo: R$ 100-150** (sem contar internet)

---

## 🚀 PARTE 1: Preparar o Raspberry Pi Zero W

### Passo 1: Baixar o SO (Sistema Operacional)

1. Acesse pelo iPhone:
   https://www.raspberrypi.com/software/

2. Baixe **Raspberry Pi OS Lite** (versão de linha de comando)
   - Mais leve, perfeito para Raspberry Pi Zero

### Passo 2: Gravar no Cartão SD

Você precisa de outro computador ou pedir ajuda para:
1. Baixar **Balena Etcher**: https://www.balena.io/etcher/
2. Gravar a imagem do Raspberry Pi no cartão SD
3. Depois devolve o cartão

*Alternativa: Compre o cartão já com o SO (mais caro)*

### Passo 3: Montar o Raspberry Pi Zero

```
Cartão SD → Slot SD do Raspberry Pi Zero
Cabo USB → Porta USB do Raspberry Pi
Fonte USB → Tomada elétrica (deixa ligado 24/7)
```

### Passo 4: Conectar à Internet (Importante!)

O **Raspberry Pi Zero W TEM WiFi integrado**, mas precisa configurar pelo menos UMA VEZ.

**Opção A: Pedir emprestado um teclado/mouse/monitor**
1. Conectar teclado USB (adaptador)
2. Conectar monitor HDMI (adaptador)
3. Usar login: pi / raspberry
4. Configurar WiFi com:
   ```bash
   sudo raspi-config
   # Ir em: Network → WiFi → Entrar SSID e Senha
   ```

**Opção B: Criar arquivo config pelo computador**
1. No computador, após gravar o cartão SD:
   - Abrir a pasta `boot` do cartão
   - Criar arquivo `wpa_supplicant.conf`:
   ```
   ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
   update_config=1
   country=BR

   network={
       ssid="NOME_DO_SEU_WIFI"
       psk="SENHA_DO_SEU_WIFI"
   }
   ```
   - Salvar no cartão
   - Ejetar cartão

2. Colocar cartão no Raspberry Pi
3. Conectar o Raspberry Pi à tomada
4. **PRONTO!** Ele vai conectar ao WiFi sozinho

---

## ⚙️ PARTE 2: Instalar o Servidor (Pelo iPhone via SSH)

### Passo 1: Descobrir o IP do Raspberry Pi

No seu iPhone:
1. Abra o **app Home** (já vem no iPhone)
2. Vá em **Configurações** → **WiFi**
3. Toque no WiFi conectado
4. Role até o final, procure **Roteador**
5. Abra configurações do roteador
6. Procure por **Dispositivos Conectados**
7. Procure por um nome começando com **"raspberrypi"**
8. **Anote o IP** (ex: 192.168.1.50)

*Alternativa: Conecte o Raspberry Pi a um monitor pela primeira vez e rode:*
```bash
hostname -I
```

### Passo 2: Baixar um App SSH no iPhone

1. Abra a **App Store**
2. Procure por: **"Terminus"** ou **"SSH Files"**
3. Baixe gratuitamente

### Passo 3: Conectar ao Raspberry Pi

No app Terminus/SSH Files:

1. Clique em **"New Connection"** ou **"+"**
2. Preencha:
   - **Host**: 192.168.1.50 (o IP que anotou)
   - **User**: pi
   - **Password**: raspberry
   - **Port**: 22

3. Toque em **"Connect"**

Você vai estar **CONECTADO AO RASPBERRY PI PELO iPhone!**

### Passo 4: Instalar o Projeto

Cole estes comandos no SSH (um por vez):

```bash
# Atualizar sistema
sudo apt update
sudo apt upgrade -y

# Instalar Python
sudo apt install -y python3 python3-pip

# Clonar o projeto
cd ~
git clone https://github.com/familiadousseau/R0T4S.git

# Entrar na pasta
cd R0T4S/wifi-human-detection

# Instalar dependências
pip3 install -r requirements.txt
```

### Passo 5: Deixar Rodando 24/7

O servidor precisa ficar rodando MESMO QUE você desconecte o SSH.

Use **screen** (mantém rodando em background):

```bash
# Instalar screen
sudo apt install -y screen

# Criar uma sessão chamada "wifi"
screen -S wifi

# Dentro do screen, rode o servidor
python3 web_server_live.py

# Para sair SEM PARAR O SERVIDOR:
# Pressione: Ctrl + A, depois D

# Para voltar depois:
# screen -r wifi
```

**PRONTO! O servidor está rodando 24/7 em casa!**

---

## 📱 PARTE 3: Acessar Pelo iPhone (Em Casa)

### Descobrir o IP do Raspberry Pi
```bash
# No terminal SSH do iPhone:
hostname -I

# Vai mostrar algo como: 192.168.1.50
```

### Abrir no Safari do iPhone

1. Abra o **Safari**
2. Digite: `http://192.168.1.50:5000/thermal`
3. **PRONTO!** A câmera térmica aparece!

### Configurar

1. Clique em **"🔌 CONECTAR"** → Aguarde "✓ Serial conectado"
2. Clique em **"🤖 CARREGAR"** → Aguarde "✓ Modelo carregado"
3. **PRONTO!** Veja a silhueta térmica!

---

## 🌐 PARTE 4: Acessar de FORA de Casa (Pelo iPhone)

Você está na rua, quer ver se há alguém em casa.

### Opção 1: VPN (MAIS SEGURO)

**Instale uma VPN no iPhone:**
1. App Store
2. Procure: "ExpressVPN", "NordVPN", "ProtonVPN"
3. Baixe a versão gratuita (ou pague)
4. Configure com a conta

**Para usar:**
1. Conecte a VPN (no iPhone)
2. Abra o Safari
3. Digite: `http://192.168.1.50:5000/thermal`
4. **PRONTO!** Está vendo a casa!

### Opção 2: ngrok (GRÁTIS, SEM CONFIGURAÇÃO)

**No iPhone (via SSH):**

```bash
# Conecte ao Raspberry Pi pelo Terminus

# Instale ngrok
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo apt-key add -
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update
sudo apt install ngrok

# Configure ngrok
ngrok config add-authtoken SEU_TOKEN_AQUI
# (Pegue o token em: https://dashboard.ngrok.com/)

# Abra o servidor em um screen NOVO
screen -S ngrok

# Rode ngrok
ngrok http 5000

# Vai aparecer algo assim:
# Forwarding    http://abc123def456.ngrok.io -> http://localhost:5000

# COPIE ESSE LINK!
```

**Para usar de qualquer lugar:**
1. Abra o Safari no iPhone
2. Digite: `http://abc123def456.ngrok.io/thermal`
3. **PRONTO!** Acesso de qualquer lugar!

---

## ⚙️ CONFIGURAÇÃO DO SERVIDOR

Se precisar mudar porta ou outros ajustes:

**Via SSH no iPhone:**

```bash
# Editar arquivo de configuração
nano web_server_live.py

# Procure por "SERIAL_PORT" e "BAUD_RATE"
# Mude se necessário
# Para salvar: Ctrl + X, depois Y, depois Enter
```

---

## 🎮 TESTE RÁPIDO (SEM ESP32)

No Safari:
1. Acesse: `http://192.168.1.50:5000/thermal`
2. Clique em 🚶 🪑 🧍
3. A câmera térmica vai mostrar a silhueta

---

## 📊 Checklist Completo

**Hardware:**
- ☐ Raspberry Pi Zero W comprado/recebido
- ☐ Cartão SD preparado com o SO
- ☐ Conectado à tomada
- ☐ Conectado ao WiFi de casa

**Software (via SSH do iPhone):**
- ☐ Conectado via SSH (Terminus app)
- ☐ Instalou Python
- ☐ Clonou o repositório
- ☐ Instalou dependências
- ☐ Servidor rodando em screen

**Acesso pelo iPhone (Em Casa):**
- ☐ Descobri o IP do Raspberry Pi
- ☐ Consegui acessar: http://IP:5000/thermal
- ☐ Cliquei "🔌 CONECTAR"
- ☐ Cliquei "🤖 CARREGAR"
- ☐ Vi a câmera térmica funcionando
- ☐ Testei com 🚶 Simular

**Acesso Remoto (Fora de Casa):**
- ☐ Instalei VPN ou ngrok
- ☐ Consegui acessar de fora de casa
- ☐ Consigo ver a silhueta térmica da rua

---

## 📱 Apps Essenciais para iPhone

1. **Terminus** - SSH para conectar ao Raspberry Pi
   - Disponível na App Store
   - Grátis com compra opcional

2. **Safari** - Já vem no iPhone
   - Use para acessar a câmera térmica

3. **VPN** (opcional) - Para acessar de fora
   - ExpressVPN, NordVPN, ProtonVPN

4. **Notes** - Para anotar senhas/IPs
   - Já vem no iPhone

---

## 💡 DICAS IMPORTANTES

1. **Deixe tudo ligado 24/7:**
   - Raspberry Pi na tomada
   - WiFi ativo
   - Servidor rodando em screen

2. **Senha do Raspberry Pi:**
   - Usuário: `pi`
   - Senha padrão: `raspberry`
   - **MUDE DEPOIS:** `passwd`

3. **Se perder a conexão SSH:**
   - Reconecte pelo Terminus
   - O servidor continua rodando (está em screen)

4. **Para ver se está rodando:**
   ```bash
   screen -ls
   # Vai mostrar as sessões ativas (deve ter "wifi")
   ```

5. **Para parar o servidor:**
   ```bash
   screen -r wifi
   # Pressione: Ctrl + C
   ```

---

## 🚨 PROBLEMAS COMUNS

### ❌ "Não consigo conectar ao Raspberry Pi via SSH"
- Verifique se o IP está correto
- Verifique se o Raspberry Pi está no WiFi
- Reinicie o Raspberry Pi
- Tente novamente

### ❌ "Digitei o comando e aparece erro"
- Verifique se digitou exatamente igual
- Copie/cole em vez de digitar
- Aguarde cada comando terminar antes do próximo

### ❌ "Não aparece a câmera térmica"
- Verifique: http://IP:5000/thermal (e não só :5000)
- Recarregue a página (Ctrl + R no Safari)
- Teste com 🚶 Simular

### ❌ "Quer uma senha e eu não sei"
- Usuário: `pi`
- Senha: `raspberry`
- Se mudou, use a senha que configurou

### ❌ "Perdi a conexão SSH"
- Reconnecte pelo Terminus
- O servidor continua rodando!
- Digite: `screen -r wifi` para voltar ao servidor

---

## 🎓 Aprendendo Mais

Se quiser entender como funciona:

1. **SSH**: É como uma linha de comando remota
   - Você digita comandos no iPhone
   - Executa no Raspberry Pi em casa

2. **Screen**: Mantém programas rodando em background
   - Mesmo que você desconecte o SSH
   - Use: `screen -S nome` para criar, `Ctrl+A D` para sair

3. **ngrok**: Abre um "túnel" para a internet
   - Qualquer pessoa com o link consegue acessar
   - Use senha se quiser segurança

4. **VPN**: Faz parecer que você está em casa
   - Mais seguro que Port Forwarding
   - Recomendado

---

## 📞 Resumo Final

```
1. Compre Raspberry Pi Zero W (R$ 30-50)
2. Prepare o cartão SD com o SO
3. Conecte à tomada em casa
4. Baixe app SSH (Terminus) no iPhone
5. Conecte ao Raspberry Pi via SSH
6. Instale o projeto com comandos
7. Deixe rodando em background (screen)
8. Acesse pelo Safari no iPhone
9. Configure VPN/ngrok para acessar de fora
10. PRONTO! Veja se há alguém em casa!
```

---

**Criado com ❤️ para quem usa APENAS iPhone**

Versão: 1.0  
Data: 29 de Julho de 2025  
Status: ✅ Pronto para seguir

**Você consegue fazer tudo isso! Comece agora!**
