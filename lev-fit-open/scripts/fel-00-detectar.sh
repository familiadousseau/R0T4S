#!/usr/bin/env bash
# LEV Fit Open — Etapa 1a: detectar o aparelho em modo FEL (SOMENTE LEITURA).
#
# Não grava nada no aparelho. Executa apenas:
#   lsusb            -> procura o ID USB 1f3a:efe8 (BROM Allwinner em FEL)
#   sunxi-fel ver    -> pergunta à BROM qual é o SoC
#   sunxi-fel sid    -> lê o número de série de fábrica (e-fuses)
set -euo pipefail
FEL="${SUNXI_FEL:-sunxi-fel}"
command -v "$FEL" >/dev/null || { echo "ERRO: sunxi-fel não encontrado (apt install sunxi-tools ou compile https://github.com/linux-sunxi/sunxi-tools)"; exit 2; }

echo "== 1. Dispositivos USB Allwinner (esperado: 1f3a:efe8) =="
if command -v lsusb >/dev/null; then
  lsusb | grep -i '1f3a:' || echo "(nenhum dispositivo 1f3a encontrado)"
fi
if ! lsusb 2>/dev/null | grep -qi '1f3a:efe8'; then
  echo
  echo "Aparelho NÃO está em modo FEL. Veja documentation/recovery/01-marco1-fel.md, seção 'Como entrar em FEL'."
  exit 1
fi

echo; echo "== 2. sunxi-fel ver =="
VER="$("$FEL" ver)"; echo "$VER"
if ! grep -q 'soc=00001625' <<<"$VER"; then
  echo "ATENÇÃO: o SoC informado não é 0x1625 (A13/A10s/R8). PARE e registre a saída acima."
  exit 1
fi

echo; echo "== 3. sunxi-fel sid =="
"$FEL" sid
echo
echo "OK: A13 respondendo em modo FEL. Próximo passo: scripts/fel-01-probe.sh"
