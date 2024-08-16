from machine import Pin, I2C
import time
from i2c_lcd import I2cLcd
import network
import socket

# Inicijalizacija I2C-a
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)

# I2C adresa LCD-a, broj kolona i redova
I2C_ADDR = 0x27
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# Inicijalizacija ultrazvučnog senzora
trig = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)

# Promenljive
distance_threshold = 300  # Prag za detekciju u cm
object_count = 0  # Brojač objekata
previous_state = False  # Prethodno stanje detekcije objekta
previous_distance = None  # Prethodna izmerena udaljenost
last_detection_time = 0  # Vreme poslednje detekcije
DETECTION_DELAY = 1  # 60 sekundi u milisekundama

# Inicijalizacija dugmeta za resetovanje
reset_button = Pin(4, Pin.IN, Pin.PULL_UP)

def measure_distance():
    trig.off()
    time.sleep_us(2)
    trig.on()
    time.sleep_us(10)
    trig.off()
    
    while echo.value() == 0:
        pulse_start = time.ticks_us()
    
    while echo.value() == 1:
        pulse_end = time.ticks_us()
    
    pulse_duration = time.ticks_diff(pulse_end, pulse_start)
    distance = (pulse_duration * 0.0343) / 2
    return distance

def update_display(distance, count):
    lcd.clear()  # Očisti ekran
    lcd.putstr("PROSAO\n")
    lcd.putstr(str(round(distance, 2)))
    lcd.move_to(0, 1)
    lcd.putstr("PUTA: " + str(count))

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    while not wlan.isconnected():
        pass

    print("Connected to Wi-Fi")
    print("IP address:", wlan.ifconfig()[0])
    
    return wlan.ifconfig()[0]

# Podesite vašu Wi-Fi mrežu ovde
SSID = 'OrionTelekom_EAAA-2.4G'
PASSWORD = 'HWTCC921EAAA'

ip_address = connect_wifi(SSID, PASSWORD)

def web_page(object_count):
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Object Counter</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            color: #333;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }}
        .container {{
            text-align: center;
            background: #fff;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }}
        h1 {{
            font-size: 2.5em;
            margin: 0;
        }}
        p {{
            font-size: 1.5em;
            margin: 10px 0 0;
        }}
    </style>
    <script>
        function refreshCount() {{
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/count', true);
            xhr.onreadystatechange = function() {{
                if (xhr.readyState == 4 && xhr.status == 200) {{
                    document.getElementById('count').innerText = xhr.responseText;
                }}
            }};
            xhr.send();
        }}
        setInterval(refreshCount, 1000);
    </script>
</head>
<body>
    <div class="container">
        <h1>Object Counter</h1>
        <p>Koliko je puta prosla ruka:</p>
        <p id="count">{object_count}</p>
    </div>
</body>
</html>"""
    return html

def start_web_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    
    print("Web server started")
    
    while True:
        conn, addr = s.accept()
        print("Got a connection from", str(addr))
        request = conn.recv(1024)
        request = str(request)
        
        if 'GET /count' in request:
            response = f"{object_count}"
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/plain\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
        else:
            response = web_page(object_count)
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
        
        conn.close()

# Pokretanje web servera u drugom threadu
import _thread
_thread.start_new_thread(start_web_server, ())

while True:
    # Merenje distance
    distance = measure_distance()
    current_time = time.ticks_ms()
    
    if distance < distance_threshold:
        current_state = True
        direction = previous_distance - distance if previous_distance is not None else 0
    else:
        current_state = False
        direction = 0

    # Ako je objekat detektovan (prešao prag) i prethodno nije bio detektovan, i kretanje je u pravcu od leve ka desnoj
    if current_state and not previous_state and direction > 0:
        if time.ticks_diff(current_time, last_detection_time) > DETECTION_DELAY:
            object_count += 1  # Povećaj brojač
            update_display(distance, object_count)  # Ažuriraj prikaz
            last_detection_time = current_time  # Ažuriraj vreme poslednje detekcije

    previous_state = current_state  # Ažuriraj prethodno stanje
    previous_distance = distance  # Ažuriraj prethodnu udaljenost

    # Provera da li je pritisnuto dugme za resetovanje
    if reset_button.value() == 0:
        object_count = 0  # Resetuj brojač
        update_display(distance, object_count)  # Ažuriraj prikaz
        time.sleep(0.5)  # Debouncing - čekanje da se dugme otpusti

    # Kratko odlaganje
    time.sleep(1)

