// Measure the current in different states for generic ESP32 board
// Each stage lasts 10 seconds:
//                                                               USB     LiPo 
// Stage 1: Just started ESP32, only LED activated, waiting     63 mA    66 mA
// Stage 2: WiFi activated, connected to router                 78 mA   120 mA
// Stage 3: Connect to webserver and submit data               120 mA   144 mA - 85 mA
// Stage 4: Switching modems off                                64 mA    67 mA
// Stage 5: Lower CPU speed                                     47 mA    49 mA
// Stage 6: Going to light sleep now for 30 seconds.       10 - 25 mA     9 mA
// Stage 7: Wake up from light sleep                            47 mA    49 mA
// Stage 8: Deep sleep for 30 seconds, then back to 7       8 - 24 mA     7 mA  - how 0.34 mA??

#include <TFT_eSPI.h> 
#include <SPI.h>
#include <WiFi.h>
#include <esp_wifi.h>
#include <esp_bt.h>
#include <Wire.h>
#include <credentials.h>  // WiFi credentials in separate file
#include <soc/sens_reg.h>
#include "driver/adc.h"

int ledPin = 2; // T-Display has no LED

TFT_eSPI tft = TFT_eSPI();

// Replace with your SSID and Password + uncomment
// const char* ssid     = "REPLACE_WITH_YOUR_SSID";
// const char* password = "REPLACE_WITH_YOUR_PASSWORD";

// Replace with your unique IFTTT URL resource + uncomment
// const char* resource = "/trigger/data/with/key/value";

// Maker Webhooks IFTTT
const char* server = "maker.ifttt.com";

// Time to sleep
uint64_t uS_TO_S_FACTOR = 1000000;  // Conversion factor for micro seconds to seconds
// sleep for 30 seconds
uint64_t TIME_TO_SLEEP = 30;

int adcValue = 0;

void setup() {
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);  
  tft.init();
  tft.fillScreen(TFT_BLACK);
  tft.setCursor(0, 0);
  tft.setTextColor(TFT_WHITE);
  tft.setTextWrap(true); //                                         Stage 1
  tft.println("Stage 1:");
  tft.println("Just activated, 10 seconds ...");
  tft.println(" ");
  delay(1000);
  digitalWrite(ledPin, LOW);
  delay(9000);

  flash(2); //                                                      Stage 2
  tft.println("Stage 2:");
  tft.println("Starting WiFi now");  
  initWifi();
  tft.println(" ");
  delay(10000);
  
  flash(3); //                                                      Stage 3
  tft.println("Stage 3:");
  tft.println("Now submitting data to the cloud");
  tft.println(" ");
  delay(2000);
  tft.fillScreen(TFT_BLACK);
  tft.setCursor(0, 0);  
  makeIFTTTRequest();
  delay(10000);

  flash(4); //                                                      Stage 4
  tft.fillScreen(TFT_BLACK);
  tft.setCursor(0, 0);  
  tft.println("Stage 4:");
  tft.println("Switching modems off");
  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);
  btStop();
  adc_power_off();
  esp_wifi_stop();
  esp_bt_controller_disable();  
  tft.println(" ");
  delay(10000);


  flash(5); //                                                      Stage 5
  tft.println("Stage 5:");
  tft.println("Lower CPU speed");
  setCpuFrequencyMhz(80);
  tft.println(" ");
  delay(10000);

  tft.println("Stage 5a: switch of backlight");
  delay(2000);
  pinMode(4, OUTPUT);
  digitalWrite(4, LOW);
  delay(8000);
  digitalWrite(4, HIGH);

  flash(6); //                                                      Stage 6
  //tft.print("Going to light sleep now for ");
  tft.print("Stage 6:");
  tft.println("Going to light sleep now for ");
  tft.print(int(TIME_TO_SLEEP));
  tft.println(" seconds.");
  tft.println(" ");
  delay(2000);
   
  // The following three lines are for hibernation - reducing to 2.5 µA of the ESP32
  esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_SLOW_MEM, ESP_PD_OPTION_OFF);
  esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_FAST_MEM, ESP_PD_OPTION_OFF);
  esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_PERIPH, ESP_PD_OPTION_OFF);
  
  // enable timer deep sleep
  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  //esp_deep_sleep_start();
  esp_light_sleep_start();
}

void loop() {
  // sleeping so wont get here 
  tft.println("Something is wrong.");
  tft.println("I woke up from light sleep.");
  delay(10000);
  tft.print("Going to deep sleep now for ");
  //tft.print("Going to deep sleep now for ");
  tft.print(int(TIME_TO_SLEEP));
  tft.println(" seconds.");
  delay(2000);
  //esp_light_sleep_start();
  esp_deep_sleep_start();
}

// Establish a Wi-Fi connection with your router
void initWifi() {
  tft.print("Connecting to: "); 
  tft.print(ssid);
  WiFi.begin(ssid, password);  

  int timeout = 10 * 4; // 10 seconds
  while(WiFi.status() != WL_CONNECTED  && (timeout-- > 0)) {
    delay(250);
    tft.print(".");
  }
  tft.println("");

  if(WiFi.status() != WL_CONNECTED) {
     tft.println("Failed to connect, going back to sleep");
  }

  tft.print("WiFi connected in: "); 
  tft.print(millis());
  tft.print(", IP address: "); 
  tft.println(WiFi.localIP());
}

// Make an HTTP request to the IFTTT web service
void makeIFTTTRequest() {
  tft.print("Connecting to "); 
  tft.print(server);
  
  WiFiClient client;
  int retries = 5;
  while(!!!client.connect(server, 80) && (retries-- > 0)) {
    tft.print(".");
  }
  tft.println();
  if(!!!client.connected()) {
    tft.println("Failed to connect...");
  }
  
  tft.print("Request resource: "); 
  //tft.println(resource);

  // raw and converted voltage reading
  adcValue = analogRead( 34 );
  String jsonObject = String("{\"value1\":\"") + adcValue + "\",\"value2\":\"" + (adcValue * 2.4)
                      + "\",\"value3\":\"" + millis() + "\"}";
                      
  // Comment the previous line and uncomment the next line to publish temperature readings in Fahrenheit                    
  /*String jsonObject = String("{\"value1\":\"") + (1.8 * bme.readTemperature() + 32) + "\",\"value2\":\"" 
                      + (bme.readPressure()/100.0F) + "\",\"value3\":\"" + bme.readHumidity() + "\"}";*/
                      
  client.println(String("POST ") + resource + " HTTP/1.1");
  client.println(String("Host: ") + server); 
  client.println("Connection: close\r\nContent-Type: application/json");
  client.print("Content-Length: ");
  client.println(jsonObject.length());
  client.println();
  client.println(jsonObject);
        
  int timeout = 5 * 10; // 5 seconds             
  while(!!!client.available() && (timeout-- > 0)){
    delay(100);
  }
  if(!!!client.available()) {
    tft.println("No response...");
  }
  while(client.available()){
    tft.write(client.read());
  }
  
  tft.println("\nclosing connection");
  client.stop(); 
}

void flash(int times) {
  for(int i = 0; i < times; i++) {
    digitalWrite(ledPin, HIGH);
    delay(50);
    digitalWrite(ledPin, LOW);
    delay(200);
  }
}
