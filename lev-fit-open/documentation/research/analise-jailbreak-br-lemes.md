# Análise do jailbreak aplicado: br-lemes/lev-jailbreak

Repositório: https://github.com/br-lemes/lev-jailbreak (último commit `0c49c58`, 2017-03-03). Lido na íntegra em 2026-11-17.

## O que ele faz [FATO, Makefile]

1. Baixa o firmware oficial `CybUpdate.bin` por `http://bit.do/atualizarlev` (link da Saraiva, hoje fora do ar).
2. Monta o `rootfs.fex` e copia para dentro dele o Dropbear (SSH), `S99dropbear.sh` e `levtogglesn`.
3. **Reescreve o arquivo `contents`** declarando três entradas para gravar:
   `LOAD|bootloader.fex|…|6`, `BOOT|boot.fex|…|10`, `ROOT|rootfs.fex|…|11`.
4. Empacota tudo como `lev-jailbreak.bin`, que é instalado pelo atualizador do próprio aparelho.

Consequência: o jailbreak **regrava a partição de bootloader (configuração de hardware: tela, touch, pinos), o kernel e o sistema**. Não grava a partição `/priv` (`nande`), onde ficam a identidade do aparelho, a waveform e o VCOM, segundo bruthethe/saraiva-lev-koreader, `docs/RECOVERY.md`.

`levtogglesn` troca o prefixo do número de série entre `SA615` (Saraiva LEV) e `BK646` (Cybook Muse) via `nvram -S` e reinicia o leitor (`boordr`).

## Relação com os sintomas do LEV Fit [INFERÊNCIA]

O autor usava um **LEV com luz** (issue #1). O firmware baixado era o da Saraiva para o LEV. Sintomas no Fit:

- imagem com listras e fora da margem → configuração de tela de outro painel (LEV: 1024×758; Fit: 800×600 [DOC]);
- touch sem resposta e travamento após o logo → driver/configuração de touch de outro modelo e/ou leitor que não inicia.

Ambos são explicados por um `bootloader.fex`/`boot.fex` de outro modelo gravado à força no Fit.

## Relatos de terceiros (issue #1, 2017–2026) [DOC]

- Vários LEV com luz (CYBOY4F-SA / CYBOY4S-SA) perderam o touch após atualização oficial; um relatou correção com o firmware Bookeen `fw_oem/.../Cybupdate20180212_2643/CYBOY4F-SA/CybUpdate.bin` (MD5 informado `D224E4CBDA0F8868182CCF8F5B58FC12`); outros não.
- Firmware de Muse HD instalado em LEV com luz → tela preta (brick).
- Segurar o botão do meio com USB ligado leva ao modo `1f3a:efe8` (FEL).
- Recuperação de aparelho travado em "Iniciando" com `CybUpdate.bin` no cartão SD (Oitalao/Jailbreak-Saraiva-Lev, Parte 3): o atualizador (`/etc/init.d/S42check_update.sh`) roda **antes** do leitor e procura `CybUpdate.bin` no microSD.
- **Nenhum link de firmware específico do LEV Fit** foi publicado no tópico.

## Próximo passo

1. Ler o modelo (`CYB…-SA`) e o prefixo do número de série na etiqueta traseira do Fit.
2. Inspecionar (somente leitura, no PC) o `CybUpdate/bootloader.fex` que o jailbreak usou, para confirmar a resolução e o touch configurados.
3. Obter o firmware correto do Fit antes de qualquer regravação; não usar firmwares de LEV com luz, Neo ou Muse HD.
