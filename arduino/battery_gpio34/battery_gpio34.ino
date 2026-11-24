#include <TFT_eSPI.h>
#include <SPI.h>
#include "esp_adc_cal.h"

#define ADC_PIN 34
#define ADC_EN  14  // Pin 14 powers the voltage divider on the T-Display

TFT_eSPI tft = TFT_eSPI();
int vref = 1100; // Default reference voltage in mV

void setup() {
  // Enable the built-in voltage divider circuit
  pinMode(ADC_EN, OUTPUT);
  digitalWrite(ADC_EN, HIGH);

  // Initialize display
  tft.init();
  tft.setRotation(1); // Landscape mode (240x135)
  tft.fillScreen(TFT_BLACK);
  tft.setTextDatum(MC_DATUM); // Center text alignment

  // Characterize ADC using factory eFuse calibration values
  esp_adc_cal_characteristics_t adc_chars;
  esp_adc_cal_value_t val_type = esp_adc_cal_characterize(
      ADC_UNIT_1, ADC_ATTEN_DB_11, ADC_WIDTH_BIT_12, 1100, &adc_chars);
      
  if (val_type == ESP_ADC_CAL_VAL_EFUSE_VREF) {
    vref = adc_chars.vref;
  }
}

void loop() {
  // Take an average of 64 samples to smooth out ADC noise
  uint32_t raw = 0;
  for (int i = 0; i < 64; i++) {
    raw += analogRead(ADC_PIN);
    delay(2);
  }
  raw /= 64;

  // Convert raw reading to voltage, multiplying by 2.0 for the 100k/100k divider
  float battery_voltage = ((float)raw / 4095.0) * 2.0 * 3.3 * (vref / 1000.0);

  // Clear previous number and draw the new reading
  tft.fillScreen(TFT_BLACK);
  
  tft.setTextColor(TFT_LIGHTGREY, TFT_BLACK);
  tft.setTextSize(2);
  tft.drawString("Battery Voltage", tft.width() / 2, 35);

  tft.setTextColor(TFT_GREEN, TFT_BLACK);
  tft.setTextSize(4);
  tft.drawString(String(battery_voltage, 2) + " V", tft.width() / 2, 85);

  delay(1000);
}
