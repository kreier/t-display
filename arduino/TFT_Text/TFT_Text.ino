#include <TFT_eSPI.h> 
#include <SPI.h>

TFT_eSPI tft = TFT_eSPI();

void setup() {
  tft.init();
  tft.fillScreen(TFT_BLACK);
  tft.setCursor(0, 0);
  tft.setTextColor(TFT_GREEN);
}

void loop() {
  tft.print("Hello world! ");
  delay(1000);
 // pinMode(4, OUTPUT);
 // digitalWrite(4, LOW); switch off backlight
}
