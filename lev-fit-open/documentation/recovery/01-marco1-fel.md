# Marco 1: executar código no A13 via FEL, sem tocar na NAND

## O que é alterado

| Onde | Alteração | Permanente? |
|---|---|---|
| Cartão microSD dedicado | ~8 KiB gravados a partir do byte 8192 (`fel-sdboot.sunxi`) | Sim, mas só no **cartão**. Backup dos 64 KiB iniciais é salvo antes. |
| SRAM interna do A13 | 0x2000 (programa, 332 bytes), 0x4000 (64 bytes de resultado), 0x4100 (nonce) | **Não**: apaga ao desligar |
| NAND, DRAM, PMIC, tela | **Nada** | — |

## Riscos e recuperação

- **Risco para o aparelho: nenhum identificado.** O código roda dentro do FEL da BROM, só lê registradores e grava em SRAM volátil. Escrever no registrador de versão da SRAM (bit 15) é um acesso de leitura de ID padrão; o valor original é restaurado.
- Se algo travar: segure o botão liga/desliga por >10 s ou desconecte a bateria e o USB. Nada persiste.
- Risco para o PC: o script do cartão recusa discos não removíveis, discos > 128 GB, discos montados e o disco do sistema, e pede a confirmação `GRAVAR`.

## Pré-requisitos no PC (Linux)

```sh
sudo apt install sunxi-tools python3 usbutils clang lld llvm   # ou gcc-arm-none-eabi
git clone https://github.com/linux-sunxi/sunxi-tools.git        # para obter bin/fel-sdboot.sunxi
# Permitir uso sem root (opcional):
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="1f3a", ATTR{idProduct}=="efe8", MODE="0666"' | \
  sudo tee /etc/udev/rules.d/60-sunxi-fel.rules && sudo udevadm control --reload
```

Compilar e testar o programa (opcional, o binário já está no repositório):

```sh
make -C tools/fel-probe          # gera fel-probe.bin e a listagem .lst
pip install unicorn && make -C tools/fel-probe test   # teste em emulador
```

## Passo a passo

1. **Bateria:** se possível, deixe o aparelho carregando por 30 min antes.
2. **Cartão FEL:** insira um microSD dedicado no leitor do PC e identifique-o com `lsblk` (ex.: `/dev/sdb`).
   ```sh
   sudo scripts/sd-gravar-cartao-fel.sh /dev/sdX sunxi-tools/bin/fel-sdboot.sunxi
   ```
3. Aparelho **desligado**. Insira o cartão FEL no LEV Fit.
4. No PC, rode `lsusb > antes.txt`.
5. Conecte o cabo USB (de dados, não só de carga) ao PC e ligue o aparelho. **A tela E-Ink não deve mudar**: em FEL nada é desenhado.
6. ```sh
   scripts/fel-00-detectar.sh
   ```
   Esperado: `1f3a:efe8` e `soc=00001625(A13)`.
7. ```sh
   scripts/fel-01-probe.sh
   ```
   Esperado: todas as linhas `[OK]` e `RESULTADO GERAL: APROVADO`.
8. Desligue o aparelho e **retire o cartão FEL**.
9. Envie a pasta `builds/fel-logs/<data-hora>/` (o `brom-a13.bin` pode ficar só com você; basta o SHA-256).

## Se não entrar em FEL

| Sintoma | Interpretação | Próximo passo |
|---|---|---|
| Nada aparece em `lsusb` | Cabo só de carga; bateria descarregada; slot não está no MMC0; cartão mal gravado | Trocar cabo; carregar; regravar cartão; testar outro cartão (alguns cartões grandes/SDXC dão problema; prefira ≤ 32 GB) |
| Aparece outro ID (não `1f3a:efe8`) | O sistema original (ou parte dele) está iniciando | Anotar o ID e enviar o `dmesg`; isso é diagnóstico valioso |
| A tela muda / o aparelho reinicia em loop | O boot pela NAND está ocorrendo, ou seja, o cartão não foi lido | Mesmo que acima; depois, UART |
| `sunxi-fel` dá erro de permissão | Regra udev | Usar `sudo` ou a regra acima |

**Não** tente, como alternativa, PhoenixSuit, LiveSuit, PhoenixCard ou "firmware de recuperação" de outro modelo: eles **regravam a NAND inteira**.

## Critério de aceitação

`RESULTADO GERAL: APROVADO`, que comprova ao mesmo tempo:
1. comunicação USB com a BROM;
2. o SoC é um 0x1625 (A13/A10s/R8) com CPU Cortex-A8;
3. código enviado foi **executado** pela CPU: hash da BROM calculado no aparelho = calculado no PC; nonce aleatório transformado corretamente;
4. a NAND não foi acessada (o programa não contém acessos ao controlador NAND; ver `tools/fel-probe/fel-probe.lst`).
