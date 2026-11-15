#!/usr/bin/env python3
"""Simulador mínimo do `sunxi-fel` para testar os scripts sem hardware.

Implementa só os comandos usados pelos scripts do Marco 1:
  ver | sid | clear ADDR LEN | write ADDR FILE | exe ADDR | read ADDR LEN FILE

O "aparelho" é um estado em disco (variável MOCK_FEL_STATE): SRAM de 48 KiB,
BROM aleatória de 32 KiB e SID. `exe` roda o código no Unicorn (Cortex-A8)
com o mesmo modelo de hardware de emulate_probe.py. Recusa acessos fora da
SRAM/BROM, como garantia extra de que os scripts não tentam tocar DRAM/NAND.
"""
import os
import random
import struct
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_LR, UC_CPU_ARM_CORTEX_A8

STATE = os.environ.get("MOCK_FEL_STATE", "/tmp/mock-fel")
SRAM_SIZE = 0xC000
BROM_BASE = 0xFFFF0000
SRAMC_VER = 0x01C00024
SID_BASE = 0x01C23800


def load():
    os.makedirs(STATE, exist_ok=True)
    p = lambda n: os.path.join(STATE, n)
    if not os.path.exists(p("brom.bin")):
        rng = random.Random(42)
        open(p("brom.bin"), "wb").write(bytes(rng.getrandbits(8) for _ in range(0x8000)))
        open(p("sram.bin"), "wb").write(bytes(SRAM_SIZE))
        open(p("sid.bin"), "wb").write(struct.pack("<4I", *[rng.getrandbits(32) for _ in range(4)]))
    return (bytearray(open(p("sram.bin"), "rb").read()), open(p("brom.bin"), "rb").read(),
            open(p("sid.bin"), "rb").read())


def save(sram):
    open(os.path.join(STATE, "sram.bin"), "wb").write(sram)


def in_sram(a, n):
    return 0 <= a and a + n <= SRAM_SIZE


def main(argv):
    sram, brom, sid = load()
    cmd = argv[0]
    if cmd == "ver":
        print("AWUSBFEX soc=00001625(A13) 00000001 ver=0001 44 08 scratchpad=00007e00 00000000 00000000")
    elif cmd == "sid":
        print(":".join(f"{w:08x}" for w in struct.unpack("<4I", sid)))
    elif cmd == "clear":
        a, n = int(argv[1], 0), int(argv[2], 0)
        assert in_sram(a, n), f"mock: clear fora da SRAM 0x{a:x}"
        sram[a:a + n] = bytes(n); save(sram)
    elif cmd == "write":
        a, data = int(argv[1], 0), open(argv[2], "rb").read()
        assert in_sram(a, len(data)), f"mock: write fora da SRAM 0x{a:x}"
        sram[a:a + len(data)] = data; save(sram)
    elif cmd == "read":
        a, n, f = int(argv[1], 0), int(argv[2], 0), argv[3]
        if in_sram(a, n):
            open(f, "wb").write(sram[a:a + n])
        elif BROM_BASE <= a and a + n <= BROM_BASE + 0x8000:
            open(f, "wb").write(brom[a - BROM_BASE:a - BROM_BASE + n])
        else:
            sys.exit(f"mock: read fora de SRAM/BROM 0x{a:x}")
    elif cmd == "exe":
        a = int(argv[1], 0)
        assert in_sram(a, 4)
        uc = Uc(UC_ARCH_ARM, UC_MODE_ARM, cpu=UC_CPU_ARM_CORTEX_A8)
        uc.mem_map(0, 0x10000); uc.mem_write(0, bytes(sram))
        uc.mem_map(0x01C00000, 0x30000)
        uc.mem_map(BROM_BASE, 0x10000); uc.mem_write(BROM_BASE, brom)
        uc.mem_write(SID_BASE, sid)
        st = {"v": 0}

        def w(u, _a, addr, size, value, _d):
            if addr == SRAMC_VER:
                v = value & 0xFFFF
                st["v"] = v | (0x1625 << 16 if v & 0x8000 else 0)

        def r(u, _a, addr, size, value, _d):
            if addr == SRAMC_VER:
                u.mem_write(SRAMC_VER, struct.pack("<I", st["v"]))
        uc.hook_add(UC_HOOK_MEM_WRITE, w); uc.hook_add(UC_HOOK_MEM_READ, r)
        uc.reg_write(UC_ARM_REG_SP, 0x7000); uc.reg_write(UC_ARM_REG_LR, 0xF000)
        uc.emu_start(a, 0xF000, count=5_000_000)
        save(bytearray(uc.mem_read(0, SRAM_SIZE)))
    else:
        sys.exit(f"mock: comando não suportado: {cmd}")


if __name__ == "__main__":
    main(sys.argv[1:])
