#!/usr/bin/env bash
# LEV Fit Open — Etapa 1b (MARCO 1): executar o fel-probe na SRAM do A13.
#
# O que este script GRAVA no aparelho: apenas SRAM interna volátil
#   0x4000 (64 bytes, limpa), 0x4100 (4 bytes, nonce), 0x2000 (programa).
# NÃO acessa NAND, DRAM, cartão SD nem PMIC. Desligar o aparelho apaga tudo.
#
# Resultado salvo em builds/fel-logs/<data-hora>/ com hashes SHA-256.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
FEL="${SUNXI_FEL:-sunxi-fel}"
PROBE="$ROOT/tools/fel-probe/fel-probe.bin"
VERIFY="$ROOT/tools/fel-probe/verify_probe.py"

command -v "$FEL" >/dev/null || { echo "ERRO: sunxi-fel não encontrado"; exit 2; }
[ -f "$PROBE" ] || { echo "ERRO: $PROBE não existe. Rode: make -C $ROOT/tools/fel-probe"; exit 2; }
SIZE=$(stat -c %s "$PROBE")
[ "$SIZE" -le 7168 ] || { echo "ERRO: fel-probe.bin grande demais ($SIZE bytes)"; exit 2; }

OUT="$ROOT/builds/fel-logs/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUT"
exec > >(tee "$OUT/log.txt") 2>&1

echo "== Verificando SoC =="
VER="$("$FEL" ver)"; echo "$VER"
grep -q 'soc=00001625' <<<"$VER" || { echo "ABORTADO: SoC não é 0x1625"; exit 1; }

NONCE="$(od -An -N4 -tx4 /dev/urandom | tr -d ' \n')"
echo "nonce=$NONCE"
python3 -c "import struct,sys; open(sys.argv[1],'wb').write(struct.pack('<I', int(sys.argv[2],16)))" "$OUT/nonce.bin" "$NONCE"
cp "$PROBE" "$OUT/fel-probe.bin"

echo "== Carregando e executando na SRAM =="
"$FEL" clear 0x4000 64
"$FEL" write 0x4100 "$OUT/nonce.bin"
"$FEL" write 0x2000 "$OUT/fel-probe.bin"
"$FEL" exe 0x2000

echo "== Lendo resultados =="
"$FEL" read 0x4000 64 "$OUT/results.bin"
"$FEL" read 0xffff0000 0x8000 "$OUT/brom-a13.bin"
SID="$("$FEL" sid | tail -n1)"
echo "$SID" > "$OUT/sid.txt"
"$FEL" ver > "$OUT/ver.txt"

set +e
python3 -I "$VERIFY" "$OUT/results.bin" "$OUT/brom-a13.bin" "$NONCE" --sid "$SID" --json "$OUT/verificacao.json"
RC=$?
set -e
(cd "$OUT" && sha256sum *.bin *.txt *.json > SHA256SUMS)
echo
echo "Arquivos e hashes em: $OUT"
echo "Envie a pasta inteira (ou o log.txt e o verificacao.json) para registro no projeto."
exit $RC
