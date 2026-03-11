# IoT Object Counter with Web Interface (ESP32 & MicroPython)

This project is a smart system for detecting and counting passing objects using an **ESP32** microcontroller and an ultrasonic sensor. The system supports local monitoring via an LCD screen and remote tracking through a web browser.

## 🚀 Features
- **Precise Detection:** Uses the HC-SR04 ultrasonic sensor for distance measurement.
- **Local Display:** 16x2 LCD (I2C) shows the current distance and total count.
- **Audio & Visual Signaling:** Activates an LED and a buzzer upon every successful detection.
- **Web Server:** Hosts a page on the local network that displays a live (AJAX) counter.
- **Reset Capability:** A physical button on the device or a "Restart" button on the Web page resets the counter to zero.
- **Multi-threading:** The Web server runs in a separate thread so it doesn't block the sensor's real-time performance.

## 🛠 Hardware
- ESP32 Development Board
- Ultrasonic Sensor (HC-SR04)
- 16x2 LCD Display with I2C Adapter
- LED and Buzzer
- Push Button (for manual reset)



## 📋 Wiring Diagram (Pinout)
| Component | ESP32 Pin |
|---|---|
| Trig (Sensor) | GPIO 5 |
| Echo (Sensor) | GPIO 18 |
| SCL (LCD) | GPIO 22 |
| SDA (LCD) | GPIO 21 |
| Reset Button | GPIO 4 |
| Red LED | GPIO 2 |
| Buzzer | GPIO 15 |



[Image of ESP32 pinout diagram]


## 💻 Setup Instructions
1. Flash the **MicroPython** firmware onto your ESP32.
2. Open the code and enter your Wi-Fi credentials in the `SSID` and `PASSWORD` variables.
3. Upload the files to the ESP32 (using Thonny IDE or a similar tool).
4. After startup, the **IP address** will be displayed in the terminal. Enter that address into your browser to access the Web Dashboard.

## ⚙️ Software Logic
- **Directional Detection:** The code monitors distance changes; objects are only counted if they move in a specific pattern/direction.
- **Anti-spam (Delay):** A configurable `DETECTION_DELAY` (e.g., 45 seconds) is implemented to prevent multiple counts of an object remaining stationary in front of the sensor.
- **Web Refresh:** JavaScript within the HTML uses `XMLHttpRequest` to refresh the count every second without reloading the entire page.

---
**Author:** Aleksa Antić  
**Technologies:** MicroPython, HTML/CSS, JavaScript (AJAX), IoT
