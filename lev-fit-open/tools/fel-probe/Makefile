# Compila o fel-probe para o Allwinner A13 (Cortex-A8, ARMv7-A, modo ARM).
#
# Padrão: clang + ld.lld (sudo apt install clang lld llvm)
# Alternativa GCC: make CROSS_COMPILE=arm-none-eabi-
#                  (sudo apt install gcc-arm-none-eabi)

CFLAGS_COMMON := -Os -marm -mcpu=cortex-a8 -mfloat-abi=soft \
                 -ffreestanding -fno-builtin -nostdlib -fno-pic \
                 -fno-stack-protector -fno-unwind-tables \
                 -fno-asynchronous-unwind-tables -Wall -Wextra -Werror

ifdef CROSS_COMPILE
CC      := $(CROSS_COMPILE)gcc
LD      := $(CROSS_COMPILE)ld
OBJCOPY := $(CROSS_COMPILE)objcopy
OBJDUMP := $(CROSS_COMPILE)objdump
CFLAGS  := $(CFLAGS_COMMON)
else
CC      := clang
LD      := ld.lld
OBJCOPY := llvm-objcopy
OBJDUMP := llvm-objdump --triple=armv7a-none-eabi
CFLAGS  := --target=armv7a-none-eabi $(CFLAGS_COMMON)
endif

all: fel-probe.bin fel-probe.lst

probe.o: probe.c
	$(CC) $(CFLAGS) -c $< -o $@

fel-probe.elf: probe.o probe.lds
	$(LD) -T probe.lds -o $@ probe.o

fel-probe.bin: fel-probe.elf
	$(OBJCOPY) -O binary $< $@
	@sha256sum $@

fel-probe.lst: fel-probe.elf
	$(OBJDUMP) -d $< > $@

test: fel-probe.bin
	python3 -I test/emulate_probe.py fel-probe.bin

clean:
	rm -f probe.o fel-probe.elf fel-probe.bin fel-probe.lst

.PHONY: all test clean
