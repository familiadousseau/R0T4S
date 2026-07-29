#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "esp_mac.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "esp_now.h"
#include "driver/gpio.h"
#include "driver/i2c.h"

// ── WiFi Config ──
#ifndef CONFIG_ESPCSI_WIFI_SSID
#define CONFIG_ESPCSI_WIFI_SSID "ESP32_CSI"
#endif
#ifndef CONFIG_ESPCSI_WIFI_PASSWORD
#define CONFIG_ESPCSI_WIFI_PASSWORD "12345678"
#endif
#ifndef CONFIG_ESPCSI_CHANNEL
#define CONFIG_ESPCSI_CHANNEL 6
#endif

// ── GPIO Pins ──
#define LED_WALKING  GPIO_NUM_25
#define LED_SITTING  GPIO_NUM_26
#define LED_STANDING GPIO_NUM_27
#define I2C_SDA      GPIO_NUM_21
#define I2C_SCL      GPIO_NUM_22
#define I2C_PORT     I2C_NUM_0
#define OLED_ADDR    0x3C

static const char *TAG = "CSI_HAR";
static char current_activity[32] = "Waiting...";

// ══════════════════════════════════════════════════
// OLED SSD1306 Driver (minimal, no external lib)
// ══════════════════════════════════════════════════

#define OLED_WIDTH  128
#define OLED_HEIGHT 64
#define OLED_PAGES  8

static uint8_t oled_buffer[OLED_WIDTH * OLED_PAGES] = {0};

// 5x7 font for characters 32-127
static const uint8_t font5x7[][5] = {
    {0x00,0x00,0x00,0x00,0x00}, // ' '
    {0x00,0x00,0x5F,0x00,0x00}, // '!'
    {0x00,0x07,0x00,0x07,0x00}, // '"'
    {0x14,0x7F,0x14,0x7F,0x14}, // '#'
    {0x24,0x2A,0x7F,0x2A,0x12}, // '$'
    {0x23,0x13,0x08,0x64,0x62}, // '%'
    {0x36,0x49,0x55,0x22,0x50}, // '&'
    {0x00,0x05,0x03,0x00,0x00}, // '''
    {0x00,0x1C,0x22,0x41,0x00}, // '('
    {0x00,0x41,0x22,0x1C,0x00}, // ')'
    {0x14,0x08,0x3E,0x08,0x14}, // '*'
    {0x08,0x08,0x3E,0x08,0x08}, // '+'
    {0x00,0x50,0x30,0x00,0x00}, // ','
    {0x08,0x08,0x08,0x08,0x08}, // '-'
    {0x00,0x60,0x60,0x00,0x00}, // '.'
    {0x20,0x10,0x08,0x04,0x02}, // '/'
    {0x3E,0x51,0x49,0x45,0x3E}, // '0'
    {0x00,0x42,0x7F,0x40,0x00}, // '1'
    {0x42,0x61,0x51,0x49,0x46}, // '2'
    {0x21,0x41,0x45,0x4B,0x31}, // '3'
    {0x18,0x14,0x12,0x7F,0x10}, // '4'
    {0x27,0x45,0x45,0x45,0x39}, // '5'
    {0x3C,0x4A,0x49,0x49,0x30}, // '6'
    {0x01,0x71,0x09,0x05,0x03}, // '7'
    {0x36,0x49,0x49,0x49,0x36}, // '8'
    {0x06,0x49,0x49,0x29,0x1E}, // '9'
    {0x00,0x36,0x36,0x00,0x00}, // ':'
    {0x00,0x56,0x36,0x00,0x00}, // ';'
    {0x08,0x14,0x22,0x41,0x00}, // '<'
    {0x14,0x14,0x14,0x14,0x14}, // '='
    {0x00,0x41,0x22,0x14,0x08}, // '>'
    {0x02,0x01,0x51,0x09,0x06}, // '?'
    {0x32,0x49,0x79,0x41,0x3E}, // '@'
    {0x7E,0x11,0x11,0x11,0x7E}, // 'A'
    {0x7F,0x49,0x49,0x49,0x36}, // 'B'
    {0x3E,0x41,0x41,0x41,0x22}, // 'C'
    {0x7F,0x41,0x41,0x22,0x1C}, // 'D'
    {0x7F,0x49,0x49,0x49,0x41}, // 'E'
    {0x7F,0x09,0x09,0x09,0x01}, // 'F'
    {0x3E,0x41,0x49,0x49,0x7A}, // 'G'
    {0x7F,0x08,0x08,0x08,0x7F}, // 'H'
    {0x00,0x41,0x7F,0x41,0x00}, // 'I'
    {0x20,0x40,0x41,0x3F,0x01}, // 'J'
    {0x7F,0x08,0x14,0x22,0x41}, // 'K'
    {0x7F,0x40,0x40,0x40,0x40}, // 'L'
    {0x7F,0x02,0x0C,0x02,0x7F}, // 'M'
    {0x7F,0x04,0x08,0x10,0x7F}, // 'N'
    {0x3E,0x41,0x41,0x41,0x3E}, // 'O'
    {0x7F,0x09,0x09,0x09,0x06}, // 'P'
    {0x3E,0x41,0x51,0x21,0x5E}, // 'Q'
    {0x7F,0x09,0x19,0x29,0x46}, // 'R'
    {0x46,0x49,0x49,0x49,0x31}, // 'S'
    {0x01,0x01,0x7F,0x01,0x01}, // 'T'
    {0x3F,0x40,0x40,0x40,0x3F}, // 'U'
    {0x1F,0x20,0x40,0x20,0x1F}, // 'V'
    {0x3F,0x40,0x38,0x40,0x3F}, // 'W'
    {0x63,0x14,0x08,0x14,0x63}, // 'X'
    {0x07,0x08,0x70,0x08,0x07}, // 'Y'
    {0x61,0x51,0x49,0x45,0x43}, // 'Z'
    {0x00,0x7F,0x41,0x41,0x00}, // '['
    {0x02,0x04,0x08,0x10,0x20}, // '\'
    {0x00,0x41,0x41,0x7F,0x00}, // ']'
    {0x04,0x02,0x01,0x02,0x04}, // '^'
    {0x40,0x40,0x40,0x40,0x40}, // '_'
    {0x00,0x01,0x02,0x04,0x00}, // '`'
    {0x20,0x54,0x54,0x54,0x78}, // 'a'
    {0x7F,0x48,0x44,0x44,0x38}, // 'b'
    {0x38,0x44,0x44,0x44,0x20}, // 'c'
    {0x38,0x44,0x44,0x48,0x7F}, // 'd'
    {0x38,0x54,0x54,0x54,0x18}, // 'e'
    {0x08,0x7E,0x09,0x01,0x02}, // 'f'
    {0x0C,0x52,0x52,0x52,0x3E}, // 'g'
    {0x7F,0x08,0x04,0x04,0x78}, // 'h'
    {0x00,0x44,0x7D,0x40,0x00}, // 'i'
    {0x20,0x40,0x44,0x3D,0x00}, // 'j'
    {0x7F,0x10,0x28,0x44,0x00}, // 'k'
    {0x00,0x41,0x7F,0x40,0x00}, // 'l'
    {0x7C,0x04,0x18,0x04,0x78}, // 'm'
    {0x7C,0x08,0x04,0x04,0x78}, // 'n'
    {0x38,0x44,0x44,0x44,0x38}, // 'o'
    {0x7C,0x14,0x14,0x14,0x08}, // 'p'
    {0x08,0x14,0x14,0x18,0x7C}, // 'q'
    {0x7C,0x08,0x04,0x04,0x08}, // 'r'
    {0x48,0x54,0x54,0x54,0x20}, // 's'
    {0x04,0x3F,0x44,0x40,0x20}, // 't'
    {0x3C,0x40,0x40,0x40,0x7C}, // 'u'
    {0x1C,0x20,0x40,0x20,0x1C}, // 'v'
    {0x3C,0x40,0x30,0x40,0x3C}, // 'w'
    {0x44,0x28,0x10,0x28,0x44}, // 'x'
    {0x0C,0x50,0x50,0x50,0x3C}, // 'y'
    {0x44,0x64,0x54,0x4C,0x44}, // 'z'
    {0x00,0x08,0x36,0x41,0x00}, // '{'
    {0x00,0x00,0x7F,0x00,0x00}, // '|'
    {0x00,0x41,0x36,0x08,0x00}, // '}'
    {0x10,0x08,0x08,0x10,0x08}, // '~'
};

static esp_err_t i2c_master_init(void) {
    i2c_config_t conf = {
        .mode = I2C_MODE_MASTER,
        .sda_io_num = I2C_SDA,
        .scl_io_num = I2C_SCL,
        .sda_pullup_en = GPIO_PULLUP_ENABLE,
        .scl_pullup_en = GPIO_PULLUP_ENABLE,
        .master = { .clk_speed = 400000 },
        .clk_flags = 0,
    };
    ESP_ERROR_CHECK(i2c_param_config(I2C_PORT, &conf));
    return i2c_driver_install(I2C_PORT, I2C_MODE_MASTER, 0, 0, 0);
}

static esp_err_t oled_write_cmd(uint8_t cmd) {
    uint8_t buf[2] = {0x00, cmd};
    return i2c_master_write_to_device(I2C_PORT, OLED_ADDR, buf, 2, pdMS_TO_TICKS(100));
}

static esp_err_t oled_init(void) {
    uint8_t init_cmds[] = {
        0xAE, 0x20, 0x00, 0xB0, 0xC8, 0x00, 0x10,
        0x40, 0x81, 0xFF, 0xA1, 0xA6, 0xA8, 0x3F,
        0xA4, 0xD3, 0x00, 0xD5, 0xF0, 0xD9, 0x22,
        0xDA, 0x12, 0xDB, 0x20, 0x8D, 0x14, 0xAF
    };
    for (int i = 0; i < sizeof(init_cmds); i++) {
        if (oled_write_cmd(init_cmds[i]) != ESP_OK) return ESP_FAIL;
    }
    return ESP_OK;
}

static void oled_clear(void) {
    memset(oled_buffer, 0, sizeof(oled_buffer));
}

static void oled_draw_char(int x, int y_page, char c) {
    if (c < 32 || c > 126) return;
    const uint8_t *glyph = font5x7[c - 32];
    for (int col = 0; col < 5; col++) {
        if (x + col < OLED_WIDTH) {
            oled_buffer[y_page * OLED_WIDTH + x + col] = glyph[col];
        }
    }
}

static void oled_draw_string(int x, int page, const char *str) {
    while (*str) {
        oled_draw_char(x, page, *str++);
        x += 6;
        if (x >= OLED_WIDTH) break;
    }
}

static void oled_draw_string_large(int x, int page, const char *str) {
    while (*str && x < OLED_WIDTH) {
        if (*str >= 32 && *str <= 126) {
            const uint8_t *glyph = font5x7[*str - 32];
            for (int col = 0; col < 5; col++) {
                uint8_t column = glyph[col];
                uint16_t scaled = 0;
                for (int bit = 0; bit < 7; bit++) {
                    if (column & (1 << bit)) {
                        scaled |= (3 << (bit * 2));
                    }
                }
                if (x + col*2 < OLED_WIDTH) {
                    oled_buffer[page * OLED_WIDTH + x + col*2] = scaled & 0xFF;
                    if (page + 1 < OLED_PAGES)
                        oled_buffer[(page+1) * OLED_WIDTH + x + col*2] = (scaled >> 8) & 0xFF;
                    if (x + col*2 + 1 < OLED_WIDTH) {
                        oled_buffer[page * OLED_WIDTH + x + col*2+1] = scaled & 0xFF;
                        if (page + 1 < OLED_PAGES)
                            oled_buffer[(page+1) * OLED_WIDTH + x + col*2+1] = (scaled >> 8) & 0xFF;
                    }
                }
            }
        }
        x += 12;
        str++;
    }
}
static void oled_flush(void) {
    for (int page = 0; page < OLED_PAGES; page++) {
        oled_write_cmd(0xB0 + page);
        oled_write_cmd(0x00);
        oled_write_cmd(0x10);
        uint8_t buf[OLED_WIDTH + 1];
        buf[0] = 0x40;
        memcpy(buf + 1, &oled_buffer[page * OLED_WIDTH], OLED_WIDTH);
        i2c_master_write_to_device(I2C_PORT, OLED_ADDR, buf, sizeof(buf), pdMS_TO_TICKS(100));
    }
}

static void oled_draw_line(int page) {
    for (int x = 0; x < OLED_WIDTH; x++) {
        oled_buffer[page * OLED_WIDTH + x] = 0xFF;
    }
}

static void update_display(const char *activity) {
    oled_clear();
    oled_draw_string(0, 0, "WiFi CSI HAR");
    oled_draw_line(1);
    oled_draw_string_large(0, 3, activity);
    oled_draw_string(0, 7, "PICT 2025-26");
    oled_flush();
}

// ══════════════════════════════════════════════════
// GPIO Setup
// ══════════════════════════════════════════════════

static void gpio_init(void) {
    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << LED_WALKING) |
                        (1ULL << LED_SITTING) |
                        (1ULL << LED_STANDING),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&io_conf);
    gpio_set_level(LED_WALKING, 0);
    gpio_set_level(LED_SITTING, 0);
    gpio_set_level(LED_STANDING, 0);
}

static void update_leds(const char *activity) {
    gpio_set_level(LED_WALKING,  strcmp(activity, "walking")  == 0 ? 1 : 0);
    gpio_set_level(LED_SITTING,  strcmp(activity, "sitting")  == 0 ? 1 : 0);
    gpio_set_level(LED_STANDING, strcmp(activity, "standing") == 0 ? 1 : 0);
}

// ══════════════════════════════════════════════════
// Serial Label Receive Task
// ══════════════════════════════════════════════════

static void serial_task(void *pvParameters) {
    char line[64];
    int idx = 0;
    while (1) {
        int c = fgetc(stdin);
        if (c == EOF) {
            vTaskDelay(pdMS_TO_TICKS(1));  // 1ms not 10ms
            continue;
        }
        if (c == '\n' || c == '\r') {
            if (idx > 0) {
                line[idx] = '\0';

                // Strip LABEL: prefix if present
                char *payload = line;
                if (strncmp(line, "LABEL:", 6) == 0) {
                    payload = line + 6;
                }

                // Convert to lowercase
                for (int i = 0; payload[i]; i++) {
                    if (payload[i] >= 'A' && payload[i] <= 'Z')
                        payload[i] += 32;
                }

                if (strcmp(payload, "walking")  == 0 ||
                    strcmp(payload, "sitting")   == 0 ||
                    strcmp(payload, "standing")  == 0) {
                    strncpy(current_activity, payload, sizeof(current_activity));
                    update_display(current_activity);
                    update_leds(current_activity);
                    printf("ACK:%s\n", current_activity);
                    fflush(stdout);
                }
                idx = 0;
            }
        } else if (idx < 63) {
            line[idx++] = (char)c;
        }
    }
}

// ══════════════════════════════════════════════════
// WiFi + CSI
// ══════════════════════════════════════════════════

static void wifi_csi_rx_cb(void *ctx, wifi_csi_info_t *data) {
    wifi_csi_info_t d = *data;
    char mac[20] = {0};
    sprintf(mac, "%02X:%02X:%02X:%02X:%02X:%02X",
            d.mac[0], d.mac[1], d.mac[2], d.mac[3], d.mac[4], d.mac[5]);

    printf("CSI_DATA,%s,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%.3f,%d,[",
           "AP", mac,
           d.rx_ctrl.rssi, d.rx_ctrl.rate,
           d.rx_ctrl.sig_mode, d.rx_ctrl.mcs, d.rx_ctrl.cwb,
           d.rx_ctrl.smoothing, d.rx_ctrl.not_sounding,
           d.rx_ctrl.aggregation, d.rx_ctrl.stbc,
           d.rx_ctrl.fec_coding, d.rx_ctrl.sgi,
           d.rx_ctrl.noise_floor, d.rx_ctrl.ampdu_cnt,
           d.rx_ctrl.channel, d.rx_ctrl.secondary_channel,
           d.rx_ctrl.timestamp, d.rx_ctrl.ant,
           d.rx_ctrl.sig_len, d.rx_ctrl.rx_state,
           0, (float)d.rx_ctrl.timestamp / 1000.0,
           d.len);
           int8_t *csi_data = (int8_t *)d.buf;
    for (int i = 0; i < d.len; i++) {
        printf("%d ", csi_data[i]);
    }
    printf("]\n");
    fflush(stdout);
}

static void wifi_event_handler(void *arg, esp_event_base_t base,
                                int32_t event_id, void *event_data) {
    if (base == WIFI_EVENT && event_id == WIFI_EVENT_AP_STACONNECTED) {
        wifi_event_ap_staconnected_t *e = (wifi_event_ap_staconnected_t *)event_data;
        ESP_LOGI(TAG, "Station connected, AID=%d", e->aid);
    }
}

static void softap_init(void) {
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_create_default_wifi_ap();

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));
    ESP_ERROR_CHECK(esp_event_handler_instance_register(
        WIFI_EVENT, ESP_EVENT_ANY_ID, &wifi_event_handler, NULL, NULL));

    wifi_config_t wifi_config = {};
    strncpy((char *)wifi_config.ap.ssid, CONFIG_ESPCSI_WIFI_SSID, 32);
    strncpy((char *)wifi_config.ap.password, CONFIG_ESPCSI_WIFI_PASSWORD, 64);
    wifi_config.ap.ssid_len = strlen(CONFIG_ESPCSI_WIFI_SSID);
    wifi_config.ap.channel = CONFIG_ESPCSI_CHANNEL;
    wifi_config.ap.max_connection = 4;
    wifi_config.ap.authmode = WIFI_AUTH_WPA_WPA2_PSK;
    if (strlen(CONFIG_ESPCSI_WIFI_PASSWORD) == 0) {
        wifi_config.ap.authmode = WIFI_AUTH_OPEN;
    }

    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_AP));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_AP, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());

    ESP_LOGI(TAG, "AP started. SSID:%s", CONFIG_ESPCSI_WIFI_SSID);

    // Enable CSI
    wifi_csi_config_t csi_config = {
        .lltf_en = true,
        .htltf_en = true,
        .stbc_htltf2_en = true,
        .ltf_merge_en = true,
        .channel_filter_en = false,
        .manu_scale = false,
    };
    ESP_ERROR_CHECK(esp_wifi_set_csi_config(&csi_config));
    ESP_ERROR_CHECK(esp_wifi_set_csi_rx_cb(&wifi_csi_rx_cb, NULL));
    ESP_ERROR_CHECK(esp_wifi_set_csi(true));

    // Print CSV header
    printf("type,role,mac,rssi,rate,sig_mode,mcs,bandwidth,smoothing,"
           "not_sounding,aggregation,stbc,fec_coding,sgi,noise_floor,"
           "ampdu_cnt,channel,secondary_channel,local_timestamp,ant,"
           "sig_len,rx_state,real_time_set,real_timestamp,len,CSI_DATA\n");
}

// ══════════════════════════════════════════════════
// app_main
// ══════════════════════════════════════════════════

extern "C" void app_main(void) {
    // NVS
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES ||
        ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    // GPIO
    gpio_init();

    // I2C + OLED
    ESP_ERROR_CHECK(i2c_master_init());
    if (oled_init() == ESP_OK) {
        ESP_LOGI(TAG, "OLED initialized");
        update_display("Waiting...");
    } else {
        ESP_LOGE(TAG, "OLED init failed");
    }

    // WiFi + CSI
    softap_init();

    // Serial receive task
    xTaskCreate(serial_task, "serial_task", 4096, NULL, 5, NULL);

    ESP_LOGI(TAG, "System ready. CSI streaming + OLED active.");
}