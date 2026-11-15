# fel-probe (Marco 1)

Programa bare-metal de 332 bytes executado na SRAM do A13 via `sunxi-fel exe 0x2000`. Lê MIDR, CPSR, SCTLR, ID do SoC (0x01C00024), SID, faz hash FNV-1a da BROM e ecoa um nonce; grava 52 bytes em 0x4000 e retorna ao FEL. Não acessa NAND, DRAM nem periféricos.

| Arquivo | Função |
|---|---|
| `probe.c`, `probe.lds`, `Makefile` | Código e build (clang/lld por padrão; `CROSS_COMPILE=arm-none-eabi-` para GCC) |
| `fel-probe.bin` | Binário pronto (SHA-256 `b1b2d7997f64991421c4c7d3d0bb8404e6139cb74802ff2e736b5d62dcc303f2`, clang 18.1.3) |
| `fel-probe.lst` | Desmontagem completa, para auditoria |
| `verify_probe.py` | Verificador no PC (só biblioteca padrão) |
| `test/emulate_probe.py` | Teste em Unicorn: retorno ao FEL, escritas só em áreas permitidas, registrador restaurado, verificador aprova/reprova |
| `test/mock_sunxi_fel.py` | Simulador do `sunxi-fel` para testar os scripts sem hardware |

```sh
make && make test
# teste do script completo com o simulador:
printf '#!/bin/sh\nexec python3 -I %s/test/mock_sunxi_fel.py "$@"\n' "$PWD" > /tmp/fel-mock && chmod +x /tmp/fel-mock
SUNXI_FEL=/tmp/fel-mock MOCK_FEL_STATE=/tmp/fel-state ../../scripts/fel-01-probe.sh
```

Não testado com GCC (`arm-none-eabi-gcc`) nesta sessão.
