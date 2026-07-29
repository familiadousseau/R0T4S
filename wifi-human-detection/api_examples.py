"""
🌐 Exemplos de Uso da API REST do Web Server
Demonstra como interagir programaticamente com o sistema
"""

import requests
import json
import time
from datetime import datetime

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Configuração
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BASE_URL = "http://localhost:5000"
HEADERS = {"Content-Type": "application/json"}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Exemplo 1: Verificar Status do Sistema
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def exemplo_1_status():
    """Obtém status atual do sistema"""
    print("\n" + "="*60)
    print("📊 EXEMPLO 1: Verificar Status")
    print("="*60)

    try:
        response = requests.get(f"{BASE_URL}/api/status")
        status = response.json()

        print(f"✓ Conectado: {status['connected']}")
        print(f"✓ Atividade: {status['activity']}")
        print(f"✓ Buffer: {status['buffer_size']} amostras")
        print(f"✓ Timestamp: {status['timestamp']}")

        return status
    except Exception as e:
        print(f"✗ Erro: {e}")
        return None

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Exemplo 2: Conectar ao ESP32
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def exemplo_2_conectar(porta="/dev/ttyUSB0", baud=115200):
    """Conecta ao ESP32 via serial"""
    print("\n" + "="*60)
    print("🔌 EXEMPLO 2: Conectar ao ESP32")
    print("="*60)

    payload = {
        "port": porta,
        "baud": baud
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/connect",
            json=payload,
            headers=HEADERS
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✓ Sucesso: {result['message']}")
            return True
        else:
            print(f"✗ Erro: {response.json()['message']}")
            return False
    except Exception as e:
        print(f"✗ Erro: {e}")
        return False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Exemplo 3: Carregar Modelo ML
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def exemplo_3_carregar_modelo(modelo_path="model.pkl"):
    """Carrega modelo machine learning"""
    print("\n" + "="*60)
    print("🤖 EXEMPLO 3: Carregar Modelo ML")
    print("="*60)

    payload = {"path": modelo_path}

    try:
        response = requests.post(
            f"{BASE_URL}/api/model/load",
            json=payload,
            headers=HEADERS
        )

        if response.status_code == 200:
            print(f"✓ Modelo '{modelo_path}' carregado com sucesso")
            return True
        else:
            print(f"✗ Falha ao carregar modelo")
            return False
    except Exception as e:
        print(f"✗ Erro: {e}")
        return False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Exemplo 4: Obter Dados CSI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def exemplo_4_obter_dados():
    """Obtém últimos dados CSI capturados"""
    print("\n" + "="*60)
    print("📈 EXEMPLO 4: Obter Dados CSI")
    print("="*60)

    try:
        response = requests.get(f"{BASE_URL}/api/data")
        data = response.json()

        print(f"✓ Total de amostras: {len(data['data'])}")
        print(f"✓ Atividade detectada: {data['activity']}")

        if data['data']:
            latest = data['data'][-1]
            amps = latest['amplitudes'][:5]  # Primeiras 5 subportadoras
            print(f"✓ Últimas 5 amplitudes: {amps}")
            print(f"✓ RSSI: {latest['rssi']} dBm")
            print(f"✓ Tempo: {latest['time']}")

        return data
    except Exception as e:
        print(f"✗ Erro: {e}")
        return None

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Exemplo 5: Enviar Comandos
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def exemplo_5_enviar_comando(atividade="walking"):
    """Envia comando para ESP32"""
    print("\n" + "="*60)
    print("🎮 EXEMPLO 5: Enviar Comando")
    print("="*60)

    atividades_validas = ["walking", "sitting", "standing"]

    if atividade not in atividades_validas:
        print(f"✗ Atividade inválida. Use: {atividades_validas}")
        return False

    payload = {"command": f"LABEL:{atividade}"}

    try:
        response = requests.post(
            f"{BASE_URL}/api/send",
            json=payload,
            headers=HEADERS
        )

        if response.status_code == 200:
            print(f"✓ Comando enviado: LABEL:{atividade}")
            return True
        else:
            print(f"✗ Falha ao enviar comando")
            return False
    except Exception as e:
        print(f"✗ Erro: {e}")
        return False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Exemplo 6: Monitorar em Tempo Real
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def exemplo_6_monitorar(duracao=10):
    """Monitora sistema por N segundos"""
    print("\n" + "="*60)
    print("⏱️  EXEMPLO 6: Monitorar em Tempo Real")
    print("="*60)
    print(f"Monitorando por {duracao} segundos...")
    print()

    start_time = time.time()
    amostras = 0

    while time.time() - start_time < duracao:
        try:
            status = requests.get(f"{BASE_URL}/api/status").json()
            data = requests.get(f"{BASE_URL}/api/data").json()

            # Atualizar contadores
            if data['data']:
                amostras = len(data['data'])

            # Exibir informações
            timestamp = datetime.now().strftime("%H:%M:%S")
            connected = "✓" if status['connected'] else "✗"
            activity = status['activity'].upper()

            print(f"[{timestamp}] {connected} {activity:15} | Buffer: {amostras:3} | RSSI: ", end="")

            if data['data']:
                print(f"{data['data'][-1]['rssi']:4} dBm", end="")

            print()

            time.sleep(1)
        except Exception as e:
            print(f"✗ Erro: {e}")
            time.sleep(1)

    print("\n✓ Monitoramento finalizado")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Exemplo 7: Análise de Dados
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def exemplo_7_analisar_dados():
    """Analisa estatísticas dos dados coletados"""
    print("\n" + "="*60)
    print("📊 EXEMPLO 7: Análise de Dados")
    print("="*60)

    try:
        data = requests.get(f"{BASE_URL}/api/data").json()

        if not data['data']:
            print("✗ Nenhum dado disponível")
            return

        # Coletar estatísticas
        rssis = [d['rssi'] for d in data['data']]
        amps = [sum(d['amplitudes']) / len(d['amplitudes']) for d in data['data']]

        print(f"\n📌 Amostras Total: {len(data['data'])}")
        print(f"📌 RSSI (dBm):")
        print(f"   Mínimo: {min(rssis)}")
        print(f"   Máximo: {max(rssis)}")
        print(f"   Média:  {sum(rssis)/len(rssis):.1f}")
        print(f"\n📌 Amplitude Média (CSI):")
        print(f"   Mínima: {min(amps):.1f}")
        print(f"   Máxima: {max(amps):.1f}")
        print(f"   Média:  {sum(amps)/len(amps):.1f}")

    except Exception as e:
        print(f"✗ Erro: {e}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Exemplo 8: Exportar Histórico
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def exemplo_8_exportar_csv():
    """Exporta histórico em CSV"""
    print("\n" + "="*60)
    print("📥 EXEMPLO 8: Exportar Histórico CSV")
    print("="*60)

    try:
        response = requests.get(f"{BASE_URL}/api/history")

        if response.status_code == 200:
            filename = f"wifi_csi_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

            with open(filename, 'w') as f:
                f.write(response.text)

            print(f"✓ Arquivo exportado: {filename}")
            print(f"✓ Tamanho: {len(response.text)} bytes")
            return filename
        else:
            print("✗ Falha ao exportar")
            return None
    except Exception as e:
        print(f"✗ Erro: {e}")
        return None

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Exemplo 9: Teste de Conectividade
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def exemplo_9_teste_conectividade():
    """Testa se servidor está rodando"""
    print("\n" + "="*60)
    print("🔍 EXEMPLO 9: Teste de Conectividade")
    print("="*60)

    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✓ Servidor respondendo (HTTP {response.status_code})")
        print(f"✓ URL: {BASE_URL}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"✗ Não conseguiu conectar em {BASE_URL}")
        print("   Certifique-se que o servidor está rodando:")
        print("   python web_server.py")
        return False
    except Exception as e:
        print(f"✗ Erro: {e}")
        return False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Exemplo 10: Fluxo Completo
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def exemplo_10_fluxo_completo():
    """Executa fluxo completo do sistema"""
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*15 + "🚀 FLUXO COMPLETO DO SISTEMA 🚀" + " "*15 + "║")
    print("╚" + "="*58 + "╝")

    # 1. Teste conectividade
    if not exemplo_9_teste_conectividade():
        return

    time.sleep(1)

    # 2. Verificar status
    exemplo_1_status()
    time.sleep(1)

    # 3. Conectar ao ESP32
    exemplo_2_conectar()
    time.sleep(2)

    # 4. Carregar modelo
    exemplo_3_carregar_modelo()
    time.sleep(1)

    # 5. Enviar alguns comandos
    exemplo_5_enviar_comando("walking")
    time.sleep(1)

    # 6. Obter dados
    exemplo_4_obter_dados()
    time.sleep(1)

    # 7. Analisar dados
    exemplo_7_analisar_dados()

    print("\n" + "="*60)
    print("✓ Fluxo completo executado com sucesso!")
    print("="*60)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Menu Principal
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def menu():
    """Menu interativo"""
    while True:
        print("\n" + "╔" + "="*58 + "╗")
        print("║" + " "*20 + "📚 EXEMPLOS DE API REST" + " "*19 + "║")
        print("╠" + "="*58 + "╣")
        print("║ 1. Verificar Status                                         ║")
        print("║ 2. Conectar ao ESP32                                        ║")
        print("║ 3. Carregar Modelo ML                                       ║")
        print("║ 4. Obter Dados CSI                                          ║")
        print("║ 5. Enviar Comando                                           ║")
        print("║ 6. Monitorar em Tempo Real                                  ║")
        print("║ 7. Análise de Dados                                         ║")
        print("║ 8. Exportar Histórico CSV                                   ║")
        print("║ 9. Teste de Conectividade                                   ║")
        print("║ 0. Fluxo Completo                                           ║")
        print("║ q. Sair                                                    ║")
        print("╚" + "="*58 + "╝")

        choice = input("\nEscolha uma opção: ").strip().lower()

        if choice == '1':
            exemplo_1_status()
        elif choice == '2':
            porta = input("Porta serial [/dev/ttyUSB0]: ").strip() or "/dev/ttyUSB0"
            exemplo_2_conectar(porta)
        elif choice == '3':
            modelo = input("Caminho do modelo [model.pkl]: ").strip() or "model.pkl"
            exemplo_3_carregar_modelo(modelo)
        elif choice == '4':
            exemplo_4_obter_dados()
        elif choice == '5':
            ativ = input("Atividade [walking/sitting/standing]: ").strip().lower() or "walking"
            exemplo_5_enviar_comando(ativ)
        elif choice == '6':
            duracao = int(input("Duração em segundos [10]: ") or "10")
            exemplo_6_monitorar(duracao)
        elif choice == '7':
            exemplo_7_analisar_dados()
        elif choice == '8':
            exemplo_8_exportar_csv()
        elif choice == '9':
            exemplo_9_teste_conectividade()
        elif choice == '0':
            exemplo_10_fluxo_completo()
        elif choice == 'q':
            print("\n✓ Até logo! 👋")
            break
        else:
            print("✗ Opção inválida")

        input("\nPressione ENTER para continuar...")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    print("🌐 Exemplos de API REST - Wi-Fi Sensing")
    print("Certifique-se que o servidor está rodando: python web_server.py")
    menu()
