# Registro de alterações

## 2026-11-15: Marco 0 (viabilidade) e ferramentas do Marco 1
- Estrutura do projeto criada.
- Relatório de viabilidade, inventário de componentes (pendente de fotos), fontes e análise do código GPL da Bookeen.
- `tools/fel-probe`: programa bare-metal para SRAM do A13 (332 bytes), verificador e testes no emulador Unicorn (Cortex-A8). Todos os testes passaram.
- Scripts: detecção FEL, execução do probe, gravação segura do cartão FEL.
- Ainda **não testado no aparelho**.
