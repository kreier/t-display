#include <TFT_eSPI.h> 
#include <SPI.h>
#include "NotoSansBold15.h"
#include "esp_adc_cal.h"

const int pin[13] = {36, 37, 38, 39, 32, 33, 27, 25, 26, 2, 15, 13, 12};
const int batteryPin = 34;

int battery;
int volt;
int vref = 1100;

TFT_eSPI tft = TFT_eSPI();

void setup() {
  Serial.begin(115200);
  tft.init();
  tft.loadFont(NotoSansBold15);
  tft.setTextColor(TFT_GREEN);
  
  esp_adc_cal_characteristics_t adc_chars;
  esp_adc_cal_value_t val_type = esp_adc_cal_characterize((adc_unit_t)ADC_UNIT_1, (adc_atten_t)ADC1_CHANNEL_6, (adc_bits_width_t)ADC_WIDTH_BIT_12, 1100, &adc_chars);
  //Check type of calibration value used to characterize ADC
  if (val_type == ESP_ADC_CAL_VAL_EFUSE_VREF) {
      Serial.printf("eFuse Vref:%u mV", adc_chars.vref);
      vref = adc_chars.vref;
  } else if (val_type == ESP_ADC_CAL_VAL_EFUSE_TP) {
      Serial.printf("Two Point --> coeff_a:%umV coeff_b:%umV\n", adc_chars.coeff_a, adc_chars.coeff_b);
  } else {
      Serial.println("Default Vref: 1100mV");
  }
}

void loop() {
  tft.fillScreen(TFT_BLACK);
  tft.setCursor(0, 0);
  tft.setTextColor(TFT_GREEN);
  tft.print("Battery: ");
  battery = measureVoltage(batteryPin) * 2;
  tft.print(battery);
  tft.println(" mV");
  tft.setTextColor(TFT_WHITE);  
  for(int i = 0; i < 13; i++) {
    volt = measureVoltage(pin[i]);
    if(pin[i]<10) tft.print("  ");
    tft.print(pin[i]);
    tft.print(" - ");
    tft.print(volt);
    tft.println(" mV");
  }
  delay(5000);
}

int measureVoltage(int measurePin) {
  int raw = 0;
  int voltage = 0;
  for(int j = 0; j < 100; j++ ) {
    raw += analogRead(measurePin);
  }
  voltage = int((float)raw / 409500.0 * 3.3 * vref);
  return voltage;
}
