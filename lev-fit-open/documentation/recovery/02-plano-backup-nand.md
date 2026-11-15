# Plano de backup da NAND (Marco 2c/2d): rascunho, NÃO executar ainda

Pré-condição: Marco 1 aprovado, chip NAND identificado pela foto e UART funcionando.

## Princípios

1. **Nada que possa gravar entra em execução.** U-Boot compilado **sem** `CMD_NAND`/`CMD_NAND_TORTURE`; kernel com o nó NAND usando uma partição única **`read-only`** no DT.
2. **Backup bruto antes do lógico.** O driver legado da Allwinner (FTL) pode atualizar tabelas internas ao montar; por isso ele só entra depois de existir uma cópia física.
3. Todo arquivo recebe **SHA-256** no momento da criação, e cada leitura é feita **duas vezes**, com comparação dos hashes (detecta bits instáveis).

## Fase A: backup bruto (cópia física)

```
PC --FEL--> U-Boot SPL+U-Boot (só RAM) --> kernel mainline + initramfs (só RAM)
            kernel: sunxi_nand com partição única read-only
            initramfs: mtd-utils (nanddump), sha256sum
destino: microSD (ext4/exFAT) ou USB gadget (mass-storage/ethernet) para o PC
```

Comandos previstos (no aparelho):
```sh
nanddump --noecc --oob -f /mnt/sd/nand-raw-1.bin /dev/mtd0   # páginas + OOB, sem correção
nanddump --noecc --oob -f /mnt/sd/nand-raw-2.bin /dev/mtd0
sha256sum /mnt/sd/nand-raw-*.bin
```
Também salvar `mtdinfo -a`, o ID ONFI/JEDEC da NAND e o log completo do kernel.

## Fase B: backup lógico

- Opção 1: kernel legado (Allwinner 3.0/3.4 com `nand.ko`) via FEL, partições `nanda…` expostas e lidas com `dd`, **sem montar**. Risco: escritas da FTL ao inicializar (mitigado pela Fase A).
- Opção 2 (preferível a longo prazo): reconstruir a FTL a partir da imagem bruta, no PC, com uma ferramenta própria (`tools/`). Zero risco ao aparelho.

Itens a extrair: `boot0`/`boot1` (parâmetros de DRAM), `script.bin` (pinagem, I²C do touch e do TPS65185), partição `boot` (kernel original), `/system/waveform.awf` ou `/system/*.bin` (**waveform do painel**), dados do usuário.

## Alternativa externa (último recurso)

Remover a NAND (TSOP-48) e ler em gravador. Só se a leitura in-circuit falhar. Exige solda e retrabalho, com risco físico. Requer autorização expressa.
