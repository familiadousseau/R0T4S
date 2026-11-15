# Inventário de componentes — Saraiva LEV Fit

Estado: **sem fotos recebidas**. Marcas: [FATO] [DOC] [INFERÊNCIA] [HIPÓTESE] [PENDENTE] (ver o relatório de viabilidade).
Regra: **nenhum código de peça é preenchido sem leitura direta na placa.** Os candidatos ficam na coluna "Indícios".

| # | Componente | Fabricante / código | Indícios disponíveis | Função | Interface | Tensão | Linux | Recuperação/substituição |
|---|---|---|---|---|---|---|---|---|
| 1 | SoC | Allwinner **A13** [DOC/usuário]; marcação **[PENDENTE]** | Configs Bookeen `awa13_*`, `CONFIG_CHIP_ID=1125` [FATO] | CPU Cortex-A8, TCON, MMC, USB, LRADC, NAND | — | Núcleo ~1,2 V; E/S 3,3 V [DOC] | Mainline `sun5i-a13.dtsi` [FATO] | BROM em ROM, FEL sempre disponível |
| 2 | RAM | Samsung, código **[PENDENTE]** | `mem=448M` → 512 MB [INFERÊNCIA]; A13 tem barramento de 16 bits | Memória principal | DDR2/DDR3 [PENDENTE] | 1,5 V se DDR3 [DOC] | Init. via SPL do U-Boot mainline | Parâmetros a extrair do `boot0` |
| 3 | NAND | **[PENDENTE]** | ~4 GB [DOC]; FTL Allwinner [FATO] | Armazenamento interno | NAND paralela (barramento NAND do A13) | 3,3 V típico [DOC] | Bruto: `sunxi_nand` (MTD) [FATO]; FTL: só no driver legado | Backup bruto + lógico; leitura externa (gravador TSOP48) só em último caso |
| 4 | Controle E-Ink | **Não há chip EPD dedicado** [FATO, família]: TCON do A13 + software | `disp_eink.c` | Gera os quadros da forma de onda | RGB paralelo do TCON reaproveitado | 3,3 V lógica | **Sem driver mainline** | Escrever driver (Marco 2e) |
| 4a | PMIC do EPD | TI **TPS65185** [FATO, família]; presença no Fit **[PENDENTE]** | Driver `tps65185-i2c` (binário) | VPOS/VNEG/VGH/VGL, VCOM, sensor de temperatura | I²C + GPIOs (WAKEUP, PWRUP, VCOM_CTRL, PWR_GOOD, INT) [DOC] | Entrada 3–6 V; saídas ±15 V, +22/−20 V; VCOM 0 a −5,1 V [DOC — datasheet TI] | Mainline `ti,tps65185` (regulador) [FATO] | Datasheet: https://www.ti.com/lit/gpn/tps65185 |
| 4b | Painel E-Ink | **[PENDENTE]** (etiqueta no flat) | 6", 800×600 [DOC, fonte única] | Display | FPC de 34/39 pinos [PENDENTE] | Fornecidas pelo TPS65185 | Depende do driver 4 | VCOM do lote costuma vir na etiqueta |
| 5 | Touchscreen | **[PENDENTE]** | Config `ff1`: Goodix GT9xx / Cypress CTM340 / CTPTS [FATO] | Entrada por toque | I²C + INT + RESET [HIPÓTESE] | 3,3 V [HIPÓTESE] | Goodix: mainline `goodix.c` [FATO] | Identificar antes de tudo |
| 6 | PMIC principal | X-Powers **AXP209** [INFERÊNCIA a partir de `CONFIG_AW_AXP20=y`]; marcação **[PENDENTE]** | — | Reguladores, carregador, medição da bateria, botão liga | I²C (endereço 0x34 [DOC]) + IRQ (NMI) | Entrada USB 5 V / bateria | Mainline `axp20x` [FATO] | Não reprogramar tensões fora da faixa do DT de referência |
| 7 | USB | PHY interno do A13 (USB0 OTG) [FATO, config] | `USB_SW_SUN5I_USB0_OTG=y` | FEL, gadget, carga | USB 2.0 | 5 V VBUS | Mainline `musb` (sunxi) | — |
| 8 | Slot microSD | **[PENDENTE]**: controlador (MMC0?) | Método FEL-SD documentado para a Muse [DOC] | Boot alternativo, dados | SD 4 bits | 3,3 V | Mainline `sunxi-mmc` | Teste do Marco 1 confirma o MMC0 |
| 9 | UART de depuração | Pinos **[PENDENTE]**; Muse: 4 ilhas `3V3/TX/RX/GND` [DOC] | `console=ttyS0,115200` [FATO] | Console do boot/kernel | UART TTL **3,3 V** | 3,3 V (NÃO ligar o VCC do adaptador) | — | Medir com multímetro; nunca injetar tensão |
| 10 | Pontos de teste de boot (FEL/uboot) | **[PENDENTE]** | — | Forçar FEL | GPIO/BROM | — | — | Usar o cartão FEL antes de qualquer ponte |
| 11 | Wi-Fi | **[PENDENTE]** (o Fit tem Wi-Fi?) | `CONFIG_BCM4330=m` em `ff1` [FATO] | Rede | SDIO [HIPÓTESE] | — | `brcmfmac` (mainline) se for BCM4330 | Não é necessário ao projeto |
| 12 | Bateria | **[PENDENTE]** (etiqueta: mAh, química) | — | Energia | — | 3,7 V nom. Li-ion/Li-Po [HIPÓTESE] | `axp20x_battery` | Medir tensão antes dos testes |
| 13 | Botões | Rede resistiva no LRADC [FATO, variante Saraiva] | `sun4i-keyboard.c` (ADC0) | Navegação | ADC | ~2 V ref. [DOC] | Mainline `sun4i-lradc-keys` [FATO] | Calibrar os níveis no DT a partir das leituras |
