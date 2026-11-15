# Regras de segurança e preservação (obrigatórias)

## Proibido sem autorização expressa e backup verificado

- Apagar, formatar ou gravar a NAND (incluindo PhoenixSuit, LiveSuit, PhoenixCard, `sunxi-fel` com `spiflash`/`nand`, `nand erase`/`write` no U-Boot e `flash_erase`/`nandwrite` no Linux).
- Usar firmware de outro modelo (mesmo Bookeen) sem verificar a compatibilidade.
- Fazer pontes em contatos não identificados ou aplicar tensões desconhecidas. Na UART, **nunca** ligar o VCC do adaptador.
- Substituir drivers ou alterar tensões do PMIC (AXP209/TPS65185) fora de valores documentados.

## Antes de qualquer operação potencialmente destrutiva, documentar

1. O que será alterado.
2. Por que será alterado.
3. Quais são os riscos.
4. Como recuperar em caso de falha.
5. Qual backup é necessário (com SHA-256 conferido).

E então **pedir autorização expressa** ao dono do aparelho.

## Salvaguardas técnicas adotadas no projeto

- Os scripts do Marco 1 só gravam na SRAM volátil e abortam se o SoC não for 0x1625.
- O script do cartão SD recusa discos fixos, montados, > 128 GB ou o disco do sistema, salva os 64 KiB iniciais e exige digitar `GRAVAR`.
- Builds futuros de U-Boot e kernel para testes terão o suporte a escrita na NAND **desabilitado em compilação**, e a NAND será declarada `read-only` no Device Tree.
