# 🚶 Visualizador de Pose - App Visual Intuitiva

## ✨ Agora Você Tem 3 Interfaces Diferentes!

Escolha a que mais gosta:

---

## 1️⃣ Dashboard Completo com Pose (RECOMENDADO)

**URL:** `http://192.168.X.X:5000/pose`

```
┌────────────────────────────────────────────────────┐
│ 🛰️ WiFi Sensing - Visualizador de Pose             │
├────────────────────────────────────────────────────┤
│                                                    │
│         ATIVIDADE DETECTADA: WALKING               │
│                                                    │
│              ┌─────┐                              │
│              │  O  │  (Cabeça)                    │
│              │ /│\ │  (Braços)                    │
│            / │ / \ │                              │
│           /  │/   \│ \                            │
│             /      \  \  (Corpo)                  │
│            /        \  \                          │
│           /          \  \                         │
│        /              \  \                        │
│       /                \  \                       │
│    /                    \  \                      │
│  /                        \  \  (Pernas)         │
│                                                  │
│        Distância: 3.2 m  |  RSSI: -55 dBm       │
│                                                  │
├─────────────────────────┬─────────────────────────┤
│  📊 Gráfico Amplitude   │  🔌 Conexão Serial      │
│  (valores de CSI)        │  🤖 Modelo ML           │
│                          │  📋 Log de Eventos     │
└─────────────────────────┴─────────────────────────┘
```

**Características:**
- ✅ Silhueta que muda de pose
- ✅ Gráfico de amplitude CSI
- ✅ Mostra distância calculada
- ✅ RSSI do sinal
- ✅ Layout em 2 colunas (desktop)
- ✅ Responsivo (mobile)

---

## 2️⃣ Visualizador de Pose Minimalista

**URL:** `http://192.168.X.X:5000/pose_only`

Interface limpa focada apenas na silhueta e distância!

**Características:**
- ✅ Interface limpa e simples
- ✅ Foco na silhueta
- ✅ Perfeito para apresentações
- ✅ Usa menos dados
- ✅ Móvel otimizado

---

## 3️⃣ Dashboard Original (com gráficos)

**URL:** `http://192.168.X.X:5000`

Como antes, mas com WebSocket (tempo real).

---

## 🎨 Como As Silhuetas Funcionam

### Posição de Pé (STANDING)
- **Cor:** Azul (#667eea)
- **Significado:** Pessoa está em pé, braços caídos
- **Uso:** Pessoa de pé em repouso

### Sentado (SITTING)
- **Cor:** Verde (#2ed573)
- **Significado:** Pessoa sentada em cadeira/banco
- **Uso:** Pessoa sentada

### Caminhando (WALKING)
- **Cor:** Laranja (#ffa502)
- **Significado:** Pessoa caminhando (braços e pernas em movimento)
- **Uso:** Movimento contínuo/caminhando

### Aguardando (WAITING)
- **Cor:** Cinza (#999)
- **Significado:** Nenhuma atividade detectada
- **Uso:** Inicialização/nenhum movimento

---

## 📏 Cálculo de Distância

A distância é **calculada automaticamente** a partir do **RSSI** (força do sinal):

**Fórmula RF (Friis Path Loss Model):**
```
distance = 10^((refRSSI - rssi) / (10 * n))
```

Onde:
- refRSSI = -50 dBm (referência a 1 metro)
- rssi = valor medido
- n = 2 (expoente em ambiente livre)

**Escala de Distância:**
- -50 dBm → 1.0 m (Muito perto)
- -55 dBm → 1.8 m
- -60 dBm → 3.2 m (Típico em casa)
- -70 dBm → 10 m (Longe)

**Nota:** Quanto mais **negativo** o RSSI, mais **longe** está!

---

## 🎮 Como Usar

### 1. Abra no Navegador

**Desktop:**
```
http://localhost:5000/pose
```

**Celular (mesma WiFi):**
```
http://192.168.X.X:5000/pose
```

### 2. Conecte o ESP32
- Clique em **"Conectar"**
- Verifique que apareceu: ✓ Serial conectado

### 3. Carregue o Modelo
- Clique em **"Carregar"**
- Verifique que apareceu: ✓ Modelo carregado

### 4. Veja em Tempo Real!
- Silhueta muda baseado na atividade
- Distância atualiza
- Log mostra eventos

### Botões de Teste (sem ESP32)
- **🚶 Walk** - Simular walking
- **🪑 Sit** - Simular sitting
- **🧍 Stand** - Simular standing

---

## 📊 Comparação das Interfaces

| Feature | Pose Only | Com Pose | Completo |
|---------|-----------|----------|----------|
| Silhueta Animada | ✅ Grande | ✅ Média | ❌ |
| Distância Visual | ✅ Sim | ✅ Sim | ✗ |
| Gráfico CSI | ❌ | ✅ | ✅ |
| Controles Fáceis | ✅ | ✅ | ✅ |
| Mobile Otimizado | ✅✅ | ✅ | ✅ |
| Para Apresentação | ✅ Ideal | ✅ Bom | ✗ |

---

## 🎯 Qual Usar?

### Para Apresentação/Demo
```
👉 /pose_only
   Interface limpa
   Impressiona visualmente
   Mostra bem a distância
```

### Para Análise Completa
```
👉 /pose
   Silhueta + gráficos
   Melhor análise
   Dashboard profissional
```

### Para Dados Técnicos
```
👉 / (raiz)
   Todos os gráficos
   Valores detalhados
   Para cientistas/devs
```

---

## 💡 Dicas de Uso

### Para Melhor Visualização
1. **Abra em tela cheia** (F11 ou Cmd+Ctrl+F)
2. **Use modo landscape** no celular
3. **Aumente o brilho** da tela
4. **Foque a câmera do ESP32** para a pessoa

### Interpretando a Visualização
- 🟠 **Laranja** = Caminhando (movimento)
- 🟢 **Verde** = Sentado (estático)
- 🔵 **Azul** = Em pé (neutro)
- ⚪ **Cinza** = Aguardando

### Troubleshooting
- **Silhueta não muda?** → Conecte o ESP32
- **Distância = 0?** → Verifique modelo ML
- **Sem dados?** → Aumentar poder do sinal

---

## 📱 Design Responsivo

Funciona perfeitamente em:
- 💻 Desktop (grande com todos os gráficos)
- 📱 Celular (otimizado, stackado verticalmente)
- 📊 Tablet (layout equilibrado)

---

## 🚀 Acessar Agora

```bash
# Terminal do seu PC
cd /home/user/R0T4S/wifi-human-detection
bash start_live.sh
```

Depois abra no navegador:
```
http://192.168.X.X:5000/pose
```

(O IP correto aparecerá no terminal)

---

## 🎊 O Que Você Tem Agora

✅ Visualizador intuitivo com silhueta  
✅ Cálculo automático de distância  
✅ Animações suaves e coloridas  
✅ Múltiplas interfaces para diferentes usos  
✅ Design responsivo (mobile-first)  
✅ Tempo real com WebSocket  
✅ Botões de teste para demonstração  

---

**Criado com ❤️ para visualizações visuais intuitivas**

Versão: 1.0  
Data: 29 de Julho de 2025  
Status: ✅ Pronto para usar
