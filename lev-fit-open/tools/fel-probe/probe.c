/*
 * fel-probe — primeiro programa a ser executado no Allwinner A13 via FEL.
 *
 * Objetivo (Marco 1): provar que a CPU executa código carregado pela USB,
 * SEM tocar na NAND, na DRAM, no PMIC ou em qualquer periférico com efeito
 * permanente.
 *
 * O que o programa faz:
 *   - lê registradores de identificação (MIDR, CPSR, SCTLR);
 *   - lê o ID do SoC pelo registrador de versão do controlador de SRAM
 *     (0x01C00024, mesmo método usado pelo U-Boot mainline em
 *     arch/arm/mach-sunxi/cpu_info.c) e restaura o valor original;
 *   - lê as 4 palavras da SID (e-fuses, somente leitura) em 0x01C23800;
 *   - calcula um hash FNV-1a de 32 bits sobre os 32 KiB da BROM
 *     (0xFFFF0000) — o computador calcula o mesmo hash sobre a BROM lida
 *     pela USB; se baterem, foi a CPU do aparelho que fez a conta;
 *   - devolve um "nonce" aleatório gravado pelo computador antes da
 *     execução, transformado (nonce ^ 0xA5A5A5A5), provando que o resultado
 *     é desta execução e não lixo antigo da SRAM;
 *   - grava tudo em 0x4000 (SRAM A2) e retorna para o código FEL da BROM
 *     (bx lr), mantendo o aparelho em modo FEL.
 *
 * Mapa de SRAM respeitado (fonte: sunxi-tools/soc_info.c):
 *   0x1000        área de rascunho usada pelo próprio sunxi-fel
 *   0x1C00-0x1FFF pilha de IRQ da BROM  -> NÃO usar
 *   0x2000        este programa (< 2 KiB)
 *   0x4000        bloco de resultados (64 bytes)
 *   0x4100        nonce escrito pelo computador
 *   0x5C00-0x6FFF pilha da BROM (usamos poucos bytes dela)
 *   0x7C00-0x7FFF dados vitais do FEL -> NÃO usar
 *
 * Escritas permitidas (conferidas pelo teste em emulador): 0x4000-0x4033
 * (resultados), alguns bytes da pilha da BROM (0x5C00-0x6FFF) e a escrita
 * temporária (e restaurada) do bit 15 em 0x01C00024. Nada mais.
 */
#include <stdint.h>

#define RESULT_ADDR   0x00004000u
#define NONCE_ADDR    0x00004100u
#define SRAMC_VER_REG 0x01C00024u
#define SID_BASE      0x01C23800u
#define BROM_BASE     0xFFFF0000u
#define BROM_SIZE     0x00008000u

#define PROBE_MAGIC   0x4656454Cu /* bytes "LEVF" em little-endian */
#define PROBE_VERSION 1u
#define PROBE_DONE    0x600DC0DEu
#define NONCE_XOR     0xA5A5A5A5u

enum {
	R_MAGIC = 0,
	R_VERSION,
	R_NONCE_X,
	R_MIDR,
	R_SOC_ID,
	R_CPSR,
	R_SCTLR,
	R_SID0, R_SID1, R_SID2, R_SID3,
	R_BROM_FNV,
	R_DONE,
	R_COUNT
};

static inline uint32_t rd32(uint32_t a) { return *(volatile uint32_t *)a; }
static inline void wr32(uint32_t a, uint32_t v) { *(volatile uint32_t *)a = v; }

static uint32_t fnv1a32(uint32_t base, uint32_t len)
{
	uint32_t h = 0x811C9DC5u;
	for (uint32_t i = 0; i < len; i += 4) {
		uint32_t w = rd32(base + i);
		for (int b = 0; b < 4; b++) {
			h ^= (w >> (8 * b)) & 0xFFu;
			h *= 0x01000193u;
		}
	}
	return h;
}

__attribute__((section(".text.entry"), used))
void probe_main(void)
{
	uint32_t midr, cpsr, sctlr, orig, soc;

	/* Limpa o bloco de resultados; R_DONE só é escrito no final. */
	for (int i = 0; i < R_COUNT; i++)
		wr32(RESULT_ADDR + 4u * i, 0);

	__asm__ volatile("mrc p15, 0, %0, c0, c0, 0" : "=r"(midr));
	__asm__ volatile("mrs %0, cpsr" : "=r"(cpsr));
	__asm__ volatile("mrc p15, 0, %0, c1, c0, 0" : "=r"(sctlr));

	orig = rd32(SRAMC_VER_REG);
	wr32(SRAMC_VER_REG, orig | (1u << 15));
	soc = rd32(SRAMC_VER_REG) >> 16;
	wr32(SRAMC_VER_REG, orig);

	wr32(RESULT_ADDR + 4u * R_MAGIC,   PROBE_MAGIC);
	wr32(RESULT_ADDR + 4u * R_VERSION, PROBE_VERSION);
	wr32(RESULT_ADDR + 4u * R_NONCE_X, rd32(NONCE_ADDR) ^ NONCE_XOR);
	wr32(RESULT_ADDR + 4u * R_MIDR,    midr);
	wr32(RESULT_ADDR + 4u * R_SOC_ID,  soc);
	wr32(RESULT_ADDR + 4u * R_CPSR,    cpsr);
	wr32(RESULT_ADDR + 4u * R_SCTLR,   sctlr);
	for (int i = 0; i < 4; i++)
		wr32(RESULT_ADDR + 4u * (R_SID0 + i), rd32(SID_BASE + 4u * i));
	wr32(RESULT_ADDR + 4u * R_BROM_FNV, fnv1a32(BROM_BASE, BROM_SIZE));
	wr32(RESULT_ADDR + 4u * R_DONE,    PROBE_DONE);
	/* retorno normal (bx lr) devolve o controle ao laço FEL da BROM */
}
