# LEV Fit Open

Recuperação, engenharia reversa e sistema operacional alternativo (Linux leve) para o leitor **Saraiva LEV Fit** (plataforma Bookeen, Allwinner A13).

**Regra nº 1: a NAND original não é alterada.** Veja [`SEGURANCA.md`](SEGURANCA.md).

## Estado atual

| Marco | Descrição | Estado |
|---|---|---|
| 0 | Relatório de viabilidade | ✅ [`documentation/RELATORIO-VIABILIDADE.md`](documentation/RELATORIO-VIABILIDADE.md) |
| 1 | Executar programa na SRAM do A13 via FEL, sem tocar na NAND | 🟡 Ferramentas prontas e testadas em emulador; **aguardando teste no aparelho** |
| 2 | Kernel mínimo + tela E-Ink | ⏳ Depende do M1, das fotos e do backup da NAND |
| 3 | Touchscreen | ⏳ |
| 4 | Interface gráfica | ⏳ |
| 5 | Leitor + xadrez | ⏳ |

## Começar aqui

1. Ler o [relatório de viabilidade](documentation/RELATORIO-VIABILIDADE.md).
2. Enviar as fotos listadas em [`documentation/hardware/fotos-necessarias.md`](documentation/hardware/fotos-necessarias.md).
3. Executar o [Marco 1](documentation/recovery/01-marco1-fel.md).

## Estrutura

```
documentation/  hardware/ (componentes, fotos) · research/ (fontes, análise do código Bookeen)
                recovery/ (procedimentos) · datasheets/
tools/fel-probe programa bare-metal do Marco 1 + verificador + testes em emulador
scripts/        fel-00-detectar.sh · fel-01-probe.sh · sd-gravar-cartao-fel.sh
bootloader/ kernel/ device-tree/ drivers/{eink,touchscreen,power,input}/ rootfs/
interface/ reader/ chess/ games/   (etapas futuras)
builds/         saídas e logs locais (não versionados)
```

## Licença

Código próprio: GPL-2.0-or-later (compatível com Linux/U-Boot/sunxi-tools). Material de terceiros mantém a licença original.
