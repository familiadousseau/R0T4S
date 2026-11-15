# Fontes consultadas

Data da consulta: 2026-11-15. "Verificado" = conteúdo lido diretamente nesta sessão.

## Código-fonte (verificado)

| Projeto | URL | Versão consultada | Uso no projeto |
|---|---|---|---|
| Kernel Bookeen (GPL) | https://github.com/BOOKEEN/kernel-linux-3.0 | commit `0aeda9a8538f`, 2016-03-11 (repositório tem um único commit) | Referência: EPD, teclas Saraiva, configs `awa13_*`, TPS65185 |
| U-Boot Bookeen (GPL) | https://github.com/BOOKEEN/u-boot-2011 | commit `cfd01dfbe12c`, 2016-03-11 | Referência: layout de boot na NAND, comandos |
| sunxi-tools | https://github.com/linux-sunxi/sunxi-tools | commit `34dfa20`, 2026-11-05 | FEL, `fel-sdboot.sunxi` (SHA-256 `2ccec08a…bc808bc`, 8192 bytes), mapa de SRAM do A13 |
| Linux mainline | https://github.com/torvalds/linux | `master` = 7.4-rc2 | Verificada a existência de: `drivers/regulator/tps65185.c`, `drivers/input/touchscreen/goodix.c`, `drivers/input/keyboard/sun4i-lradc-keys.c`, `drivers/mtd/nand/raw/sunxi_nand.c`, `arch/arm/boot/dts/allwinner/sun5i-a13.dtsi`, `drivers/mfd/axp20x.c`, `drivers/power/supply/axp20x_battery.c` |
| U-Boot mainline | https://github.com/u-boot/u-boot | `master` | Verificada a existência de `configs/A13-OLinuXino_defconfig` e `drivers/mtd/nand/raw/sunxi_nand_spl.c`; **não existe** config para Bookeen |

Verificado como **ausente** no `master` do Linux: `drivers/gpu/drm/imx/epdc/`, `drivers/gpu/drm/mxc-epdc/`, `drivers/gpu/drm/rockchip/rockchip_ebc.c` (drivers EPD por software de outros SoCs; só verifiquei esses caminhos).

## Documentação de terceiros (não reverificada: host bloqueado nesta sessão)

| Fonte | URL | O que diz (segundo o buscador) |
|---|---|---|
| linux-sunxi: Bookeen Cybook Muse | https://linux-sunxi.org/Bookeen_Cybook_Muse | A13; EPD acionado com TPS65185; driver de tela "só software"; UART em 4 pinos 3V3/TX/RX/GND; root sem senha no console; FEL com cartão SD especial; não suportado no mainline |
| linux-sunxi: Bookeen Notea | https://linux-sunxi.org/Bookeen_Notea | UART G/R/T/V; FEL enviando `2` pela UART a 115200 |
| linux-sunxi: FEL, BROM, A13 | https://linux-sunxi.org/FEL · https://linux-sunxi.org/BROM · https://linux-sunxi.org/A13 | Ordem de boot da BROM e métodos de FEL (a reconsultar quando o host estiver acessível) |
| Blog G. Soutadé — "GAME_OVER" | https://blog.soutade.fr/post/2015/03/game_over.html | Saraiva LEV usa o mesmo firmware da Bookeen; display via `/dev/disp` e `/dev/fb0` |
| Blog G. Soutadé — custom ROM Cybook | https://blog.soutade.fr/post/2015/07/how-to-make-custom-rom-for-cybook-e-readers.html | Estrutura de firmware Cybook; erros ao compilar kernel e U-Boot da Bookeen |
| KOReader issue #6043 | https://github.com/koreader/koreader/issues/6043 | Bookeen Saga sem porte oficial |
| TechTudo (2018) | https://www.techtudo.com.br/noticias/2018/11/saraiva-lev-saiba-especificacoes-e-precos-de-e-readers-a-venda-no-brasil.ghtml | LEV Fit: 6", 800×600, sem luz, 4 GB, 130 g, touch (**fonte única**) |
| Tecnoblog (review do LEV) | https://tecnoblog.net/testamos/saraiva-lev-review/ | LEV original: 1024×758, projeto Bookeen |
| MobileRead | https://www.mobileread.com/forums/showthread.php?t=258427 | Atualizações Muse/Odyssey |

## Datasheets

| Componente | Link | Estado |
|---|---|---|
| TI TPS65185 | https://www.ti.com/lit/gpn/tps65185 | Link citado no driver mainline; presença no Fit pendente |
| Allwinner A13 (datasheet / user manual) | via https://linux-sunxi.org/A13 | A obter |
| X-Powers AXP209 | via linux-sunxi | A obter (presença inferida) |
| RAM, NAND, touch, painel | — | Dependem das fotos |

## Ações para quando houver acesso a `linux-sunxi.org`

1. Ler as páginas Muse/Notea/BROM/FEL na íntegra e substituir as marcas [DOC] por [FATO] quando confirmadas.
2. Baixar os datasheets do A13 e do AXP209 para `documentation/datasheets/`, com SHA-256.
