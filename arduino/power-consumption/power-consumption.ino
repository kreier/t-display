// Measure the current in different states for generic ESP32 board
// Each stage lasts 10 seconds:
//                                                               USB     LiPo 
// Stage 1: Just started ESP32, only LED activated, waiting     63 mA    40 mA
// Stage 2: WiFi activated, connected to router                 78 mA    72 mA
// Stage 3: Connect to webserver and submit data               120 mA    72 mA
// Stage 4: Switching modems off                                64 mA    72 mA
// Stage 5: Lower CPU speed                                     47 mA
// Stage 6: Going to light sleep now for 30 seconds.            25 mA     0.33 mA
// Stage 7: Wake up from light sleep                            47 mA
// Stage 8: Deep sleep for 30 seconds, then back to 7           24 mA

#include <WiFi.h>
#include <esp_wifi.h>
#include <esp_bt.h>
#include <Wire.h>
#include <credentials.h>  // WiFi credentials in separate file
#include <soc/sens_reg.h>
#include "driver/adc.h"

int ledPin = 2; // T-Display has no LED

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
  Serial.begin(115200);
  Serial.println("."); //                                           Stage 1
  Serial.println("Stage 1: Just activated, 10 seconds ...");
  delay(1000);
  digitalWrite(ledPin, LOW);
  delay(9000);

  flash(2); //                                                      Stage 2
  Serial.println("Stage 2: Starting WiFi now");  
  initWifi();
  delay(10000);
  
  flash(3); //                                                      Stage 3
  Serial.println("Stage 3: Now submitting data to the cloud");   
  makeIFTTTRequest();
  delay(10000);

  flash(4); //                                                      Stage 4
  Serial.println("Stage 4: Switching modems off");
  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);
  btStop();
  adc_power_off();
  esp_wifi_stop();
  esp_bt_controller_disable();  
  delay(10000);


  flash(5); //                                                      Stage 5
  Serial.println("Stage 5: Lower CPU speed");
  setCpuFrequencyMhz(80);
  delay(10000);

  flash(6); //                                                      Stage 6
  //Serial.print("Going to light sleep now for ");
  Serial.print("Stage 6: Going to deep sleep now for ");
  Serial.print(int(TIME_TO_SLEEP));
  Serial.println(" seconds.");
  delay(300);
   
  // The following three lines are for hibernation - reducing to 2.5 µA of the ESP32
  // esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_SLOW_MEM, ESP_PD_OPTION_OFF);
  // esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_FAST_MEM, ESP_PD_OPTION_OFF);
  // esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_PERIPH, ESP_PD_OPTION_OFF);
  
  // enable timer deep sleep
  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  //esp_deep_sleep_start();
  esp_light_sleep_start();
}

void loop() {
  // sleeping so wont get here 
  Serial.println("Something is wrong. I woke up from light sleep.");
  delay(10000);
  Serial.print("Going to light sleep now for ");
  //Serial.print("Going to deep sleep now for ");
  Serial.print(int(TIME_TO_SLEEP));
  Serial.println(" seconds.");
  delay(200);
  //esp_light_sleep_start();
  esp_deep_sleep_start();
}

// Establish a Wi-Fi connection with your router
void initWifi() {
  Serial.print("Connecting to: "); 
  Serial.print(ssid);
  WiFi.begin(ssid, password);  

  int timeout = 10 * 4; // 10 seconds
  while(WiFi.status() != WL_CONNECTED  && (timeout-- > 0)) {
    delay(250);
    Serial.print(".");
  }
  Serial.println("");

  if(WiFi.status() != WL_CONNECTED) {
     Serial.println("Failed to connect, going back to sleep");
  }

  Serial.print("WiFi connected in: "); 
  Serial.print(millis());
  Serial.print(", IP address: "); 
  Serial.println(WiFi.localIP());
}

// Make an HTTP request to the IFTTT web service
void makeIFTTTRequest() {
  Serial.print("Connecting to "); 
  Serial.print(server);
  
  WiFiClient client;
  int retries = 5;
  while(!!!client.connect(server, 80) && (retries-- > 0)) {
    Serial.print(".");
  }
  Serial.println();
  if(!!!client.connected()) {
    Serial.println("Failed to connect...");
  }
  
  Serial.print("Request resource: "); 
  Serial.println(resource);

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
    Serial.println("No response...");
  }
  while(client.available()){
    Serial.write(client.read());
  }
  
  Serial.println("\nclosing connection");
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
