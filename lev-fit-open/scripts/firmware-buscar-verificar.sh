#!/usr/bin/env bash
# LEV Fit Open — procurar e VERIFICAR firmwares oficiais (CybUpdate.bin).
#
# NÃO toca no aparelho. Só baixa arquivos para o PC e lê o conteúdo deles,
# para saber se um firmware é do LEV Fit (tela 800x600) antes de usá-lo.
#
# Uso:
#   scripts/firmware-buscar-verificar.sh                 # tenta os links conhecidos
#   scripts/firmware-buscar-verificar.sh ARQUIVO.bin     # só verifica um arquivo que você já tem
#
# Requer: curl, tar, bzip2, md5sum, sunxi-tools (bin2fex), sudo (para montar
# o bootloader.fex só para leitura).
set -euo pipefail
OUT="${OUT:-$HOME/lev-firmware}"
MODEL="${MODEL:-CYBME1S-SA}"
OEM="http://fw.bookeen.com/fw_oem/SA-226D8A93-CB0F-4e23-A027-0E5AB7E1A861"

# Links candidatos. Nenhum é garantido: são padrões vistos em relatos públicos.
CANDIDATOS=(
  "fit-oem-2643|$OEM/Cybupdate20180212_2643/$MODEL/CybUpdate.bin"
  "saraiva-oficial|http://images.livrariasaraiva.com.br/estatico/ereader/CybUpdate.bin"
)

verificar() {
  local f="$1" d
  d="$(mktemp -d "${TMPDIR:-/tmp}/levfw.XXXXXX")"
  echo; echo "=== Verificando: $f"
  echo "SHA-256: $(sha256sum "$f" | cut -d' ' -f1)"
  echo "MD5:     $(md5sum "$f" | cut -d' ' -f1)"
  echo "Tipo:    $(file -b "$f")"
  if ! tar xjf "$f" -C "$d" 2>/dev/null; then
    echo "Não é um tar.bz2 (formato diferente); envie o tipo acima para análise."
    rm -rf "$d"; return
  fi
  echo "--- conteúdo do pacote:"; ls -l "$d"
  if [ -f "$d/contents" ]; then
    echo "--- arquivo 'contents' (o que o atualizador vai gravar):"; cat "$d/contents"
    echo "--- conferência de MD5 declarados:"
    while IFS='|' read -r tipo nome tam md5 ver; do
      [ -f "$d/$nome" ] || { echo "  $nome: AUSENTE"; continue; }
      real="$(md5sum "$d/$nome" | cut -d' ' -f1)"
      [ "${real,,}" = "${md5,,}" ] && echo "  $nome: OK" || echo "  $nome: MD5 DIFERENTE"
    done < "$d/contents"
  fi
  if [ -f "$d/bootloader.fex" ]; then
    local m="$d/mnt"; mkdir -p "$m"
    if sudo mount -o loop,ro "$d/bootloader.fex" "$m" 2>/dev/null; then
      echo "--- arquivos no bootloader:"; ls "$m"
      local sb; sb="$(find "$m" -maxdepth 2 -iname 'script*.bin' | head -n1)"
      if [ -n "$sb" ] && command -v bin2fex >/dev/null; then
        echo "--- configuração de tela e touch ($sb):"
        bin2fex "$sb" 2>/dev/null | grep -iE '^\[(lcd0_para|ctp_para|tp_para|eink|tps)|lcd_x|lcd_y|ctp_name|ctp_twi|eink_|tps65185' | head -40
      fi
      sudo umount "$m"
    else
      echo "(não foi possível montar o bootloader.fex)"
    fi
  else
    echo "(pacote sem bootloader.fex: não altera a configuração de tela)"
  fi
  rm -rf "$d"
  echo "=== Para servir no LEV Fit, esperamos lcd_x = 800 e lcd_y = 600."
}

if [ $# -ge 1 ]; then verificar "$1"; exit 0; fi

mkdir -p "$OUT"
for c in "${CANDIDATOS[@]}"; do
  nome="${c%%|*}"; url="${c#*|}"
  echo; echo "### $nome: $url"
  if curl -fsSL -m 120 -o "$OUT/$nome.part" "$url"; then
    mv "$OUT/$nome.part" "$OUT/$nome.bin"
    verificar "$OUT/$nome.bin"
  else
    rm -f "$OUT/$nome.part"; echo "indisponível"
  fi
done
echo; echo "Arquivos baixados em: $OUT  (NADA foi gravado no aparelho)"
