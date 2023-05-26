from machine import Pin, reset, PWM
import network
import socket
import time

#Disable debug output
import esp
esp.osdebug(None)

#It reclaims the memory occupied by objects that are not necessary for the program
import gc
gc.collect()

#WiFi Connection
#Replace the SSID and KEY data with those of your Wi-Fi network
ssid = 'iPhone de Jou'
key = 'jou12345'
indicator = Pin(0, Pin.OUT)
wlan = network.WLAN(network.STA_IF)
if not wlan.isconnected():
    wlan.active(True)
    wlan.connect(ssid, key)
    print('Connecting to: %s' % ssid)
    timeout = time.ticks_ms()
    while not wlan.isconnected():
        indicator.on()
        time.sleep(0.15)
        indicator.off()
        time.sleep(0.15)
        if (time.ticks_diff (time.ticks_ms(), timeout) > 10000):
            break
    if wlan.isconnected():
        indicator.on()
        print('Successful connection to: %s' % ssid)
        print('IP: %snSUBNET: %snGATEWAY: %snDNS: %s' % wlan.ifconfig()[0:4])
    else:
        indicator.off()
        wlan.active(False)
        print('Failed to connect to: %s' % ssid)
else:
    indicator.on()
    print('ConnectednIP: %snSUBNET: %snGATEWAY: %snDNS: %s' % wlan.ifconfig()[0:4])

serv1 = Pin(5, Pin.OUT)
serv2 = Pin(12, Pin.OUT)

servo1 = PWM(serv1, freq=50)
servo2 = PWM(serv2, freq=50)

switchIzq = Pin(4, Pin.IN)
switchCen = Pin(0, Pin.IN)
switchDer = Pin(2, Pin.IN)

switchStateIzq = 0
switchStateCen = 0
switchStateDer = 0

servo1.duty(26)
servo2.duty(26)

#Web Page
def web_page():
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
        <link rel=\"icon\" href=\"data:,\">
    </head>
    <body></body>
    </html>
    """
    return html

#Socket Configuration
try:
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(('', 80))
    tcp_socket.listen(5)
    time.sleep(1)
    print('Successful socket configuration\n')
except OSError as e:
    print('Failed to socket configuration. Rebooting...\n')
    time.sleep(3)
    reset()
print('Ready...!\n********************************\n')

while True:
    try:
        if gc.mem_free() < 102000:
            gc.collect()
        tcp_socket.settimeout(0.5)
        conn, addr = tcp_socket.accept()
        conn.settimeout(3.0)
        print('New connection from: %s' % str(addr[0]))
        request = conn.recv(1024)
        print("hola")
        conn.settimeout(None)
        print("hola2")
        request = str(request)
        print("hola3")
        #print('Request:  %s' % request)
        if request.find('/izq') == 6:
            print('OUTPUT1: izquierda')
            print("izq")
            servo1.duty(123)  # 77 corresponde a un ángulo de 180 grados en un servo SG90
            servo2.duty(26)
            time.sleep(0.5)
            
        if request.find('/cen') == 6:
            print('OUTPUT2: centro')
            print("centro")
            servo1.duty(26)  # 77 corresponde a un ángulo de 180 grados en un servo SG90
            servo2.duty(26)
            time.sleep(0.5)
            
        if request.find('/der') == 6:
            print('OUTPUT3: derecha')
            print("derecha")
            servo1.duty(26)  # 77 corresponde a un ángulo de 180 grados en un servo SG90
            servo2.duty(123)
            time.sleep(0.5)
            
        conn.send('HTTP/1.1 200 OKn')
        conn.send('Content-Type: text/htmln')
        conn.send('Connection: closenn')
        conn.sendall(web_page())
        conn.close()
    except OSError as e:
        try:
            conn.close()
        except:
            pass
    print("cerrada")
    time.sleep(0.1)
    
    switchStateIzq = switchIzq.value()
    switchStateCen = switchCen.value()
    switchStateDer = switchDer.value()
    
    if switchStateIzq == 1 and switchStateCen == 1:
        pass
    elif switchStateIzq == 1 and switchStateDer == 1:
        pass
    elif switchStateCen == 1 and switchStateDer == 1:
        pass
    else:
        if switchStateIzq == 1:
            print("izq")
            servo1.duty(123)  # 77 corresponde a un ángulo de 180 grados en un servo SG90
            servo2.duty(26)
            time.sleep(0.5)
            
        elif switchStateCen == 1:
            print("centro")
            servo1.duty(26)  # 77 corresponde a un ángulo de 180 grados en un servo SG90
            servo2.duty(26)
            time.sleep(0.5)
            
        elif switchStateDer == 1:
            print("derecha")
            servo1.duty(26)  # 77 corresponde a un ángulo de 180 grados en un servo SG90
            servo2.duty(123)
            time.sleep(0.5)
            
        else:
            pass