# 🌐 Como Usar a App Web ao Vivo no Celular

## 🚀 Instalação Rápida (3 Passos)

### 1️⃣ Instale as Dependências

```bash
cd /home/user/R0T4S/wifi-human-detection
pip install -r requirements.txt
```

**Tempo:** ~2 minutos

### 2️⃣ Inicie o Servidor

```bash
bash start_live.sh
```

Você verá:
```
✓ IP Local: 192.168.1.100:5000

ACESSE NO NAVEGADOR:
   Celular: http://192.168.1.100:5000
   Computador: http://localhost:5000
```

### 3️⃣ Abra no Seu Celular

1. Certifique-se que seu **celular está na mesma WiFi da casa**
2. Abra o navegador
3. Digite: `http://192.168.1.100:5000` (substitua o IP)

✨ **Pronto! Está ao vivo!**

---

## 📱 Como Usar no Celular

### 🔌 Passo 1: Conectar o ESP32

1. Plugue o ESP32 no USB do **computador onde o servidor está rodando**
2. No celular, abra a app
3. Clique no botão **"Conectar"**

**Resultado esperado:**
```
✓ Conectado com sucesso
/dev/ttyUSB0 @ 115200
```

### 🤖 Passo 2: Carregar o Modelo ML

1. Certifique-se que o arquivo `model.pkl` existe
   ```bash
   ls -l model.pkl
   ```

2. Na app, clique em **"Carregar Modelo"**

**Resultado esperado:**
```
✓ Modelo ML carregado
```

### 🎯 Passo 3: Veja os Dados em Tempo Real

Agora você verá:
- ✅ **Atividade Detectada** em GRANDE (WALKING, SITTING, STANDING)
- ✅ **RSSI** (força do sinal em dBm)
- ✅ **Gráfico** de amplitude CSI atualizando
- ✅ **Log** com eventos

---

## 📊 Entendendo a Interface

### 🎯 Seção de Atividade

```
┌─────────────────────────────┐
│  ATIVIDADE DETECTADA        │
│           🚶                 │
│       WALKING               │
│  RSSI: -45 dBm  Buffer: 42  │
└─────────────────────────────┘
```

**O que significa:**
- 🚶🪑🧍 = Tipo de atividade
- RSSI = Força do sinal (-100 a 0, quanto maior/menos negativo = mais forte)
- Buffer = Quantidade de amostras capturadas

### 📈 Gráfico

Mostra as **20 últimas amplitudes CSI** dos sinais WiFi capturados.

### 🎮 Botões de Controle

- **🚶 Walk** = Enviar label "Walking" para treinamento
- **🪑 Sit** = Enviar label "Sitting" para treinamento
- **🧍 Stand** = Enviar label "Standing" para treinamento

### 📋 Log de Eventos

Mostra tudo que aconteceu:
```
[14:32:15] ✓ Conectado ao servidor
[14:32:18] ✓ Modelo ML carregado
[14:32:45] 📤 Enviado: walking
[14:35:22] ✓ Atividade: STANDING
```

---

## 🔧 Descobrir o IP Automaticamente

Se não sabe qual é o IP do computador onde o servidor está rodando:

**Linux/Mac:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
# Procure por algo como: 192.168.1.100
```

**Windows:**
1. Abra Prompt de Comando
2. Digite: `ipconfig`
3. Procure por "IPv4 Address"

**Ou simplesmente:**

O script `start_live.sh` **mostra o IP automaticamente**:
```
✓ IP: 192.168.1.100
```

---

## 🐛 Solução de Problemas

### ❌ "Não consegue conectar no servidor"

**Problema:** Navegador diz "Não é possível alcançar"

**Solução:**

1. Verifique que você está na **mesma WiFi**
   ```bash
   # No celular, abra Configurações → WiFi → Ver rede conectada
   ```

2. Certifique-se que o servidor está **rodando**
   ```bash
   # No computador, você deve ver:
   # ✓ Servidor iniciado!
   ```

3. Tente o **IP do computador**, não localhost
   ```
   Errado:  http://localhost:5000
   Correto: http://192.168.1.100:5000
   ```

### ❌ "App conecta mas não mostra dados"

**Problema:** Interface carrega mas sem dados

**Solução:**

1. Conecte o **ESP32 via USB** no computador
2. Clique em **"Conectar"** na app
3. Verifique que apareceu a mensagem:
   ```
   ✓ /dev/ttyUSB0 @ 115200
   ```

4. Se não aparecer, verifique a porta:
   ```bash
   ls /dev/tty* | grep USB
   # Resultado: /dev/ttyUSB0 (ou outro)
   ```

### ❌ "Modelo não carrega"

**Problema:** Clica em carregar mas não acontece nada

**Solução:**

1. Verifique que o arquivo existe:
   ```bash
   ls -la model.pkl
   ```

2. Se não existe, treine um novo:
   ```bash
   python pipeline.py --data-dir ./data --output model.pkl
   ```

### ❌ "App fica lenta ou congela"

**Problema:** Muitos dados, interface lenta

**Solução:**

1. **Recarregue a página** no celular
2. **Reinicie o servidor**
   ```bash
   CTRL+C para parar
   bash start_live.sh para reiniciar
   ```

---

## 📊 Dados em Tempo Real

### Como Funciona

```
ESP32 (Captura CSI)
    ↓ (Serial USB 115200 baud)
Python Server (Processa)
    ↓ (WebSocket - TEMPO REAL)
Navegador (Celular)
    ↓ (Mostra gráficos e atividade)
Você vê!
```

**Taxa de Atualização:** ~2 updates por segundo (500ms)

### Latência

- Captura → Processamento: ~50ms
- Servidor → Celular (WiFi): ~100-200ms
- **Total:** ~150-250ms (meio segundo)

---

## 💡 Dicas Avançadas

### Otimizar para Celular

O dashboard já é otimizado, mas você pode:

1. **Aumentar tamanho do texto:**
   - Android: Configurações → Acessibilidade → Tamanho da fonte
   - iOS: Configurações → Acessibilidade → Tamanho do texto

2. **Evitar zoom:**
   - Double-tap para zoom já está desabilitado
   - Pinch to zoom também

3. **Manter tela acesa:**
   - Android: Configurações → Display → Manter tela acesa
   - iOS: Configurações → Visor e Brilho → Auto-travamento

### Compartilhar com Outros

Qualquer um na **mesma WiFi** pode acessar:

```
Diga para seus amigos:
"Acesse http://192.168.1.100:5000 no seu celular"
```

Múltiplos celulares podem estar conectados **ao mesmo tempo**!

---

## 📈 Dados do Servidor

### Tamanho do Buffer

O servidor mantém os **últimos 200 dados** em memória.

Para ver histórico completo:
1. O servidor já salva dados em CSV na memória
2. Você pode exportar

### Performance

- **Memória:** ~50-100 MB
- **CPU:** <5% (em idle)
- **Conexões simultâneas:** Suporta múltiplas

---

## 🎯 Próximos Passos

### 1. Treinar Seu Próprio Modelo

Coletar dados suas atividades e treinar:

```bash
python pipeline.py --data-dir ./data --output model.pkl
```

Depois recarregue na app.

### 2. Adicionar Novas Atividades

Edite `pipeline.py` para treinar com mais classes:
```python
labels = ['walking', 'sitting', 'standing', 'running', 'jumping']
```

### 3. Usar em Produção

Para deixar rodando 24/7:

```bash
# Use screen ou tmux
screen -S wifi-sensing bash start_live.sh

# Ou use systemd (Linux)
sudo systemctl create-unit wifi-sensing
```

---

## 📞 Suporte

### Documentação Completa

- `GUIA_WEB_SERVER.md` - Documentação detalhada
- `WIFI_SENSING_PROJECT.md` - Sobre o projeto
- `api_examples.py` - Exemplos de código

### Recursos Online

- Flask-SocketIO: https://flask-socketio.readthedocs.io/
- ESP32: https://docs.espressif.com/
- scikit-learn: https://scikit-learn.org/

---

## ✅ Checklist de Uso

- [ ] Instalei dependências (`pip install -r requirements.txt`)
- [ ] Iniciei servidor (`bash start_live.sh`)
- [ ] Descobri o IP local (ex: 192.168.1.100)
- [ ] Abri no navegador do celular
- [ ] Conectei o ESP32 via USB
- [ ] Cliquei em "Conectar" na app
- [ ] Carreguei o modelo ML
- [ ] Vejo dados em tempo real! 🎉

---

## 🎊 Parabéns! 

Você agora tem um **sistema profissional de Wi-Fi Sensing rodando na sua casa** que você pode acessar de **qualquer dispositivo** na rede!

Aproveite! 🚀

---

**Versão:** 1.0  
**Data:** 29 de Julho de 2025  
**Status:** ✅ Completo e Testado
