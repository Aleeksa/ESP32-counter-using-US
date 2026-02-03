# IoT Brojač Objekata sa Web Interfejsom (ESP32 & MicroPython)

Ovaj projekat predstavlja pametni sistem za detekciju i brojanje prolazaka objekata koristeći **ESP32** mikrokontroler i ultrazvučni senzor. Sistem podržava lokalno praćenje putem LCD ekrana i daljinsko praćenje putem Web browsera.

## 🚀 Funkcionalnosti
- **Precizna detekcija:** Koristi ultrazvučni senzor (HC-SR04) za merenje udaljenosti.
- **Lokalni prikaz:** LCD 16x2 (I2C) prikazuje trenutnu udaljenost i ukupan broj prolazaka.
- **Zvučna i svetlosna signalizacija:** Aktiviranje LED diode i zujalice (buzzer) pri svakoj uspešnoj detekciji.
- **Web Server:** Hostuje stranicu na lokalnoj mreži koja uživo (AJAX) prikazuje broj prolazaka.
- **Mogućnost resetovanja:** Fizičko dugme na uređaju ili "Restart" dugme na Web stranici vraćaju brojač na nulu.
- **Multi-threading:** Web server radi u posebnom thread-u kako ne bi blokirao rad senzora.

## 🛠 Hardver
- ESP32 Development Board
- Ultrazvučni senzor (HC-SR04)
- LCD Displej 16x2 sa I2C adapterom
- LED dioda i Zujalica (Buzzer)
- Taster (Dugme) za reset



## 📋 Šema povezivanja (Pins)
| Komponenta | ESP32 Pin |
|---|---|
| Trig (Senzor) | GPIO 5 |
| Echo (Senzor) | GPIO 18 |
| SCL (LCD) | GPIO 22 |
| SDA (LCD) | GPIO 21 |
| Reset Dugme | GPIO 4 |
| Crvena LED | GPIO 2 |
| Zujalica | GPIO 15 |

## 💻 Kako podesiti projekat
1. Flešujte **MicroPython** firmware na vaš ESP32.
2. Otvorite kod i u promenljive `SSID` i `PASSWORD` unesite podatke vaše Wi-Fi mreže.
3. Prebacite fajlove na ESP32 (koristeći Thonny IDE ili sličan alat).
4. Nakon pokretanja, u terminalu će se ispisati **IP adresa**. Unesite tu adresu u vaš browser da biste pristupili Web kontrolnoj tabli.

## ⚙️ Logika rada (Software)
- **Detekcija pravca:** Kod prati promenu udaljenosti; objekat se broji samo ako se kreće u određenom smeru (od leve ka desnoj strani senzora).
- **Anti-spam (Delay):** Postoji `DETECTION_DELAY` od 45 sekundi (podesivo) kako bi se sprečilo višestruko brojanje istog objekta koji stoji ispred senzora.
- **Web Refresh:** JavaScript unutar HTML-a koristi `XMLHttpRequest` da bi svake sekunde osvežio broj bez ponovnog učitavanja cele stranice.

---
**Autor:** Aleksa Antić

**Tehnologije:** MicroPython, HTML/CSS, JavaScript (AJAX), IoT
