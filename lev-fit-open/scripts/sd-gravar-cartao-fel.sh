#!/usr/bin/env bash
# LEV Fit Open — preparar um cartão microSD que força o A13 a entrar em FEL.
#
# ALTERA SOMENTE O CARTÃO microSD indicado (nunca o aparelho).
# Grava o fel-sdboot.sunxi (sunxi-tools, ~512 bytes, cabeçalho eGON.BT0)
# no deslocamento de 8 KiB do cartão, onde a BROM do A13 procura um
# carregador. Esse programa só salta para a rotina FEL da própria BROM.
#
# A área 8 KiB–(8 KiB + tamanho) normalmente fica ANTES da 1ª partição
# (que costuma começar em 1 MiB), então partições/arquivos do cartão não
# são afetados — mas use, de preferência, um cartão dedicado e vazio.
#
# Uso: sudo scripts/sd-gravar-cartao-fel.sh /dev/sdX  CAMINHO/fel-sdboot.sunxi
set -euo pipefail
DEV="${1:-}"; IMG="${2:-}"
[ -n "$DEV" ] && [ -n "$IMG" ] || { sed -n 2,14p "$0"; exit 2; }
[ -b "$DEV" ] || { echo "ERRO: $DEV não é dispositivo de bloco"; exit 2; }
[ -f "$IMG" ] || { echo "ERRO: $IMG não existe"; exit 2; }

NAME="$(basename "$DEV")"
case "$NAME" in sd[a-z]|mmcblk[0-9]) ;; *) echo "ERRO: informe o disco inteiro (ex. /dev/sdb ou /dev/mmcblk0), não uma partição"; exit 2;; esac

# Proteções contra gravar no disco do computador
ROOTDEV="$(lsblk -no PKNAME "$(findmnt -no SOURCE /)" 2>/dev/null || true)"
[ "$NAME" != "$ROOTDEV" ] || { echo "ERRO: $DEV contém o sistema do computador!"; exit 3; }
if lsblk -no MOUNTPOINT "$DEV" | grep -q .; then echo "ERRO: há partições montadas em $DEV; desmonte antes"; exit 3; fi
SIZE_B=$(blockdev --getsize64 "$DEV")
[ "$SIZE_B" -le $((128*1024*1024*1024)) ] || { echo "ERRO: $DEV tem mais de 128 GB — não parece um microSD"; exit 3; }
REMOVABLE="$(cat /sys/block/$NAME/removable 2>/dev/null || echo 0)"
case "$NAME" in mmcblk*) REMOVABLE=1;; esac
[ "$REMOVABLE" = 1 ] || { echo "ERRO: $DEV não é removível segundo o kernel"; exit 3; }

# Verifica a imagem: cabeçalho eGON.BT0 no deslocamento 4 e tamanho pequeno
MAGIC="$(dd if="$IMG" bs=1 skip=4 count=8 2>/dev/null)"
[ "$MAGIC" = "eGON.BT0" ] || { echo "ERRO: $IMG não tem cabeçalho eGON.BT0"; exit 3; }
ISZ=$(stat -c %s "$IMG"); [ "$ISZ" -le 32768 ] || { echo "ERRO: imagem grande demais ($ISZ)"; exit 3; }
FIRST_PART_START=$(lsblk -bno START "$DEV" 2>/dev/null | sed -n 2p | tr -d ' ' || true)
if [ -n "${FIRST_PART_START:-}" ] && [ $((FIRST_PART_START*512)) -lt $((8192+ISZ)) ]; then
  echo "ERRO: a 1ª partição começa cedo demais e seria sobrescrita"; exit 3
fi

lsblk -o NAME,SIZE,MODEL,TRAN,RM "$DEV"
echo
echo "Será gravado: $IMG ($ISZ bytes) em $DEV a partir do byte 8192."
echo "Backup dos 64 KiB iniciais será salvo antes em ./sd-backup-$NAME-inicio.bin"
read -r -p "Digite GRAVAR para confirmar: " OK
[ "$OK" = "GRAVAR" ] || { echo "Cancelado."; exit 1; }
dd if="$DEV" of="./sd-backup-$NAME-inicio.bin" bs=1024 count=64 status=none
sha256sum "./sd-backup-$NAME-inicio.bin"
dd if="$IMG" of="$DEV" bs=1024 seek=8 conv=fsync status=none
sync
dd if="$DEV" bs=1 skip=8192 count="$ISZ" status=none | cmp - "$IMG" && echo "OK: gravado e conferido."
