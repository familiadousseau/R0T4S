# Relatório técnico de viabilidade — LEV Fit Open

Versão 1 · 2026-11-15 · Estado: **pré-hardware** (nenhum teste no aparelho ainda; nenhuma foto da placa recebida)

## Convenção de confiabilidade

Cada afirmação é marcada:

| Marca | Significado |
|---|---|
| **[FATO]** | Verificado nesta sessão em fonte primária (código-fonte, repositório, datasheet). A fonte está em `research/fontes.md`. |
| **[DOC]** | Documentado por terceiros (wiki, blog, imprensa), mas não reverificado na fonte primária nesta sessão. |
| **[INFERÊNCIA]** | Dedução lógica a partir de fatos; provável, mas não comprovada no LEV Fit. |
| **[HIPÓTESE]** | Possibilidade técnica que precisa de teste. |
| **[PENDENTE]** | Não pode ser respondido sem fotos/medições do aparelho. |

> **Limitação importante desta versão.** O briefing menciona fotografias da placa, mas **nenhuma imagem foi anexada** à sessão. Além disso, a rede desta sessão bloqueou `linux-sunxi.org` e `blog.soutade.fr`; usei apenas o código-fonte no GitHub (acessível) e resultados de busca. Tudo que depende das fotos está marcado **[PENDENTE]** e a lista exata de fotos necessárias está em `hardware/fotos-necessarias.md`.

---

## Resumo executivo

1. **O projeto é viável**, e o caminho de menor risco existe: a BROM do A13 é uma ROM gravada no silício. Nenhum jailbreak ou NAND corrompida consegue apagá-la, e ela oferece o modo FEL (USB) **[FATO — característica do SoC; ver sunxi-tools]**.
2. **Achado principal do código GPL da Bookeen:** o kernel publicado pela Bookeen tem uma configuração com opção **específica da Saraiva** (`awa13_ff1_defconfig` → `CONFIG_KEYBOARD_SUN4I_KEYBOARD_SARAIVA=y`), com touchscreen **Goodix GT9xx**, PMIC **AXP209** e Wi-Fi BCM4330 como módulos **[FATO]**. Porém essa configuração usa tela **1024×758**, enquanto a imprensa descreve o LEV Fit com **800×600** e sem luz **[DOC]**. Portanto, **ainda não se pode afirmar que `ff1` é o LEV Fit** — pode ser outro modelo Saraiva (ex.: LEV com luz).
3. **A tela E-Ink é o maior desafio.** O A13 **não tem controlador EPD**. A Bookeen aciona o painel *por software*: a CPU calcula os quadros da forma de onda e o controlador LCD (TCON) os envia ao painel como pixels; o PMIC **TI TPS65185** gera as altas tensões e o VCOM **[FATO — `drivers/video/sun5i/disp/de_bsp/de/disp_eink.c`]**. Não existe driver equivalente no Linux mainline **[FATO — não encontrado]**; ele terá de ser escrito, usando o código GPL da Bookeen como referência.
4. **Os arquivos de forma de onda (waveform) do painel estão na NAND** (`/system/waveform.awf` ou `/system/*.bin`) **[FATO — caminhos no código]**. Sem eles a tela não pode ser acionada corretamente. **Isso torna o backup da NAND obrigatório também por razões técnicas**, não só de preservação.
5. O driver do TPS65185 da Bookeen é distribuído **só como objeto binário pré-compilado** **[FATO]**, mas o Linux mainline atual já tem um driver aberto `ti,tps65185` (regulador, 2025) **[FATO]**.
6. Os demais periféricos têm suporte no mainline: AXP209, teclas LRADC, MMC, USB OTG, Goodix, controlador NAND bruto **[FATO]**.
7. **Primeiro procedimento prático (Marco 1):** cartão microSD com `fel-sdboot` → aparelho em FEL → executar o programa `fel-probe` **somente na SRAM interna**. Programa, scripts e verificador **já estão prontos e testados em emulador** (`tools/fel-probe`, `scripts/`).

---

## Respostas às 15 perguntas

### 1. Qual é a arquitetura real do Saraiva LEV Fit?

| Item | Estado | Base |
|---|---|---|
| SoC Allwinner A13 (sun5i, ARM Cortex-A8, ARMv7-A, NEON, ~1 GHz) | [DOC]/[INFERÊNCIA] | Informado pelo usuário; os kernels Bookeen para Saraiva são todos `awa13_*` com `CONFIG_CHIP_ID=1125` **[FATO]**. **Prova definitiva = Marco 1** (o `fel-probe` lê o ID 0x1625 e o MIDR Cortex-A8). |
| RAM 512 MB, barramento de 16 bits | [INFERÊNCIA] | Todas as configs `awa13_*` usam `mem=448M@0x40000000` **[FATO]**, o que é compatível com 512 MB menos 64 MB reservados. O A13 tem barramento DRAM de 16 bits **[DOC]**. Código do chip **[PENDENTE]**. |
| Armazenamento NAND (≈4 GB) com FTL proprietária Allwinner (partições `nanda`, `nandb`…; rootfs `/dev/nandd`) | [FATO] parcial | U-Boot Bookeen: `nand_root=/dev/nandd`, `bootcmd=nand read 50000000 boot; boota` **[FATO]**. Capacidade de 4 GB **[DOC — TechTudo]**. Chip **[PENDENTE]**. |
| Tela E-Ink 6" acionada pelo TCON do A13 + PMIC TPS65185 | [FATO] na família / [INFERÊNCIA] no Fit | Código `disp_eink.c` + `tps65185-i2c`. Resolução do Fit: 800×600 **[DOC — fonte única]**. |
| Touch: capacitivo Goodix GT9xx **ou** outro | [HIPÓTESE] | `ff1` habilita GT9xx, Cypress CTM340 e "CTPTS" como módulos **[FATO]**. Qual está no Fit: **[PENDENTE]**. |
| PMIC principal AXP209 | [INFERÊNCIA] | `CONFIG_AW_AXP20=y` em `ff1` **[FATO]**; todas as configs têm `CONFIG_AW_AXP=y`. |
| Botões físicos via LRADC (ADC de teclas do A13) | [FATO] na variante Saraiva | `sun4i-keyboard.c` lê `LRADC_ADC0`; a variante Saraiva usa o código de tecla 0x05 para um botão especial. |
| Console serial `ttyS0`, 115200 8N1 | [FATO] | `CONFIG_CMDLINE` das configs. Pinos no Fit **[PENDENTE]**. |

### 2. Quais componentes podem ser identificados pelas fotografias?

**Nenhum ainda: nenhuma foto foi recebida.** A tabela completa de componentes, com os campos pedidos (fabricante, código, datasheet, função, interface, tensão, suporte Linux, recuperação), está em `hardware/componentes.md`, preenchida com o que já é fato e com as lacunas **[PENDENTE]**. A lista de fotos necessárias (incluindo ângulos e a etiqueta do flat da tela) está em `hardware/fotos-necessarias.md`.

### 3. Qual é a memória NAND instalada?

**[PENDENTE]** O código do chip só pode vir da foto. Fatos já conhecidos:
- O sistema Bookeen usa o **driver NAND proprietário da Allwinner** (`CONFIG_SUN5I_NANDFLASH=y`), com uma FTL própria por cima da NAND bruta **[FATO]**.
- O `boot0` e o `boot1` (carregadores Allwinner) ficam nos primeiros blocos da NAND, gravados com aleatorizador e ECC próprios **[DOC]**.
- Consequência: haverá **dois tipos de backup**. O *bruto* (páginas + OOB, cópia física exata) e o *lógico* (partições `nanda…`, legíveis por arquivo). Detalhes em `recovery/02-plano-backup-nand.md`.

### 4. Qual é o controlador da tela E-Ink?

**[FATO, na família Bookeen A13]** Não há um "controlador EPD" dedicado:
- **Temporização e dados:** o **TCON (controlador LCD) do A13** envia quadros em que cada "pixel" de 32 bits mistura os dados da fonte (source driver) e os sinais de controle do painel. O código monta palavras como `data | 0xD08000 | 0xff030303` (`disp_eink.c`, linhas 796–1117).
- **Forma de onda:** é calculada pela CPU, com tabelas por temperatura. Há suporte a painéis **OED (E Ink)** e **PVI**, e modos INIT, GC16, GC4, DU e A2.
- **Alimentação, VCOM e temperatura:** **TI TPS65185** pelo I²C (`tps65185_vcom_set`, `papyrus_set_vcom2`).
- **Modelo do painel, resolução real, VCOM do lote:** **[PENDENTE]**. Normalmente estão impressos na etiqueta do flat da tela, então é preciso fotografá-la.

### 5. Qual é o controlador touchscreen?

**[PENDENTE]**. Há três candidatos documentados no código Bookeen para a configuração Saraiva (`ff1`): **Goodix GT9xx** (`drivers/input/touchscreen/gt9xx/`), **Cypress CTM340** e um driver genérico "CTPTS". Também é possível que o Fit use outra tecnologia (ex.: infravermelho). Não presumo nenhum deles. A identificação virá:
1. da foto do chip no flat do digitalizador;
2. de uma varredura **somente leitura** do barramento I²C no Marco 2 (`i2cdetect -r`). O endereço 0x5D/0x14 apontaria para Goodix **[DOC]**.

### 6. Existe suporte Linux para os componentes?

| Componente | Linux mainline (verificado no `master`, versão 7.4-rc2) | Legado (Bookeen 3.0) |
|---|---|---|
| A13: CPU, clocks, pinos, UART, I²C, MMC, USB OTG (musb) | Sim (`sun5i-a13.dtsi`) **[FATO]** | Sim |
| AXP209 (PMIC, bateria, carregador) | Sim (`axp20x`, `axp20x_battery`) **[FATO]** | Sim |
| Teclas no LRADC | Sim (`sun4i-lradc-keys`) **[FATO]** | Sim (`sun4i-keyboard`) |
| Goodix GT9xx (se confirmado) | Sim (`goodix.c`) **[FATO]** | Sim |
| TPS65185 | Sim, como regulador (`ti,tps65185`, 2025) **[FATO]** | Só binário fechado |
| Controlador NAND (acesso bruto) | Sim (`sunxi_nand.c`, MTD) **[FATO]** | — |
| FTL Allwinner (`nanda…`) | **Não** | Sim (driver proprietário) |
| **E-Ink via TCON** | **Não** (nenhum driver EPD para Allwinner encontrado) | Sim (código GPL) |
| U-Boot: SPL do A13, boot por FEL e SD | Sim (ex.: `A13-OLinuXino_defconfig`) **[FATO]** | U-Boot 2011 sem SPL (usa boot0/boot1 fechados) |

### 7. É possível acessar o modo FEL?

**Sim, com alta probabilidade.** O FEL está na BROM, e a BROM não é afetada pelo jailbreak **[FATO]**. Formas de entrar, em ordem de preferência:

1. **Cartão microSD com `fel-sdboot.sunxi`** (sunxi-tools). Não exige abrir o aparelho nem soldar. A Bookeen Muse é documentada como "entra em FEL com cartão SD especial" **[DOC — linux-sunxi]**.
2. **Comando no console serial** do boot1/U-Boot original (ex.: tecla durante o boot, `efex`). Em um Bookeen Notea, a documentação cita "enviar `2` pela UART" **[DOC]**. No LEV Fit isso é **[HIPÓTESE]** e exige a UART.
3. **Botão ou ponto de teste "FEL/uboot"** na placa: **[PENDENTE]** (fotos e, possivelmente, medição).
4. **Queda automática para FEL** quando nenhuma mídia é inicializável. **Não usar**, porque isso exigiria invalidar o boot0 na NAND.

### 8. É possível utilizar um cartão SD para entrar em FEL?

**Sim, se o slot microSD estiver ligado ao controlador MMC0 do A13**, que é o primeiro dispositivo consultado pela BROM, antes da NAND **[DOC — linux-sunxi/BROM; U-Boot: "a BROM procura a imagem no setor 16 (8 KiB) do SD no primeiro controlador MMC"]**. É **[INFERÊNCIA]** forte que esteja no MMC0, porque o método é documentado para a Muse. **O próprio teste do Marco 1 prova isso:** se o aparelho aparecer como `1f3a:efe8` com o cartão inserido, o slot está no MMC0.

O cartão FEL **não** contém sistema operacional. São só ~8 KiB que mandam a BROM para a rotina FEL. Isso é diferente da pergunta 9.

### 9. É possível inicializar um sistema pelo microSD?

**Sim, sob a mesma condição da pergunta 8 [INFERÊNCIA forte].** Se a BROM lê o SD antes da NAND, um cartão com **U-Boot SPL mainline + U-Boot + kernel + DTB + rootfs** inicializa sem tocar na NAND. Com o cartão removido, o aparelho volta ao sistema original (ou ao estado atual). Pré-requisitos:
- **Parâmetros da DRAM** para o SPL: começar com valores conservadores e, depois, extrair os valores exatos do `boot0`/`script.bin` originais lidos no backup.
- Enquanto isso não estiver validado, a alternativa é **carregar tudo pela RAM via FEL** (`sunxi-fel uboot …`, `write` do kernel/initramfs), igualmente sem tocar na NAND (Marco 2).

### 10. É possível executar código diretamente na RAM?

- **SRAM interna (48 KiB):** sim, logo após entrar em FEL. É exatamente o Marco 1, e o programa está pronto **[FATO — testado em emulador Cortex-A8]**.
- **DRAM (512 MB):** sim, depois que um SPL inicializa o controlador DRAM (também pelo FEL, só em RAM). Isso responde ao item "identificar a quantidade de RAM", que **só pode ser medida após a inicialização da DRAM** (o SPL mainline detecta o tamanho). Isso é o início do Marco 2.

### 11. Qual distribuição Linux seria mais adequada?

**Buildroot (versão LTS vigente) + Linux mainline LTS + U-Boot mainline + BusyBox**, imagem própria e sem gerenciador de pacotes. Justificativa:
- reprodutível e documentada, com configuração em arquivos versionáveis no Git;
- rootfs de poucos MB, boot de poucos segundos, nada de systemd/Xorg;
- suporte nativo a toolchain ARMv7 hard-float com NEON (Cortex-A8).

A escolha da libc (glibc × musl) fica para o Marco 4, depois de medir o MuPDF e o motor de xadrez. **Descartado:** Debian, Armbian e Alpine (pesados e desnecessários) e o kernel Bookeen 3.0 como base definitiva (antigo, Android, blobs). O kernel legado será usado **só como ferramenta** de backup lógico, se necessário.

### 12. Quais drivers precisam ser desenvolvidos?

| Driver | Trabalho | Complexidade |
|---|---|---|
| **EPD via TCON do A13** (DRM/fbdev + motor de forma de onda + atualização parcial + temperatura) | Escrever do zero, guiado por `disp_eink.c` (GPL) | **Muito alta** |
| Parser do formato `.awf` (ou `.bin`) da Bookeen | Engenharia reversa a partir do código GPL que o carrega | Média |
| Device Tree da placa LEV Fit | Escrever (pinos, I²C, regulador, teclas, touch) | Média |
| Integração do TPS65185 (VCOM, sequência de energia, sensor de temperatura) | Adaptar driver mainline | Média |
| Touchscreen | Só DT, se for Goodix; driver novo, se for algo sem suporte | Baixa a alta |
| Leitor da FTL Allwinner em espaço de usuário (para o backup lógico **sem** o driver legado) | Opcional | Alta |
| Suspensão/retomada com a tela "congelada" | Integração | Média |

### 13. Quais projetos existentes podem ser aproveitados?

- **sunxi-tools** (FEL, `fel-sdboot`, `nand-part`, `meminfo`): Marco 1 e backup.
- **U-Boot mainline**: SPL para A13, boot por FEL e SD.
- **Linux mainline**: todos os periféricos, exceto o EPD.
- **BOOKEEN/kernel-linux-3.0 e BOOKEEN/u-boot-2011 (GPL)**: referência para EPD, teclas, pinagem e sequência do TPS65185. Também é uma ferramenta de backup lógico (com cuidado, ver riscos).
- **Buildroot / BusyBox**: sistema base.
- **LVGL** (interface): leve, em C, sem servidor gráfico, com *flush* por região (ótimo para atualização parcial de E-Ink) e tema monocromático.
- **MuPDF** (EPUB/PDF) ou **crengine** (EPUB/TXT). Alternativa completa: **KOReader** (leitor maduro para E-Ink; exigiria um porte de "device", e não há porte oficial conhecido para Bookeen, ver issue koreader#6043).
- **Stockfish** (ou motor mais leve), com interface própria.

Para o EPD, a abordagem de *drivers EPD por software* existe em outros SoCs (Rockchip EBC, EPDC do i.MX). Nenhum dos dois está no mainline nos caminhos verificados, mas servem como referência de arquitetura **[HIPÓTESE de utilidade]**.

### 14. Quais são os riscos técnicos?

| Risco | Prob. | Impacto | Mitigação |
|---|---|---|---|
| Waveform irrecuperável (NAND ilegível) | Média | **Crítico** para a tela | Backup bruto + lógico antes de tudo. Plano B: waveform genérica do mesmo tipo de painel (qualidade inferior). |
| VCOM/sequência de tensão errados danificam o painel | Baixa | Alto | Usar valores lidos do painel/NAND; limitar tensões no DT; testar com quadros curtos. |
| Driver Allwinner NAND legado **grava** metadados ao inicializar (FTL) | **Média** | Alto | Fazer **primeiro o backup bruto** com o MTD mainline marcado como somente leitura; usar o driver legado só depois e sobre o backup. |
| Slot SD não está no MMC0 | Baixa | Médio | Entrar em FEL por UART/botão; carregar tudo via USB. |
| Parâmetros de DRAM incorretos no SPL | Média | Baixo (só não inicializa; nada é gravado) | Começar conservador; extrair do boot0 original. |
| Bateria descarregada/instável | Média | Médio | Testar ligado ao USB; medir a tensão da bateria. |
| UART inexistente ou não sinalizada | Média | Médio | Medir com multímetro, sem nunca aplicar tensão desconhecida. |
| Usar PhoenixSuit/LiveSuit ou firmware de outro modelo | — | **Destrutivo** | **Proibido** sem backup e autorização (ver `SEGURANCA.md`). |
| Desempenho de PDF e Stockfish no Cortex-A8 | Média | Baixo | Medir; limitar profundidade/tempo; motor mais leve. |

### 15. Qual é o primeiro procedimento prático de recuperação?

**Marco 1, totalmente não destrutivo** (passo a passo em `recovery/01-marco1-fel.md`):

1. No PC Linux: instalar `sunxi-tools`, `python3` e `clang lld llvm` (ou `gcc-arm-none-eabi`).
2. Preparar um microSD **dedicado** com `scripts/sd-gravar-cartao-fel.sh`. Só o cartão é alterado.
3. Aparelho desligado: inserir o cartão, ligar o cabo USB ao PC e ligar o aparelho.
4. `scripts/fel-00-detectar.sh`: precisa mostrar `1f3a:efe8` e `soc=00001625(A13)`.
5. `scripts/fel-01-probe.sh`: carrega o `fel-probe` na SRAM, executa, lê o resultado e confere hash da BROM, nonce, MIDR, ID do SoC e SID. Salva o log com SHA-256.
6. Desligar (a SRAM se apaga) e remover o cartão.

**Critério de sucesso do Marco 1:** `RESULTADO GERAL: APROVADO`.

---

## Estimativa de complexidade por etapa

| Etapa | Complexidade | Principal incerteza | Dependência |
|---|---|---|---|
| M1 — FEL + programa na SRAM | **Baixa** | Slot SD no MMC0 / estado da bateria | Nenhuma (pronto) |
| M1b — Fotos e identificação de componentes | Baixa | Inscrições legíveis | Usuário |
| M2a — SPL + DRAM via FEL; medir RAM | Média | Parâmetros de DRAM | M1 |
| M2b — Kernel mínimo + initramfs via FEL, console UART | Média | Achar a UART | M2a |
| M2c — **Backup bruto da NAND** (+SHA-256) | Média | Geometria da NAND/ECC | M2b |
| M2d — Backup lógico (`nanda…`), extração da waveform | Alta | FTL proprietária | M2c |
| M2e — **Driver EPD** (primeira imagem na tela) | **Muito alta** | Mapeamento de sinais, waveform | M2d |
| M3 — Touchscreen | Baixa a alta | Qual controlador é | M2b |
| M3b — Boot autônomo pelo microSD | Média | DRAM, DT | M2a |
| M4 — Interface (LVGL) | Média | Estratégia de atualização parcial | M2e, M3 |
| M5a — Leitor (EPUB/TXT, depois PDF) | Média a alta | Desempenho do PDF | M4 |
| M5b — Xadrez + motor | Média | Força × tempo × bateria | M4 |
| Energia (suspensão, bateria) | Média a alta | Retomada do EPD/TCON | M2e |
| Jogos e utilitários extras | Baixa a média cada | — | M4 |

---

## Próxima etapa proposta

1. **Usuário:** enviar as fotos listadas em `hardware/fotos-necessarias.md` e descrever o estado atual (o que aparece na tela, se carrega, se o PC detecta algo via USB ao ligar, qual jailbreak foi feito e em que passo falhou).
2. **Usuário:** executar o Marco 1 e enviar a pasta `builds/fel-logs/<data>/`.
3. **Projeto (após M1 aprovado):** preparar o Marco 2a: SPL mainline para A13 carregado via FEL, sem suporte a NAND compilado, para detectar a RAM.

Nenhuma operação que grave na NAND será proposta antes do backup completo e de sua autorização expressa.
