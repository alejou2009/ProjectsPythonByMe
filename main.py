#print("hola mundo")
#import pycom
#pycom.heartbeat(False)
#pycom.rgbled(0x00FFFF)
import time
import pycom # Para manejar el led
#import network
from network import LoRa # Para instanciar el radio LoRaWAN
import usocket # Para enviar datos por el radio LoRa
import uos # Para generar valores aleatorios
import ubinascii # Para hacer cast
import ustruct

class lora_endnode:
    def __init__(self):
        # Configurar el radio LoRaWAN de acuerdo con los parámetros de la región
        print("[INFO] Configuring radio...")
        self.radio = LoRa(mode = LoRa.LORAWAN) # Con este modo podemos conectarnos a un GW y enviar los datos a activation
        self.radio.init(mode = LoRa.LORAWAN, # Configuracion del radio
                        region = LoRa.US915, # Estoy configurando el radio para el plan de frecuencias de Colombia
                        tx_power = 10, # Puede ir de 0 dBm hasta 20 dBm, 30-2*tx_power
                        bandwidth = LoRa.BW_125KHZ, # Voy a trabajar con un ancho de banda de 125kHz
                        sf = 7, # Numero de bits por simbolo (puede ir entre 7 y 12, en Colombia se permiten 10)
                        preamble = 8, # Numero de secuencias de subida para enganchar el receptor
                        coding_rate = LoRa.CODING_4_8, # 4/5, 4/6, 4/7 y 4/8
                        adr = False # Adaptative Data Rate (Realizar control de transmision de potencia)
                        )
        for i in range(0,8): # Voy a eliminar las transmisiones por las sub bandas 1-7
            self.radio.remove_channel(i)
        for i in range(16,64):
            self.radio.remove_channel(i)
        print("[INFO] Radio configured!")

    def join_network(self):
        """
        device address 260C23FF
        appskey DBA1BF6BAC7EDC982179FD3C0E6E79D3
        nskey 0D25881D4343CA1B70AF399387225DAA
        """
        dev_eui = "ABCD1234" # En string
        dev_eui = ubinascii.unhexlify(dev_eui) # En bytes
        dev_address = "260C23FF"
        dev_address = ustruct.unpack(">l", ubinascii.unhexlify(dev_address))[0] # Castear el string a long
        app_swkey = "DBA1BF6BAC7EDC982179FD3C0E6E79D3"
        nwk_swkey = "0D25881D4343CA1B70AF399387225DAA"

        app_swkey = ubinascii.unhexlify(app_swkey)
        nwk_swkey = ubinascii.unhexlify(nwk_swkey)

        print("[INFO] Joining network...")
        self.radio.join(activation = LoRa.ABP, auth = (dev_address,
                                                       nwk_swkey,
                                                       app_swkey))
        print("[INFO] End node joined the network!")
        self.socket = usocket.socket(usocket.AF_LORA, usocket.SOCK_RAW)
        # El socket es para LoRa y vamos a enviar los datos crudos
        self.socket.setsockopt(usocket.SOL_LORA, usocket.SO_DR, 2)
        # 10 = 0
        # 9 = 1
        # 8 = 2
        # 7 = 3
        print("[INFO] Socket created!")

    def send_data(self, value):
        print("[INFO] Sending data...")
        print("[INFO] Value: {}".format(value))
        self.socket.setblocking(True)
        self.socket.send(value)
        self.socket.setblocking(False)
        print("[INFO] Data sent!")

if __name__ == "__main__":
    pycom.heartbeat(True)
    end_node = lora_endnode()
    end_node.join_network()

    while True:
        value = ustruct.unpack(">B",uos.urandom(1))[0]
        end_node.send_data(bytes([value]))
        print("data sent...")
        time.sleep(5)
        pass
