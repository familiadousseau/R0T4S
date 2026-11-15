# Fotos e informações necessárias

Para preencher `componentes.md` sem inventar referências, preciso de:

## Fotos (luz difusa, sem flash direto, foco nas inscrições; de preferência >= 12 MP)

1. **Placa inteira, frente e verso**, com todos os conectores visíveis.
2. **Close de cada chip**, com a inscrição legível. Se o reflexo atrapalhar, incline a luz ~45°:
   - SoC (Allwinner);
   - chip(s) de RAM Samsung;
   - NAND (geralmente TSOP-48 retangular ou BGA);
   - chip próximo ao conector do flat da tela (esperado: TI TPS65185, marcação curta, ex. "TPS65185" ou um código de 4–6 caracteres);
   - PMIC próximo ao conector da bateria/USB (esperado: AXP209);
   - qualquer chip no **flat do touchscreen** ou próximo ao seu conector;
   - chip Wi-Fi/módulo, se houver.
3. **Etiqueta do flat (FPC) da tela E-Ink**: modelo do painel (ex. "ED060…"), lote e, se houver, a **tensão VCOM** (ex. "-1.56V").
4. **Etiqueta da bateria** (mAh, tensão, química).
5. **Ilhas/pontos de teste** sem componente, especialmente grupos de 3–4 ilhas alinhadas (possível UART) e ilhas marcadas `TX`, `RX`, `GND`, `3V3`, `FEL`, `UBOOT`, `BOOT`, `RECOVERY`.
6. **Serigrafia da placa** (código como `AWA13-…`, `V1.x`, data). Isso permite associar a placa à config correta do kernel Bookeen (`awa13_ff1`, `awa13_l_l`, …).
7. Slot microSD e conector USB, mostrando as trilhas próximas, se visíveis.

## Informações sobre o estado atual

- O que acontece ao ligar: tela muda? fica congelada? LED? vibra?
- O aparelho carrega (indicador de carga)?
- Ao ligar com o cabo no PC, o PC detecta algo? Rode `lsusb` antes e depois e envie as duas saídas, e também `dmesg | tail -30`.
- Qual jailbreak foi aplicado (link ou nome), quais arquivos foram copiados e em que passo falhou.
- Versão do firmware original (se lembrar).
- Etiqueta traseira: modelo, número de série (pode mascarar parte) e data.
