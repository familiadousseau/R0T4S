/* Ligado para execução na SRAM A1 do A13, endereço 0x2000 (ver probe.c). */
ENTRY(probe_main)
SECTIONS
{
	. = 0x2000;
	.text : {
		KEEP(*(.text.entry))
		*(.text*)
		*(.rodata*)
	}
	/* Nenhum dado gravável/zerado é permitido: o programa não tem .data/.bss. */
	/DISCARD/ : { *(.data*) *(.bss*) *(.ARM.exidx*) *(.ARM.attributes) *(.comment) }
	ASSERT(SIZEOF(.text) <= 0x1C00, "fel-probe excede a janela 0x2000-0x3BFF")
}
