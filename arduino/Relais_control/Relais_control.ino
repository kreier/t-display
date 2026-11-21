/*
 * ======================================================================================
 * Project: Relais Control
 * Platform: LilyGO TTGO T-Display (ESP32, ST7789 240x135 Display)
 *
 * Description:
 *   Controls 5 relays connected to GPIO pins 17, 2, 15, 13, and 12 (adjustable).
 *   Creates a Wi-Fi Soft-AP with an embedded web server & responsive dashboard.
 *   Provides on-device control using the two physical buttons:
 *     - Upper / Right Button (GPIO 35): Cycle through the relays.
 *     - Lower / Left Button  (GPIO 0) : Toggle the selected relay ON / OFF.
 *   The 240x135 color display shows the real-time status of all relays, the active
 *   selection, and Soft-AP network details.
 * ======================================================================================
 */

#include <WiFi.h>
#include <WebServer.h>
#include <DNSServer.h>
#include <SPI.h>
#include <TFT_eSPI.h>

// ======================================================================================
// CONFIGURATION & PIN DEFINITIONS (Adjustable)
// ======================================================================================

// Structure representing a single relay
struct Relay {
  const char* name;
  uint8_t pin;
  bool state;       // true = ON, false = OFF
};

// Relay list with adjustable pins
Relay relays[] = {
  { "Relais 1", 17, false },
  { "Relais 2",  2, false },
  { "Relais 3", 15, false },
  { "Relais 4", 13, false },
  { "Relais 5", 12, false }
};

const uint8_t NUM_RELAYS = sizeof(relays) / sizeof(relays[0]);

// Relay trigger logic:
// Set true if your relay board is Active-LOW (standard for most optocoupler relay boards)
// Set false if your relay board is Active-HIGH
#define RELAY_ACTIVE_LOW    true

// TTGO T-Display Physical Button Pins
#define BTN_CYCLE_PIN       35    // Upper/Right button: cycle through relays
#define BTN_TOGGLE_PIN      0     // Lower/Left button: toggle selected relay

// Capacitive Touch Sensor Pins (Just connect a free wire to each!)
#define ENABLE_TOUCH        true  // Set to true to enable touch inputs on pins 32 & 33
#define TOUCH_CYCLE_PIN     32    // GPIO 32 (Touch 9): Touch wire to cycle selection
#define TOUCH_TOGGLE_PIN    33    // GPIO 33 (Touch 8): Touch wire to toggle selected relay
#define TOUCH_THRESHOLD     35    // Typical untouched: 65-95. Touched: 10-25.

// TTGO T-Display Backlight Control Pin
#define TFT_BL_PIN          4

// Wi-Fi Soft-AP Settings
#define AP_SSID             "Relais-Control-AP"
#define AP_PASS             "12345678"   // Minimum 8 characters. Set to "" for open network
#define AP_CHANNEL          1
#define AP_MAX_CONN         4
#define DNS_PORT            53

// Display Settings
#define DISPLAY_ROTATION    1     // 1 = Landscape (240x135), USB connector on left

// Custom RGB565 Colors for Modern UI
#define COLOR_BG            0x0841  // Very dark slate background
#define COLOR_HEADER_BG     0x10A2  // Dark blue-grey header
#define COLOR_CARD_NORMAL   0x18C3  // Card background
#define COLOR_CARD_BORDER   0x2965  // Subtle border
#define COLOR_CARD_SEL      0x020C  // Highlighted card for selected relay
#define COLOR_CARD_SEL_BD   0x05BF  // Cyan border for selected relay
#define COLOR_ON_BG         0x05E0  // Bright emerald green for ON badge
#define COLOR_ON_TXT        0x0000  // Black text on green
#define COLOR_OFF_BG        0x39E7  // Muted grey for OFF badge
#define COLOR_OFF_TXT       0xCE59  // Light grey text on dark badge
#define COLOR_ACCENT        0x04FF  // Cyan accent
#define COLOR_DIVIDER       0x2124  // Subtle divider line

// ======================================================================================
// GLOBAL OBJECTS & STATE
// ======================================================================================

TFT_eSPI tft = TFT_eSPI();
WebServer server(80);
DNSServer dnsServer;

int selectedRelay = 0;              // Currently highlighted relay index (0 to NUM_RELAYS-1)
uint8_t lastClientCount = 255;      // Tracks connected Wi-Fi clients
unsigned long lastClientCheck = 0;

// Button Debounce Handler
struct DebouncedButton {
  uint8_t pin;
  bool lastState;
  bool stableState;
  unsigned long lastDebounceTime;

  void init(uint8_t p) {
    pin = p;
    pinMode(pin, INPUT);            // Both GPIO 35 & 0 have external pullups on T-Display
    lastState = digitalRead(pin);
    stableState = lastState;
    lastDebounceTime = 0;
  }

  bool wasPressed() {
    bool reading = digitalRead(pin);
    bool pressed = false;

    if (reading != lastState) {
      lastDebounceTime = millis();
      lastState = reading;
    }

    if ((millis() - lastDebounceTime) > 35) { // 35ms debounce window
      if (reading != stableState) {
        stableState = reading;
        if (stableState == LOW) {              // Trigger on button press (active LOW)
          pressed = true;
        }
      }
    }
    return pressed;
  }
};

DebouncedButton btnCycle;
DebouncedButton btnToggle;

// Capacitive Touch Handler
struct DebouncedTouch {
  uint8_t pin;
  uint16_t threshold;
  bool isTouched;
  unsigned long lastActionTime;

  void init(uint8_t p, uint16_t thresh) {
    pin = p;
    threshold = thresh;
    isTouched = false;
    lastActionTime = 0;
  }

  bool wasTouched() {
    uint16_t val = touchRead(pin);
    bool pressed = false;
    // When touched by human hand, the capacitance increases and touchRead() value drops
    if (val < threshold) {
      if (!isTouched && (millis() - lastActionTime > 250)) {
        isTouched = true;
        lastActionTime = millis();
        pressed = true;
      }
    } else if (val > (threshold + 10)) {
      if (isTouched && (millis() - lastActionTime > 100)) {
        isTouched = false;
      }
    }
    return pressed;
  }
};

DebouncedTouch touchCycle;
DebouncedTouch touchToggle;

// ======================================================================================
// HTML, CSS & JAVASCRIPT WEB INTERFACE (Stored in Flash PROGMEM)
// ======================================================================================

const char INDEX_HTML[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
  <title>ESP32 Relais Control</title>
  <style>
    :root {
      --bg: #0f172a;
      --card-bg: #1e293b;
      --card-border: #334155;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --accent: #38bdf8;
      --green: #10b981;
      --red: #ef4444;
      --green-glow: rgba(16, 185, 129, 0.25);
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    body { background-color: var(--bg); color: var(--text); padding: 16px; display: flex; justify-content: center; }
    .container { width: 100%; max-width: 480px; }
    header { text-align: center; margin-bottom: 20px; padding: 12px; background: var(--card-bg); border-radius: 12px; border: 1px solid var(--card-border); }
    h1 { font-size: 1.4rem; color: var(--accent); margin-bottom: 4px; display: flex; align-items: center; justify-content: center; gap: 8px; }
    .status-bar { font-size: 0.82rem; color: var(--text-muted); display: flex; justify-content: space-between; margin-top: 8px; padding-top: 8px; border-top: 1px solid var(--card-border); }
    .global-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 16px; }
    .btn-global {
      padding: 10px; border-radius: 8px; border: none; font-weight: 600; font-size: 0.9rem; cursor: pointer;
      display: flex; align-items: center; justify-content: center; gap: 6px; transition: transform 0.1s, opacity 0.2s;
    }
    .btn-global:active { transform: scale(0.98); }
    .btn-all-on { background: #059669; color: white; }
    .btn-all-off { background: #dc2626; color: white; }
    .relay-list { display: flex; flex-direction: column; gap: 12px; }
    .relay-card {
      background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 12px;
      padding: 14px 16px; display: flex; align-items: center; justify-content: space-between;
      transition: border-color 0.2s, box-shadow 0.2s;
    }
    .relay-card.is-on { border-color: var(--green); box-shadow: 0 0 12px var(--green-glow); }
    .relay-info { display: flex; flex-direction: column; }
    .relay-name { font-size: 1.1rem; font-weight: 600; margin-bottom: 2px; }
    .relay-pin { font-size: 0.78rem; color: var(--text-muted); }
    .switch-wrap { display: flex; align-items: center; gap: 10px; }
    .badge {
      font-size: 0.75rem; font-weight: 700; padding: 4px 8px; border-radius: 6px; min-width: 42px; text-align: center;
      text-transform: uppercase;
    }
    .badge-on { background: var(--green); color: #000; }
    .badge-off { background: #475569; color: #cbd5e1; }
    .toggle-switch {
      position: relative; display: inline-block; width: 56px; height: 30px; cursor: pointer;
    }
    .toggle-switch input { opacity: 0; width: 0; height: 0; }
    .slider {
      position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0;
      background-color: #475569; transition: .25s; border-radius: 30px;
    }
    .slider:before {
      position: absolute; content: ""; height: 22px; width: 22px; left: 4px; bottom: 4px;
      background-color: white; transition: .25s; border-radius: 50%;
    }
    input:checked + .slider { background-color: var(--green); }
    input:checked + .slider:before { transform: translateX(26px); }
    footer { text-align: center; margin-top: 24px; font-size: 0.78rem; color: var(--text-muted); }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>&#x26A1; ESP32 Relais Control</h1>
      <div class="status-bar">
        <span>SSID: <b>Relais-Control-AP</b></span>
        <span id="connStatus">&#x1F7E2; Connected</span>
      </div>
    </header>

    <div class="global-actions">
      <button class="btn-global btn-all-on" onclick="setAll(1)">&#x2705; ALL ON</button>
      <button class="btn-global btn-all-off" onclick="setAll(0)">&#x274C; ALL OFF</button>
    </div>

    <div class="relay-list" id="relayList">
      <!-- Populated dynamically via JavaScript -->
    </div>

    <footer>
      T-Display ESP32 &bull; Upper Btn: Cycle &bull; Lower Btn: Toggle
    </footer>
  </div>

  <script>
    let isFetching = false;

    async function fetchStatus() {
      if (isFetching) return;
      try {
        isFetching = true;
        const res = await fetch('/status');
        if (!res.ok) throw new Error('Network error');
        const data = await res.json();
        renderRelays(data.relays);
        document.getElementById('connStatus').innerHTML = '&#x1F7E2; Connected (' + data.clients + ' cli)';
      } catch (err) {
        document.getElementById('connStatus').innerHTML = '&#x1F534; Disconnected';
      } finally {
        isFetching = false;
      }
    }

    function renderRelays(relays) {
      const container = document.getElementById('relayList');
      container.innerHTML = '';
      relays.forEach((r, idx) => {
        const card = document.createElement('div');
        card.className = 'relay-card ' + (r.state ? 'is-on' : '');
        card.innerHTML = `
          <div class="relay-info">
            <span class="relay-name">${r.name}</span>
            <span class="relay-pin">GPIO Pin: ${r.pin}</span>
          </div>
          <div class="switch-wrap">
            <span class="badge ${r.state ? 'badge-on' : 'badge-off'}">${r.state ? 'ON' : 'OFF'}</span>
            <label class="toggle-switch">
              <input type="checkbox" ${r.state ? 'checked' : ''} onchange="toggleRelay(${idx}, this.checked)">
              <span class="slider"></span>
            </label>
          </div>
        `;
        container.appendChild(card);
      });
    }

    async function toggleRelay(index, state) {
      try {
        await fetch(`/set?id=${index}&state=${state ? 1 : 0}`);
        fetchStatus();
      } catch (e) {
        console.error(e);
      }
    }

    async function setAll(state) {
      try {
        await fetch(`/all?state=${state}`);
        fetchStatus();
      } catch (e) {
        console.error(e);
      }
    }

    // Initial load and periodic polling every 1000ms
    fetchStatus();
    setInterval(fetchStatus, 1000);
  </script>
</body>
</html>
)rawliteral";

// ======================================================================================
// HARDWARE OUTPUT CONTROL
// ======================================================================================

void applyRelayState(int index) {
  if (index < 0 || index >= NUM_RELAYS) return;
  bool physicalLevel;
  if (RELAY_ACTIVE_LOW) {
    physicalLevel = relays[index].state ? LOW : HIGH;
  } else {
    physicalLevel = relays[index].state ? HIGH : LOW;
  }
  digitalWrite(relays[index].pin, physicalLevel);
}

void applyAllRelays() {
  for (int i = 0; i < NUM_RELAYS; i++) {
    applyRelayState(i);
  }
}

// ======================================================================================
// TFT DISPLAY DRAWING FUNCTIONS
// ======================================================================================

void drawHeader() {
  tft.fillRect(0, 0, 240, 18, COLOR_HEADER_BG);
  tft.setTextDatum(TL_DATUM);
  tft.setTextColor(TFT_WHITE, COLOR_HEADER_BG);
  tft.drawString("AP: Relais-Control", 6, 2, 2);

  tft.setTextDatum(TR_DATUM);
  tft.setTextColor(COLOR_ACCENT, COLOR_HEADER_BG);
  tft.drawString("192.168.4.1", 234, 2, 2);

  tft.drawFastHLine(0, 18, 240, COLOR_DIVIDER);
}

void drawRelayRow(int i) {
  if (i < 0 || i >= NUM_RELAYS) return;

  // Row vertical positioning: 5 rows starting at y=20, each 18px high + 1px spacing
  int y = 20 + i * 19;
  bool isSelected = (i == selectedRelay);

  // Card Background & Border
  if (isSelected) {
    tft.fillRoundRect(3, y, 234, 18, 3, COLOR_CARD_SEL);
    tft.drawRoundRect(3, y, 234, 18, 3, COLOR_CARD_SEL_BD);
  } else {
    tft.fillRoundRect(3, y, 234, 18, 3, COLOR_CARD_NORMAL);
    tft.drawRoundRect(3, y, 234, 18, 3, COLOR_CARD_BORDER);
  }

  // Cursor indicator
  tft.setTextDatum(ML_DATUM);
  if (isSelected) {
    tft.setTextColor(COLOR_ACCENT, COLOR_CARD_SEL);
    tft.drawString(">", 7, y + 9, 2);
  }

  // Relay Name
  uint16_t txtBg = isSelected ? COLOR_CARD_SEL : COLOR_CARD_NORMAL;
  tft.setTextColor(TFT_WHITE, txtBg);
  tft.drawString(relays[i].name, 20, y + 9, 2);

  // Pin Number label
  char pinBuf[12];
  snprintf(pinBuf, sizeof(pinBuf), "(P%d)", relays[i].pin);
  tft.setTextColor(TFT_LIGHTGREY, txtBg);
  tft.drawString(pinBuf, 105, y + 9, 1);

  // Status Badge (ON / OFF)
  int badgeX = 174;
  int badgeY = y + 2;
  int badgeW = 58;
  int badgeH = 14;

  if (relays[i].state) {
    tft.fillRoundRect(badgeX, badgeY, badgeW, badgeH, 2, COLOR_ON_BG);
    tft.setTextDatum(MC_DATUM);
    tft.setTextColor(COLOR_ON_TXT, COLOR_ON_BG);
    tft.drawString("ON", badgeX + (badgeW / 2), badgeY + (badgeH / 2), 2);
  } else {
    tft.fillRoundRect(badgeX, badgeY, badgeW, badgeH, 2, COLOR_OFF_BG);
    tft.setTextDatum(MC_DATUM);
    tft.setTextColor(COLOR_OFF_TXT, COLOR_OFF_BG);
    tft.drawString("OFF", badgeX + (badgeW / 2), badgeY + (badgeH / 2), 2);
  }
}

void drawFooter() {
  tft.drawFastHLine(0, 116, 240, COLOR_DIVIDER);
  tft.fillRect(0, 117, 240, 18, COLOR_BG);

  tft.setTextDatum(TL_DATUM);
  tft.setTextColor(TFT_LIGHTGREY, COLOR_BG);
  tft.drawString("[UP] Next", 6, 120, 1);

  tft.setTextDatum(TC_DATUM);
  tft.drawString("[DN] Toggle", 120, 120, 1);

  uint8_t clients = WiFi.softAPgetStationNum();
  char cliBuf[16];
  snprintf(cliBuf, sizeof(cliBuf), "Cli: %d", clients);
  tft.setTextDatum(TR_DATUM);
  tft.setTextColor(COLOR_ACCENT, COLOR_BG);
  tft.drawString(cliBuf, 234, 120, 1);
}

void drawFullDisplay() {
  tft.fillScreen(COLOR_BG);
  drawHeader();
  for (int i = 0; i < NUM_RELAYS; i++) {
    drawRelayRow(i);
  }
  drawFooter();
}

// ======================================================================================
// WEB SERVER HANDLERS
// ======================================================================================

void handleRoot() {
  server.send_P(200, "text/html", INDEX_HTML);
}

void handleStatus() {
  String json = "{\"clients\":" + String(WiFi.softAPgetStationNum()) + ",\"relays\":[";
  for (int i = 0; i < NUM_RELAYS; i++) {
    json += "{\"id\":" + String(i) + ",";
    json += "\"name\":\"" + String(relays[i].name) + "\",";
    json += "\"pin\":" + String(relays[i].pin) + ",";
    json += "\"state\":" + String(relays[i].state ? "true" : "false") + "}";
    if (i < NUM_RELAYS - 1) json += ",";
  }
  json += "]}";
  server.send(200, "application/json", json);
}

void handleToggle() {
  if (server.hasArg("id")) {
    int id = server.arg("id").toInt();
    if (id >= 0 && id < NUM_RELAYS) {
      relays[id].state = !relays[id].state;
      applyRelayState(id);
      drawRelayRow(id);
      server.send(200, "application/json", "{\"success\":true}");
      return;
    }
  }
  server.send(400, "application/json", "{\"error\":\"Invalid ID\"}");
}

void handleSet() {
  if (server.hasArg("id") && server.hasArg("state")) {
    int id = server.arg("id").toInt();
    int state = server.arg("state").toInt();
    if (id >= 0 && id < NUM_RELAYS) {
      relays[id].state = (state == 1);
      applyRelayState(id);
      drawRelayRow(id);
      server.send(200, "application/json", "{\"success\":true}");
      return;
    }
  }
  server.send(400, "application/json", "{\"error\":\"Missing or invalid parameters\"}");
}

void handleAll() {
  if (server.hasArg("state")) {
    int state = server.arg("state").toInt();
    bool targetState = (state == 1);
    for (int i = 0; i < NUM_RELAYS; i++) {
      relays[i].state = targetState;
      applyRelayState(i);
      drawRelayRow(i);
    }
    server.send(200, "application/json", "{\"success\":true}");
    return;
  }
  server.send(400, "application/json", "{\"error\":\"Missing state parameter\"}");
}

void handleNotFound() {
  // Captive portal redirect: redirect unknown requests to root
  server.sendHeader("Location", "http://192.168.4.1/", true);
  server.send(302, "text/plain", "Redirecting to Relais Control...");
}

// ======================================================================================
// ARDUINO SETUP
// ======================================================================================

void setup() {
  Serial.begin(115200);
  delay(100);
  Serial.println("\n--- ESP32 Relais Control Initializing ---");

  // 1. Initialize Relay Output Pins
  // Set initial state before enabling output mode to prevent pin glitching
  for (int i = 0; i < NUM_RELAYS; i++) {
    bool initialLevel = RELAY_ACTIVE_LOW ? HIGH : LOW; // OFF state
    digitalWrite(relays[i].pin, initialLevel);
    pinMode(relays[i].pin, OUTPUT);
    Serial.printf("Configured %s on GPIO %d [OFF]\n", relays[i].name, relays[i].pin);
  }

  // 2. Initialize Hardware Buttons & Touch Inputs
  btnCycle.init(BTN_CYCLE_PIN);
  btnToggle.init(BTN_TOGGLE_PIN);
#if ENABLE_TOUCH
  touchCycle.init(TOUCH_CYCLE_PIN, TOUCH_THRESHOLD);
  touchToggle.init(TOUCH_TOGGLE_PIN, TOUCH_THRESHOLD);
  Serial.printf("Touch enabled: Wire on GPIO %d (Cycle), Wire on GPIO %d (Toggle)\n",
                TOUCH_CYCLE_PIN, TOUCH_TOGGLE_PIN);
#endif

  // 3. Initialize Display & Backlight
  if (TFT_BL_PIN > 0) {
    pinMode(TFT_BL_PIN, OUTPUT);
    digitalWrite(TFT_BL_PIN, HIGH);   // Turn on backlight
  }
  tft.init();
  tft.setRotation(DISPLAY_ROTATION);
  drawFullDisplay();

  // 4. Start Wi-Fi Soft-AP
  WiFi.mode(WIFI_AP);
  IPAddress local_ip(192, 168, 4, 1);
  IPAddress gateway(192, 168, 4, 1);
  IPAddress subnet(255, 255, 255, 0);
  WiFi.softAPConfig(local_ip, gateway, subnet);

  if (strlen(AP_PASS) >= 8) {
    WiFi.softAP(AP_SSID, AP_PASS, AP_CHANNEL, 0, AP_MAX_CONN);
  } else {
    WiFi.softAP(AP_SSID); // Open network
  }

  Serial.print("Soft-AP Started. SSID: ");
  Serial.println(AP_SSID);
  Serial.print("AP IP Address: ");
  Serial.println(WiFi.softAPIP());

  // 5. Start DNS Server for Captive Portal
  dnsServer.start(DNS_PORT, "*", local_ip);

  // 6. Configure Web Server Routes
  server.on("/", HTTP_GET, handleRoot);
  server.on("/status", HTTP_GET, handleStatus);
  server.on("/toggle", HTTP_GET, handleToggle);
  server.on("/set", HTTP_GET, handleSet);
  server.on("/all", HTTP_GET, handleAll);

  // Captive portal probes for Android / iOS / Windows
  server.on("/generate_204", HTTP_GET, handleRoot);
  server.on("/fwlink", HTTP_GET, handleRoot);
  server.on("/hotspot-detect.html", HTTP_GET, handleRoot);
  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP Web Server Started.");

  // Redraw display with AP info
  drawFullDisplay();
}

// ======================================================================================
// MAIN LOOP
// ======================================================================================

void loop() {
  // 1. Process Web Server & DNS Requests
  dnsServer.processNextRequest();
  server.handleClient();

  // 2. Handle Cycle Input (Physical Button 1 or Wire Touch on Pin 32)
  bool cycleTriggered = btnCycle.wasPressed();
#if ENABLE_TOUCH
  if (!cycleTriggered && touchCycle.wasTouched()) {
    cycleTriggered = true;
    Serial.println("[Touch 32] Cycle trigger");
  }
#endif
  if (cycleTriggered) {
    int prevSelected = selectedRelay;
    selectedRelay = (selectedRelay + 1) % NUM_RELAYS;
    Serial.printf("Selected relay changed to: %d (%s)\n", selectedRelay, relays[selectedRelay].name);
    // Redraw only the previously selected row and newly selected row (flicker-free)
    drawRelayRow(prevSelected);
    drawRelayRow(selectedRelay);
  }

  // 3. Handle Toggle Input (Physical Button 2 or Wire Touch on Pin 33)
  bool toggleTriggered = btnToggle.wasPressed();
#if ENABLE_TOUCH
  if (!toggleTriggered && touchToggle.wasTouched()) {
    toggleTriggered = true;
    Serial.println("[Touch 33] Toggle trigger");
  }
#endif
  if (toggleTriggered) {
    relays[selectedRelay].state = !relays[selectedRelay].state;
    applyRelayState(selectedRelay);
    Serial.printf("Toggled %s (GPIO %d) -> %s\n",
                  relays[selectedRelay].name,
                  relays[selectedRelay].pin,
                  relays[selectedRelay].state ? "ON" : "OFF");
    drawRelayRow(selectedRelay);
  }

  // 4. Periodically update connected client count on display footer
  if (millis() - lastClientCheck > 2000) {
    lastClientCheck = millis();
    uint8_t currentClients = WiFi.softAPgetStationNum();
    if (currentClients != lastClientCount) {
      lastClientCount = currentClients;
      drawFooter();
    }
  }
}
