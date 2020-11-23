// A fun MATRIX-like screen demo of scrolling
// Screen will flicker initially until fully drawn
// then scroll smoothly

// Needs GLCD font

/*
 Make sure all the display driver and pin comnenctions are correct by
 editting the User_Setup.h file in the TFT_eSPI library folder.

 #########################################################################
 ###### DON'T FORGET TO UPDATE THE User_Setup.h FILE IN THE LIBRARY ######
 #########################################################################
*/

#include <TFT_eSPI.h> // Hardware-specific library
#include <SPI.h>

TFT_eSPI tft = TFT_eSPI();       // Invoke custom library

#define TEXT_HEIGHT 8 // Height of text to be printed and scrolled
#define BOT_FIXED_AREA 0  // Number of lines in bottom fixed area (lines counted from bottom of screen)
#define TOP_FIXED_AREA 0  // Number of lines in top fixed area (lines counted from top of screen)

uint16_t yStart = TOP_FIXED_AREA;
uint16_t yArea = 240 - TOP_FIXED_AREA - BOT_FIXED_AREA;
uint16_t yDraw = 240 - BOT_FIXED_AREA - TEXT_HEIGHT;
byte     pos[42];
uint16_t xPos = 0;

void setup() {
  Serial.begin(115200);
  randomSeed(analogRead(A0));
  tft.init();
  tft.setRotation(0);
  tft.fillScreen(TFT_BLACK);
  setupScrollArea(TOP_FIXED_AREA, BOT_FIXED_AREA);
}

void loop(void) {
// First fill the screen with random streaks of characters
  for (int j = 0; j < 400; j += TEXT_HEIGHT) {
    for (int i = 0; i < 40; i++) {
      // Rapid fade initially brightness values
      if (pos[i] > 20)
        pos[i] -= 3;
      // Slow fade later
      if (pos[i] > 0)
        pos[i] -= 1;
      // ~1 in 20 probability of a new character
      if ((random(20) == 1) && (j < 200))
        pos[i] = 63;
      // Set the green character brightness
      tft.setTextColor(pos[i] << 5, TFT_BLACK);
      // Draw white character
      if (pos[i] == 63)
        tft.setTextColor(TFT_WHITE, TFT_BLACK);
      // Draw the character
      xPos += tft.drawChar(random(32, 128), xPos, yDraw, 1);
    }
    // Scroll, 14ms per pixel line
    yDraw = scroll_slow(TEXT_HEIGHT, 14);
    xPos = 0;
  }

  // Now scroll smoothly forever
  while (1) {
    yield();
    yDraw = scroll_slow(240, 5);
  } // Scroll 320 lines, 5ms per line

}

void setupScrollArea(uint16_t TFA, uint16_t BFA) {
  // Vertical scroll definition
  tft.writecommand(ST7789_VSCRDEF);
  tft.writedata(TFA >> 8);
  tft.writedata(TFA);
  tft.writedata((240 - TFA - BFA) >> 8);
  tft.writedata(240 - TFA - BFA);
  tft.writedata(BFA >> 8);
  tft.writedata(BFA);
}

int scroll_slow(int lines, int wait) {
  int yTemp = yStart;
  for (int i = 0; i < lines; i++) {
    yStart++;
    if (yStart == 240 - BOT_FIXED_AREA)
      yStart = TOP_FIXED_AREA;
    scrollAddress(yStart);
    delay(wait);
  }
  return yTemp;
}

void scrollAddress(uint16_t VSP) {
  // Vertical scrolling start address
  tft.writecommand(0x37); // ILI9341_VSCRSADD);
  tft.writedata(VSP >> 8);
  tft.writedata(VSP);
}
