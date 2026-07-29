# 🛰️ Wi-Fi-CSI Human Sensing Through Wall Activity Detection

## 📋 Visão Geral
Um sistema de detecção de atividades humanas através de paredes usando **Wi-Fi Channel State Information (CSI)** e **Machine Learning**. Funciona sem câmeras, sem sensores vestíveis e com hardware de baixo custo (ESP32).

**Linhas de código:** ~27,721  
**Linguagens:** C++, Python  
**Hardware:** ESP32, OLED Display SSD1306, LEDs RGB  

---

## ✨ Funcionalidades Principais

### 1. **Captura de Sinal Wi-Fi (CSI)**
- Captura dados brutos de **Channel State Information** do Wi-Fi
- Extrai informações de **amplitude** e **fase** do sinal
- Processamento em tempo real via ESP32
- Dados transmitidos via serial para análise em PC

### 2. **Detecção de Atividades Humanas**
Identifica 3 tipos de atividades:
- 🚶 **Walking** (Caminhando)
- 🪑 **Sitting** (Sentado)
- 🧍 **Standing** (De pé)

### 3. **Localização Sem Dispositivo (Device-Free)**
- Detecta presença humana através de paredes
- Funciona sem marcadores ou sensores no corpo
- Baseado apenas em mudanças no sinal Wi-Fi

### 4. **Processamento de Sinais RF**
- Filtro passa-banda (1-50 Hz)
- Extração de características usando Scipy
- Análise de múltiplas subportadoras Wi-Fi

### 5. **Machine Learning - Random Forest**
- Classificador com ~100+ features
- Extração de features por subportadora:
  - Média, desvio padrão
  - Valores mínimo e máximo
  - Assimetria (skewness)
  - Curtose (kurtosis)
  - Energia (sum of squares)

### 6. **Interface Visual com OLED**
- Display SSD1306 (128x64)
- Mostra atividade detectada em tempo real
- Comunicação I2C com ESP32
- Font 5x7 customizado integrado

### 7. **Indicadores Visuais com LEDs**
- 🔴 LED Vermelho → Walking
- 🟢 LED Verde → Sitting
- 🟡 LED Amarelo → Standing
- Controle via GPIO do ESP32

### 8. **Comunicação em Tempo Real**
- Serial UART bidirecional
- Recebe labels de atividade
- Confirma com ACK
- CSV output com todos os dados CSI

---

## 📁 Estrutura do Projeto

```
wifi-human-detection/
├── README.md (original)
├── Human_Detection_using_wifi/
│   ├── main.cc                    # Firmware ESP32 (447 linhas)
│   │   ├── Inicialização Wi-Fi AP
│   │   ├── Captura CSI
│   │   ├── Driver OLED SSD1306
│   │   ├── Controle de GPIO/LEDs
│   │   └── Serial receiver task
│   │
│   ├── pipeline.py                # ML Pipeline
│   │   ├── load_all_data()        # Carrega dados CSV
│   │   ├── sliding_window()       # Janelas deslizantes
│   │   ├── extract_features()     # Extração de features
│   │   ├── train_model()          # Treina Random Forest
│   │   └── save_model()           # Salva modelo joblib
│   │
│   ├── parse_csi.py               # Processamento de CSI
│   │   ├── Converte raw CSI para amplitude/fase
│   │   └── Demonstração de parsing
│   │
│   ├── capture.py                 # Captura dados
│   ├── realtime.py                # Inferência em tempo real
│   ├── serial_plot_csi_live.py   # Visualização ao vivo
│   ├── serial_append_time.py     # Timestamp
│   ├── serial_measure_rate.py    # Taxa de captura
│   │
│   ├── example_csi.csv            # Dados de exemplo
│   ├── Project_report.pdf         # Relatório técnico
│   └── Project_PPT.pdf            # Apresentação
```

---

## 🔧 Componentes Técnicos

### ESP32 (Firmware C++)
**Pinos GPIO:**
```
LED_WALKING  = GPIO 25
LED_SITTING  = GPIO 26
LED_STANDING = GPIO 27
I2C_SDA      = GPIO 21
I2C_SCL      = GPIO 22
```

**Configuração Wi-Fi:**
- SSID: `ESP32_CSI`
- Password: `12345678`
- Canal: 6 (configurável)
- Modo: Access Point (AP)

**Periféricos:**
- OLED Display SSD1306 (endereço I2C: 0x3C)
- Taxa de baud serial: Padrão
- Frequência I2C: 400 kHz

### Pipeline de ML (Python)
1. **Leitura de Dados:** Carrega CSV com CSI raw
2. **Filtragem:** Butter filter passa-banda (1-50 Hz)
3. **Janelamento:** Sliding window (window_size=100, step=50)
4. **Feature Extraction:** ~100+ features por janela
5. **Classificação:** Random Forest com cross-validation
6. **Exportação:** Modelo salvo em joblib para inferência

### Extração de Features
Para cada subportadora:
- `mean, std, min, max, range`
- `skewness, kurtosis, energy`
- Agregação por todas as subportadoras
- Total: ~100 features por amostra

---

## 📊 Fluxo de Dados

```
ESP32 (CSI Capture)
    ↓
Serial UART (CSV format)
    ↓
Python Pipeline (parse_csi.py)
    ↓
Feature Extraction
    ↓
Random Forest ML Model
    ↓
Activity Label (walking/sitting/standing)
    ↓
OLED Display + LEDs
```

---

## 🚀 Como Usar

### Setup Inicial
1. **Compilar Firmware:**
   ```bash
   cd Human_Detection_using_wifi
   idf.py build
   idf.py flash -p /dev/ttyUSB0
   ```

2. **Instalar Dependências Python:**
   ```bash
   pip install numpy pandas scipy scikit-learn joblib matplotlib
   ```

3. **Treinar Modelo:**
   ```bash
   python pipeline.py --data-dir ./data --output model.pkl
   ```

### Captura de Dados
```bash
python capture.py --port /dev/ttyUSB0 --output data.csv
```

### Inferência em Tempo Real
```bash
python realtime.py --model model.pkl --port /dev/ttyUSB0
```

### Visualização
```bash
python serial_plot_csi_live.py --port /dev/ttyUSB0
```

---

## 🎯 Vantagens do Sistema

✅ **Device-Free:** Não requer sensores no corpo  
✅ **Through-Wall:** Funciona através de paredes  
✅ **Low-Cost:** Hardware comum (ESP32 ~$10)  
✅ **Real-Time:** Detecção instantânea  
✅ **Privacy-Friendly:** Sem câmeras/microfones  
✅ **Multiple Activities:** 3 classes de atividades  
✅ **Visual Feedback:** OLED + LEDs RGB  

---

## 📈 Performance Esperada

- **Taxa de captura:** ~100 amostras/segundo
- **Latência de detecção:** <500ms
- **Acurácia RF:** Tipicamente 85-95% (com treino adequado)
- **Consumo ESP32:** ~100-200mA em operação

---

## 🔬 Tecnologias Utilizadas

- **Hardware:** ESP32, OLED SSD1306, LEDs RGB
- **Embedded:** C++, FreeRTOS, ESP-IDF
- **ML Framework:** scikit-learn (RandomForest)
- **Signal Processing:** SciPy, NumPy
- **Protocolos:** I2C, UART, Wi-Fi 802.11b/g/n CSI

---

## 📚 Arquivos Principais

| Arquivo | Linhas | Descrição |
|---------|--------|-----------|
| `main.cc` | 447 | Firmware ESP32 completo |
| `pipeline.py` | ~200+ | ML training pipeline |
| `parse_csi.py` | 39 | Parser CSI amplitude/phase |
| `realtime.py` | ~100+ | Inferência tempo real |
| `capture.py` | ~100+ | Coleta de dados |

---

## 🔐 Aplicações Possíveis

1. **Smart Homes:** Detecção de atividades em ambientes
2. **Healthcare:** Monitoramento de pacientes sem câmeras
3. **Security:** Detecção de movimento através de paredes
4. **Fitness:** Contagem de exercícios
5. **Ambient Sensing:** Contexto ambiental inteligente

---

## 📝 Notas Técnicas

- CSI é extraído de frames 802.11 padrão
- Cada subportadora contém informações de amplitude/fase
- O filtro passa-banda remove ruído de baixa frequência
- Random Forest oferece boa generalização com dados limitados
- Necessário treino com dados do ambiente específico

---

**Projeto Baseado em:** Pesquisa de Anuja Naik  
**Ano:** 2025-2026  
**Status:** Ativo e em desenvolvimento
