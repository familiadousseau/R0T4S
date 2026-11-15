#!/usr/bin/env python3
"""Teste do fel-probe em emulador (Unicorn, Cortex-A8) — sem hardware.

Simula o ambiente que a BROM do A13 oferece em modo FEL:
  * SRAM em 0x0000-0xBFFF, pilha da BROM em 0x7000 (cresce para baixo);
  * BROM de 32 KiB em 0xFFFF0000 (conteúdo aleatório no teste);
  * registrador de versão do controlador de SRAM (0x01C00024) que devolve
    o ID 0x1625 nos bits 31:16 quando o bit 15 está ligado;
  * SID (e-fuses) em 0x01C23800.

Verifica:
  1. o programa termina retornando pelo LR (como exige o FEL);
  2. todas as escritas ficam restritas a: bloco de resultados
     0x4000-0x4033, pilha da BROM 0x5C00-0x6FFF e o registrador 0x01C00024
     (que precisa voltar ao valor original);
  3. o verificador do PC aprova o resultado correto;
  4. o verificador REPROVA resultados adulterados (nonce errado, BROM
     diferente, resultado velho na SRAM).

Requer: pip install unicorn
"""
import os
import random
import struct
import subprocess
import sys
import tempfile

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_READ
from unicorn import UcError
from unicorn.arm_const import (UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC,
                               UC_CPU_ARM_CORTEX_A8)

HERE = os.path.dirname(os.path.abspath(__file__))
VERIFY = os.path.join(HERE, "..", "verify_probe.py")

LOAD = 0x2000
RET_TRAP = 0x9000
SRAMC_VER = 0x01C00024
SID_BASE = 0x01C23800
SOC_ID = 0x1625
ALLOWED = [(0x4000, 0x4034), (0x5C00, 0x7000), (SRAMC_VER, SRAMC_VER + 4)]


def run(binary: bytes, nonce: int, brom: bytes, sid, stale_results=False):
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM, cpu=UC_CPU_ARM_CORTEX_A8)
    uc.mem_map(0x0, 0xC000)
    uc.mem_map(0x01C00000, 0x30000)
    uc.mem_map(0xFFFF0000, 0x10000)
    uc.mem_write(0xFFFF0000, brom)
    uc.mem_write(SID_BASE, struct.pack("<4I", *sid))
    sramc_orig = 0x00000003  # valor qualquer; deve ser restaurado
    uc.mem_write(SRAMC_VER, struct.pack("<I", sramc_orig))
    if stale_results:
        uc.mem_write(0x4000, os.urandom(0x40))
    uc.mem_write(0x4100, struct.pack("<I", nonce))
    uc.mem_write(LOAD, binary)

    writes = []

    def on_write(uc_, access, addr, size, value, _):
        writes.append((addr, size))
        if addr == SRAMC_VER:
            v = value & 0xFFFF
            if v & 0x8000:
                v |= SOC_ID << 16
            # Unicorn grava `value` após o hook; registramos o valor modelado
            uc_.mem_write(SRAMC_VER, struct.pack("<I", value & 0xFFFFFFFF))
            hw_state["val"] = v

    hw_state = {"val": sramc_orig}

    def on_read(uc_, access, addr, size, value, _):
        if addr == SRAMC_VER:
            uc_.mem_write(SRAMC_VER, struct.pack("<I", hw_state["val"]))

    uc.hook_add(UC_HOOK_MEM_WRITE, on_write)
    uc.hook_add(UC_HOOK_MEM_READ, on_read)
    uc.reg_write(UC_ARM_REG_SP, 0x7000)
    uc.reg_write(UC_ARM_REG_LR, RET_TRAP)
    uc.emu_start(LOAD, RET_TRAP, count=2_000_000)
    pc = uc.reg_read(UC_ARM_REG_PC)
    results = bytes(uc.mem_read(0x4000, 0x40))
    final_sramc = hw_state["val"]
    return pc, results, writes, final_sramc, sramc_orig


def verify(results: bytes, brom: bytes, nonce: int, sid_str: str) -> int:
    with tempfile.TemporaryDirectory() as d:
        r = os.path.join(d, "results.bin")
        b = os.path.join(d, "brom.bin")
        open(r, "wb").write(results)
        open(b, "wb").write(brom)
        p = subprocess.run([sys.executable, "-I", VERIFY, r, b, f"{nonce:08x}",
                            "--sid", sid_str], capture_output=True, text=True)
        return p.returncode, p.stdout


def main() -> int:
    binary = open(sys.argv[1], "rb").read()
    rng = random.Random(1234)
    brom = bytes(rng.getrandbits(8) for _ in range(0x8000))
    sid = [rng.getrandbits(32) for _ in range(4)]
    sid_str = ":".join(f"{w:08x}" for w in sid)
    nonce = rng.getrandbits(32)
    failures = 0

    def expect(cond, msg):
        nonlocal failures
        print(("PASSOU " if cond else "FALHOU ") + msg)
        if not cond:
            failures += 1

    try:
        pc, results, writes, final_sramc, sramc_orig = run(binary, nonce, brom, sid,
                                                           stale_results=True)
    except UcError as e:
        print("FALHOU execução no emulador:", e)
        return 1

    expect(pc == RET_TRAP, f"programa retorna ao FEL via LR (PC final 0x{pc:x})")
    bad = [(a, s) for a, s in writes
           if not any(lo <= a and a + s <= hi for lo, hi in ALLOWED)]
    expect(not bad, f"nenhuma escrita fora das áreas permitidas ({len(writes)} escritas; "
                    f"fora: {[hex(a) for a, _ in bad]})")
    expect(final_sramc == sramc_orig, "registrador 0x01C00024 restaurado ao valor original")

    rc, out = verify(results, brom, nonce, sid_str)
    print(out)
    expect(rc == 0, "verificador APROVA o resultado legítimo")

    rc, _ = verify(results, brom, nonce ^ 1, sid_str)
    expect(rc != 0, "verificador REPROVA nonce diferente")
    brom2 = bytearray(brom)
    brom2[100] ^= 0xFF
    rc, _ = verify(results, bytes(brom2), nonce, sid_str)
    expect(rc != 0, "verificador REPROVA BROM diferente")
    rc, _ = verify(bytes(0x40), brom, nonce, sid_str)
    expect(rc != 0, "verificador REPROVA bloco de resultados vazio")

    print("\nTOTAL:", "TODOS OS TESTES PASSARAM" if failures == 0 else f"{failures} FALHA(S)")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
