#!/usr/bin/env python3
"""Verifica o resultado do fel-probe (Marco 1 do projeto LEV Fit Open).

Uso:
  verify_probe.py RESULTS.bin BROM.bin NONCE_HEX [--sid "aaaa:bbbb:cccc:dddd"]
                  [--json SAIDA.json]

RESULTS.bin : 64 bytes lidos de 0x4000 (sunxi-fel read 0x4000 64 RESULTS.bin)
BROM.bin    : 32 KiB lidos de 0xFFFF0000 (sunxi-fel read 0xffff0000 0x8000 BROM.bin)
NONCE_HEX   : valor de 32 bits gravado em 0x4100 antes da execução
--sid       : saída de `sunxi-fel sid` (comparação cruzada opcional)

Código de saída 0 = todas as verificações críticas passaram.
Só usa a biblioteca padrão do Python.
"""
import argparse
import hashlib
import json
import struct
import sys

PROBE_MAGIC = 0x4656454C
PROBE_VERSION = 1
PROBE_DONE = 0x600DC0DE
NONCE_XOR = 0xA5A5A5A5
EXPECTED_SOC_ID = 0x1625  # A10s / A13 / R8 (sunxi-tools soc_info.c)
FIELDS = ["magic", "version", "nonce_x", "midr", "soc_id", "cpsr", "sctlr",
          "sid0", "sid1", "sid2", "sid3", "brom_fnv", "done"]


def fnv1a32(data: bytes) -> int:
    h = 0x811C9DC5
    for b in data:
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("results")
    ap.add_argument("brom")
    ap.add_argument("nonce")
    ap.add_argument("--sid", default=None)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()

    raw = open(a.results, "rb").read()
    brom = open(a.brom, "rb").read()
    nonce = int(a.nonce, 16) & 0xFFFFFFFF
    if len(raw) < 4 * len(FIELDS):
        print(f"ERRO: {a.results} tem {len(raw)} bytes; esperado >= {4 * len(FIELDS)}")
        return 1
    v = dict(zip(FIELDS, struct.unpack_from("<%dI" % len(FIELDS), raw)))

    checks = []  # (nome, ok, crítico, detalhe)

    def check(name, ok, critical, detail):
        checks.append((name, bool(ok), critical, detail))

    check("assinatura LEVF", v["magic"] == PROBE_MAGIC, True, f"0x{v['magic']:08x}")
    check("versão do formato", v["version"] == PROBE_VERSION, True, str(v["version"]))
    check("execução concluída", v["done"] == PROBE_DONE, True, f"0x{v['done']:08x}")
    check("nonce desta execução", v["nonce_x"] == (nonce ^ NONCE_XOR), True,
          f"recebido 0x{v['nonce_x']:08x}, esperado 0x{nonce ^ NONCE_XOR:08x}")
    implementer = v["midr"] >> 24
    part = (v["midr"] >> 4) & 0xFFF
    check("CPU ARM Cortex-A8 (MIDR)", implementer == 0x41 and part == 0xC08, True,
          f"MIDR=0x{v['midr']:08x} (implementador 0x{implementer:02x}, peça 0x{part:03x})")
    check("ID do SoC = 0x1625 (A13/A10s/R8)", v["soc_id"] == EXPECTED_SOC_ID, True,
          f"0x{v['soc_id']:04x}")
    check("BROM lida tem 32 KiB", len(brom) == 0x8000, True, f"{len(brom)} bytes")
    host_fnv = fnv1a32(brom[:0x8000])
    check("hash da BROM calculado no aparelho == calculado no PC",
          v["brom_fnv"] == host_fnv, True,
          f"aparelho 0x{v['brom_fnv']:08x}, PC 0x{host_fnv:08x}")
    sid_words = [v["sid0"], v["sid1"], v["sid2"], v["sid3"]]
    sid_str = ":".join(f"{w:08x}" for w in sid_words)
    if a.sid:
        check("SID igual à do `sunxi-fel sid`", a.sid.strip().lower() == sid_str, False,
              f"probe {sid_str} / sunxi-fel {a.sid.strip()}")
    mode = v["cpsr"] & 0x1F
    modes = {0x10: "USR", 0x11: "FIQ", 0x12: "IRQ", 0x13: "SVC", 0x17: "ABT",
             0x1B: "UND", 0x1F: "SYS"}

    print("=== fel-probe: resultado ===")
    for name, ok, critical, detail in checks:
        tag = "OK  " if ok else ("FALHA" if critical else "AVISO")
        print(f"[{tag}] {name}: {detail}")
    print(f"       CPSR=0x{v['cpsr']:08x} (modo {modes.get(mode, hex(mode))})"
          f"  SCTLR=0x{v['sctlr']:08x} (MMU={'on' if v['sctlr'] & 1 else 'off'},"
          f" D-cache={'on' if v['sctlr'] & 4 else 'off'},"
          f" I-cache={'on' if v['sctlr'] & 0x1000 else 'off'})")
    print(f"       SID={sid_str}")
    print(f"       SHA-256 BROM={hashlib.sha256(brom).hexdigest()}")
    print(f"       SHA-256 resultados={hashlib.sha256(raw).hexdigest()}")

    passed = all(ok for _, ok, critical, _ in checks if critical)
    print("RESULTADO GERAL:", "APROVADO — a CPU do aparelho executou o código carregado via FEL"
          if passed else "REPROVADO")

    if a.json:
        with open(a.json, "w") as f:
            json.dump({
                "passed": passed,
                "fields": {k: f"0x{x:08x}" for k, x in v.items()},
                "sid": sid_str,
                "brom_sha256": hashlib.sha256(brom).hexdigest(),
                "checks": [{"name": n, "ok": o, "critical": c, "detail": d}
                           for n, o, c, d in checks],
            }, f, indent=2, ensure_ascii=False)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
