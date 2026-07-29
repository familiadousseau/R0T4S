# 🔥 Visão Térmica - Raio-X da Parede

## ✨ Agora Visualize Como Um Sensor Térmico!

Você pediu algo tipo **raio-x da parede** mostrando a silhueta como uma **sombra térmica**... **FEITO!** 🚀

---

## 🎯 O Que É

Uma **visualização térmica** que mostra:

```
┌─────────────────────────────────────────────┐
│  🔥 VISÃO TÉRMICA - WiFi Sensing            │
├─────────────────────────────────────────────┤
│                                             │
│          [    PAREDE    ]                   │
│                                             │
│             ╭─────────╮                     │
│             │  🟡🟠🔴  │  Silhueta          │
│             │  Térmica │  (Sombra)          │
│             │  Quente  │                    │
│             ╰─────────╯                     │
│         (Raio-X da Pessoa)                  │
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│  ATIVIDADE: WALKING                         │
│  RSSI: -55 dBm                              │
│  DISTÂNCIA: 3.2 m                           │
│  AMOSTRAS: 42                               │
│                                             │
│  [🔌 Conectar] [🤖 Carregar]               │
│                                             │
│  ESCALA TÉRMICA:                            │
│  🔵 Frio (-70 dBm)                         │
│  🟢 Médio (-60 dBm)                        │
│  🟡 Quente (-50 dBm)                       │
│  🔴 Muito Quente (-40 dBm)                 │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🌡️ Como Funciona

### 1. Captura de Sinal WiFi
```
ESP32 mede força do sinal (RSSI)
em diferentes direções
```

### 2. Mapa Térmico
```
RSSI forte (-40 dBm) = Vermelho (Quente)
RSSI médio (-60 dBm) = Verde (Morno)
RSSI fraco (-80 dBm) = Azul (Frio)
```

### 3. Desenha Silhueta
```
A silhueta aparece como uma sombra térmica
onde o sinal é mais forte (pessoa próxima)
```

### 4. Animação em Tempo Real
```
Atualiza 60fps (suave e fluida)
Mostra movimento contínuo
Efeito de pulso na silhueta
```

---

## 🎨 Visualização por Atividade

### 🚶 WALKING (Caminhando)
```
Silhueta: Se move de um lado a outro
Cor: Laranja/Vermelho (ativo)
Tamanho: Maior (mais movimento)
Pulso: Rápido (80x/s)
```

### 🪑 SITTING (Sentado)
```
Silhueta: Centralizada, mais baixa
Cor: Verde (ativo mas estático)
Tamanho: Médio
Pulso: Lento (40x/s)
```

### 🧍 STANDING (Em Pé)
```
Silhueta: Centralizada, altura normal
Cor: Azul/Verde (estático)
Tamanho: Médio
Pulso: Mínimo (20x/s)
```

---

## 📊 Escala de Cores

```
RSSI → Cor → Significado

-40 dBm  🔴 VERMELHO INTENSO   (Muito quente, muito perto)
-45 dBm  🟠 VERMELHO-LARANJA   (Quente, perto)
-50 dBm  🟡 LARANJA            (Morno, distância normal)
-55 dBm  🟢 VERDE              (Morno-frio, um pouco longe)
-60 dBm  🟦 AZUL CLARO         (Frio, longe)
-70 dBm  🟦 AZUL ESCURO        (Muito frio, muito longe)
-80 dBm  ⚫ PRETO              (Nenhum sinal)
```

---

## 🖥️ Interface

### Lado Esquerdo: Visualização Térmica
- **Parede com efeito de raio-X**
- **Silhueta como sombra térmica**
- **Cores indicam intensidade do sinal**
- **Animação contínua**
- **Escala de cores (legenda)**

### Lado Direito: Controles & Dados
- **📊 Atividade detectada**
- **📡 RSSI (força do sinal)**
- **📏 Distância calculada**
- **📊 Número de amostras**
- **🔌 Botões de controle**
- **🎮 Botões de teste (Walk/Sit/Stand)**
- **📋 Log de eventos**

---

## 🎮 Como Usar

### 1. Abra no Navegador

```
http://192.168.X.X:5000/thermal
```

### 2. Conecte ESP32

```
Clique em "🔌 Conectar"
Aguarde: "SERIAL CONECTADO"
```

### 3. Carregue Modelo

```
Clique em "🤖 Carregar"
Aguarde: "MODELO CARREGADO"
```

### 4. Veja a Silhueta Térmica!

```
A sombra aparecerá na parede
Cores indicam distância
Muda com a atividade
```

---

## 🎨 Efeitos Visuais

### Scanlines
```
Linhas horizontais que se movem continuamente
Efeito de câmera de vigilância antiga
Reforça a sensação de "raio-x"
```

### Pulso
```
Silhueta "respira" ritmicamente
Intensidade varia com RSSI
Efeito hipnotizante
```

### Aura Térmica
```
Halo ao redor da silhueta
Cor indica temperatura (RSSI)
Se expande/contrai com movimento
```

### Glow (Brilho)
```
Silhueta brilha no escuro
Efeito neon verde
Cria sensação de futurista
```

---

## 📱 Responsivo

### Desktop
```
┌──────────────────────────────┬─────────────────┐
│   [VISUALIZAÇÃO TÉRMICA]     │ CONTROLES       │
│                              │                 │
│                              │ Atividade       │
│       (PAREDE)               │ RSSI            │
│                              │ Distância       │
│       ╭──────╮               │                 │
│       │ 🔥🟠  │ Silhueta      │ [Conectar]      │
│       ╰──────╯               │ [Carregar]      │
│                              │                 │
│                              │ Log             │
└──────────────────────────────┴─────────────────┘
```

### Celular/Tablet
```
┌─────────────────────────────┐
│  [VISUALIZAÇÃO TÉRMICA]     │
│                             │
│      ╭──────╮               │
│      │ 🔥🟠  │ Silhueta      │
│      ╰──────╯               │
│                             │
├─────────────────────────────┤
│ CONTROLES                   │
│ Atividade: WALKING          │
│ RSSI: -55 dBm               │
│ Distância: 3.2 m            │
│ [Conectar] [Carregar]       │
└─────────────────────────────┘
```

---

## 🧪 Teste Sem ESP32

Clique nos botões para simular:

```
🚶 - Simula caminhando
🪑 - Simula sentado
🧍 - Simula em pé
```

A silhueta térmica se adapta automaticamente!

---

## 🔴 Cores Significam O Quê

| Cor | RSSI | Significado |
|-----|------|-------------|
| 🔴 Vermelho | -40 a -45 | Pessoa muito perto (< 1m) |
| 🟠 Laranja | -50 a -55 | Pessoa perto (1-3m) |
| 🟡 Amarelo | -55 a -60 | Pessoa a distância normal (3-5m) |
| 🟢 Verde | -60 a -65 | Pessoa longe (5-10m) |
| 🔵 Azul | -70+ | Pessoa muito longe (10m+) |

---

## 💡 Dicas

### Para Melhor Efeito
1. **Apague as luzes** (mais contraste)
2. **Aumente o brilho da tela**
3. **Use em tela cheia** (F11)
4. **Coloque perto da parede** (realismo)

### Interpretação
- **Silhueta no centro** = Pessoa em frente ao ESP32
- **Silhueta se move** = Pessoa caminhando
- **Cor muda constantemente** = Movimento
- **Cor estática** = Pessoa parada

### Se Não Vir Nada
1. Conecte o ESP32 (clique "Conectar")
2. Carregue o modelo (clique "Carregar")
3. Aguarde 2-3 segundos
4. Mova-se perto do ESP32

---

## 🎯 Quando Usar

### Apresentações
```
👉 /thermal
   Impressiona visualmente
   Futurista e intuitivo
   Fácil de entender
```

### Análise Técnica
```
👉 /pose
   Dados + gráficos + silhueta
```

### Dados Puros
```
👉 / (raiz)
   Gráficos técnicos detalhados
```

---

## 🌈 Inspiração

Esta visualização é inspirada em:
- 📹 Câmeras térmicas profissionais
- 🎮 Visão de predador (Predator - filme)
- 🛡️ Sistemas de detecção militar
- 🔬 Tecnologia de sensoriamento WiFi
- 🎬 Ficção científica futurista

---

## 🚀 Acessar Agora

```bash
# Terminal
cd /home/user/R0T4S/wifi-human-detection
bash start_live.sh
```

```
# Navegador
http://192.168.X.X:5000/thermal
```

**E veja o raio-X da parede funcionando!** 🔥

---

## 📊 Comparação de Interfaces

| Interface | Gráficos | Silhueta | Térmica | Melhor Para |
|-----------|----------|----------|---------|-------------|
| `/` | ✅✅ | ❌ | ❌ | Análise técnica |
| `/pose` | ✅ | ✅ | ❌ | Completo |
| `/pose_only` | ❌ | ✅✅ | ❌ | Apresentação |
| `/thermal` | ❌ | ❌ | ✅✅ | Futurista |

---

## 🎊 Recursos

✅ Visualização térmica em tempo real  
✅ Silhueta como sombra (raio-x)  
✅ Cores variam com RSSI  
✅ Animação contínua (60fps)  
✅ Efeito de scanlines  
✅ Pulso sincronizado  
✅ Aura térmica  
✅ Interface futurista  
✅ Responsivo (mobile-friendly)  
✅ Totalmente intuitivo  

---

**Criado com ❤️ e autorização completa** 🚀

Versão: 1.0  
Data: 29 de Julho de 2025  
Status: ✅ Pronto e Impressionante
