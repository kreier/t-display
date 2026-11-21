# Relais Control for LilyGO TTGO T-Display (ESP32)

A dedicated relay controller firmware for the **LilyGO TTGO T-Display** (ESP32 with 1.14" 240x135 ST7789 IPS LCD).

---

## Features

- **5 Relay Outputs (Adjustable)**: Controls relays connected to GPIO pins **17, 2, 15, 13, and 12**.
- **Soft-AP & Web Dashboard**: Creates a standalone Wi-Fi Access Point (`Relais-Control-AP`). Connect with any phone or computer to access a responsive dark-mode touch control panel at `http://192.168.4.1`.
- **Live AJAX State Sync**: Physical button presses and Web UI toggles sync instantly without manual page reloads.
- **Physical Button & Capacitive Touch Controls**:
  - **Upper / Right Button (GPIO 35)** or **Wire Touch (GPIO 32)**: Cycle through relays.
  - **Lower / Left Button (GPIO 0)** or **Wire Touch (GPIO 33)**: Toggle the currently highlighted relay ON or OFF.
- **240x135 Color Display UI**: High-contrast, flicker-free dashboard showing each relay's name, GPIO pin, active cursor, ON/OFF status badge, Soft-AP IP, and connected Wi-Fi client count.
- **Captive Portal**: Automatically prompts or redirects connected mobile devices to the control dashboard.
- **Configurable Relay Logic**: Easily switch between **Active-LOW** (common optocoupler relay boards) and **Active-HIGH**.

---

## Hardware Pinout

| Function / Component | GPIO Pin | Notes |
| :--- | :---: | :--- |
| **Relais 1** | **17** | General I/O on expansion header |
| **Relais 2** | **2** | General I/O on expansion header |
| **Relais 3** | **15** | General I/O on expansion header |
| **Relais 4** | **13** | General I/O on expansion header |
| **Relais 5** | **12** | General I/O on expansion header |
| **Touch Cycle Input** | **32** | Capacitive Touch 9 (attach wire to touch with hand) |
| **Touch Toggle Input** | **33** | Capacitive Touch 8 (attach wire to touch with hand) |
| **Upper / Right Button** | **35** | Built-in push button (cycles selection) |
| **Lower / Left Button** | **0** | Built-in push button (toggles selected relay) |
| **Display Backlight (BL)** | **4** | Automatically driven HIGH |
| **Display SPI (ST7789)** | 19 (MOSI), 18 (SCLK), 5 (CS), 16 (DC), 23 (RST) | Standard TTGO T-Display wiring |

> [!NOTE]
> All 5 relay pins (`17`, `2`, `15`, `13`, `12`) are positioned together along the 12-pin header of the TTGO T-Display board, making wiring to multi-channel relay modules straightforward.

---

## Quick Start Guide

### 1. Arduino IDE Setup
1. Open the Arduino IDE.
2. Ensure you have the **ESP32** board package installed via the Boards Manager:
   - *Tools* > *Board* > *ESP32 Arduino* > **TTGO T1** (or **ESP32 Dev Module**).
3. Ensure the **TFT_eSPI** library is installed:
   - In `User_Setup_Select.h` of the `TFT_eSPI` library, make sure `#include <User_Setups/Setup25_TTGO_T_Display.h>` is uncommented (or use the repository's pre-configured setup).
4. Select the serial COM port for your board and upload `Relais_control.ino`.

### 2. Connecting via Wi-Fi Soft-AP
1. Power up the board. The display will show the Soft-AP info:
   - **SSID**: `Relais-Control-AP`
   - **Default Password**: `12345678`
   - **Default IP**: `192.168.4.1`
2. Connect your smartphone, tablet, or laptop to the `Relais-Control-AP` Wi-Fi network.
3. Open your browser and navigate to:
   ```text
   http://192.168.4.1/
   ```
4. The dashboard allows you to:
   - Toggle individual relays with animated switches.
   - Click **ALL ON** or **ALL OFF** for bulk control.
   - View live state updates matching the onboard LCD.

### 3. On-Device Button & Touch Control
- **Cycle to next relay**: Press the **Upper / Right button** (GPIO 35) **OR** touch the wire connected to **GPIO 32**.
- **Toggle selected relay**: Press the **Lower / Left button** (GPIO 0) **OR** touch the wire connected to **GPIO 33**.

#### How Capacitive Touch Works on ESP32
Pins 32 and 33 connect to the ESP32 internal capacitive touch sensor peripheral (`TOUCH9` and `TOUCH8`).
- You can simply plug a jumper wire (solid or stranded) directly into pin 32 or 33.
- When untouched, the reading is typically between `60` and `95`.
- When your finger or hand touches the bare wire end (or even a metal foil pad / coin attached to it), your body's capacitance causes the reading to plummet to `10`–`25`.
- The firmware detects this drop below `TOUCH_THRESHOLD` (default: 35) with software debouncing.

---

## Customization

All configuration is located at the top of [`Relais_control.ino`](Relais_control.ino):

### Changing Relay Pins or Names
Edit the `relays[]` array:
```cpp
Relay relays[] = {
  { "Relais 1", 17, false },
  { "Relais 2",  2, false },
  { "Relais 3", 15, false },
  { "Relais 4", 13, false },
  { "Relais 5", 12, false }
};
```

### Inverting Relay Trigger Logic (Active-HIGH vs Active-LOW)
If your relay module requires a `HIGH` signal to turn ON:
```cpp
#define RELAY_ACTIVE_LOW false
```
For standard Arduino/Raspberry Pi 5V/3.3V opto-isolated relay modules (which trigger on `LOW`):
```cpp
#define RELAY_ACTIVE_LOW true
```

### Changing Soft-AP Name or Password
```cpp
#define AP_SSID  "Relais-Control-AP"
#define AP_PASS  "12345678"          // At least 8 characters, or "" for open network
```
