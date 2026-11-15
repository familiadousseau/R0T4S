# Análise do código GPL da Bookeen

Repositórios: `BOOKEEN/kernel-linux-3.0` @ `0aeda9a`, `BOOKEEN/u-boot-2011` @ `cfd01df`.

## 1. Variantes de placa (`arch/arm/configs/awa13_*_defconfig`)

13 configurações de produto: `b1b2`, `ff1`, `h_l`, `l_l`, `l_s`, `m1_2`, `m_l`, `m_l_android`, `m_s`, `nf1nf2`, `s1s2`, além de `a13_defconfig` e `a13_nuclear_defconfig`.

| Config | Resolução FB | Teclado | Touch (módulos) | PMIC |
|---|---|---|---|---|
| `awa13_ff1` | 1024×758 | **`KEYBOARD_SUN4I_KEYBOARD_SARAIVA=y`** | GT9XX, CYPRESS_XRZ, CTPTS | `AW_AXP20=y`, `AW_AXP20_COU=y` |
| `awa13_h_l` | 1448×1072 | — | CYPRESS_XRZ, CTPTS | `AW_AXP=y` |
| `awa13_l_l` | 800×600 | — | CYPRESS_XRZ, CTPTS | `AW_AXP=y` |
| `awa13_l_s` | 800×600 | — | CYPRESS_XRZ, CTPTS | `AW_AXP=y` |
| demais | não definida explicitamente | — | CYPRESS_XRZ, CTPTS | `AW_AXP=y` |

Todas: `CONFIG_CMDLINE="mem=448M@0x40000000 console=ttyS0,115200"`, `CONFIG_SUN5I_NANDFLASH=y`, `CONFIG_MMC_SUNXI=y`, USB0 OTG.

**Leitura crítica:** `ff1` é a **única** config com a opção Saraiva, mas tem 1024×758. Se o LEV Fit for de fato 800×600 (TechTudo), ele pode corresponder a `l_l`/`l_s` com outro teclado, ou o Fit pode simplesmente não estar entre essas configs. **Não usar nenhuma dessas configs como verdade para o Fit** sem confirmar pela serigrafia da placa ou pelo kernel/`script.bin` extraídos da NAND.

## 2. Teclas (`drivers/input/keyboard/sun4i-keyboard.c`)

- As teclas são lidas pelo **LRADC canal 0** (interrupções `LRADC_ADC0_*`).
- A variante Saraiva trata o código `0x05` como o botão que muda de estado (`button_change_status(1)`); as outras variantes usam `0x07`.
- No mainline isso corresponde ao `sun4i-lradc-keys`, com os limiares de tensão definidos no DT. Será preciso medir os níveis de cada tecla.

## 3. Tela E-Ink (`drivers/video/sun5i/disp/de_bsp/de/disp_eink*.c`)

- Os quadros são gerados em software e enviados pelo pipeline de display/TCON. Cada palavra de 32 bits combina dados e sinais de controle (padrões `0xD08000`, `0xF08000`, `0xff030303`).
- Waveforms carregadas do sistema de arquivos em tempo de execução:
  - `AWF_WAVEFORM_SUPPORTED` definido → `/system/waveform.awf` (recuperação: `/waveform.awf`);
  - formato antigo: `/system/{du,short_du,gc16,short_gc16,local,a2,a2_in,a2_out}.bin`.
- Tabelas por temperatura (`T_MAX`, `wf_temp_area_tbl`); modos INIT, GC16, GC4, DU e A2; famílias de painel **OED** e **PVI**.
- `rotate_buffer[776192]` = 1024×758 (o código assume esse tamanho como máximo).
- Interface com o PMIC: `tps65185_vcom_set(int vcom_mv)`, `tps65185_v3p3_set()`.

**Para o novo driver:** é preciso documentar (a) o mapeamento bit → sinal do painel (SPH/SPV, CKV, LE, OE, GMODE…), (b) a temporização do TCON usada no modo EPD, (c) o formato `.awf` e (d) a sequência de energia. Os quatro podem ser extraídos desse código GPL.

## 4. TPS65185 (`drivers/hwmon/tps65185/`)

- `tps65185-i2c.c` + `tps65185-i2c.uu`: o `.uu` é um **objeto ELF ARM relocável pré-compilado** (com símbolos de depuração). A lógica real está nesse binário.
- Strings revelam: nome interno "papyrus", leitura do ID do chip (`TPS6518%dr%dp%d`), endereço I²C vindo do `sys_config` (`tps65185_twi_addr`, `tps65185_twi_id`), leitura de temperatura, `papyrus_set_vcom2`.
- **Decisão:** não usar o binário. Usar o driver mainline `ti,tps65185` (GPL, 2025), estendendo-o se faltar algo (ex.: temperatura).

## 5. U-Boot Bookeen (`include/configs/sun5i_a13.h`)

- `bootcmd`: `nand read 50000000 boot; boota 50000000` (imagem estilo Android na partição `boot`).
- `boot_recovery`: `nand read 50000000 recovery; boota 50000000`.
- `nand_root=/dev/nandd`, `mmc_root=/dev/mmcblk0p4`, ambiente na NAND (`CONFIG_ENV_IS_IN_NAND_SUNXI`).
- Tecla de recuperação lida pelo ADC (`recovery_key_value_min/max`, `arch/arm/cpu/armv7/sunxi/key.c`).
- Os carregadores `boot0`/`boot1` da Allwinner **não** estão no repositório (são fechados). A entrada em FEL por UART (se existir) estaria neles.

**Hipótese sobre o "brick":** se o jailbreak alterou apenas a partição de sistema (`nandd`) ou o `boot`, o `boot0`/`boot1`/U-Boot podem estar íntegros. Nesse caso, o console UART mostraria o boot avançando até falhar. Isso é diagnosticável no Marco 2 sem gravar nada.
