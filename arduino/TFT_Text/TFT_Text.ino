#include <TFT_eSPI.h> 
#include <SPI.h>

TFT_eSPI tft = TFT_eSPI();

void setup() {
  tft.init();
  tft.fillScreen(TFT_BLACK);
  tft.setCursor(0, 0);
  tft.setTextColor(TFT_WHITE);
  tft.setTextWrap(true);
  tft.println("Hello world!");
  delay(1000);
}

void loop() {
  tft.print(".");
  delay(500);
}
