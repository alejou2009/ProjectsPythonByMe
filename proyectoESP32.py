# CSV
# timestamp, battery\n\r
# 2022-09-22 8:34:15, 100 \n\r
# ... Se incluirian las demas lineas
# Se debe definir un tiempo de muestreo ( Cada cuanto se incluira una nueva linea)
# Para obtener el tiempo, se va a usar el modulo RTC (Real Time Clock)
# Para la asignacion debe usarse un RTC fisico (DS1302)

# Formato del data logger
# timestamp pluv ultras termo humedad

#Archivos: UltraSonTerminado2, Humedimetro2, thermocouple2 y pluviometer2

# imports base
import random
import time
import _thread
import gc

from machine import RTC
from machine import UART # Para descargar los datos en el PC
from machine import Pin
import ds1302

# Sensores -----------------------------------------

#Humedad
# adc 15
from Humedimetro2 import mauroSoltanos

#Ultrasonido
# e 25 y t 26
from UltraSonTerminado2 import mauroNoNosPegues

#Thermocouple
#sck_pin = 14, miso_pin = 12, cs_pin = 0, mosi_pin = 13
from thermocouple2 import thermocouple

#Pluviometer
#entrada = 4
from pluviometer2 import pluviometer

#---------------------------------------------------
# Para el initialTimeStamp = (year, month, day, weekday, hour, minute, sec, microsec)

#----------------
#Variables globales
porc = 0;
temp = 0;
lluvia = 0;
dist = 0;

class datalogger:
    def __init__(self, sampleTime = 5, filename = "datalogger.csv"):
        self.sampleTime = sampleTime
        self.filename = filename
        #self.rtc = RTC()
        #self.rtc.datetime(initialTimeStamp)
        
        self.ds = ds1302.DS1302(Pin(5),Pin(18),Pin(19))
        self.ds.date_time([2022, 10, 19, 3, 12, 45, 0, 0]) # set datetime.
        
        self.ds.start()
        
        self.enable = False # Para activar o desactivar el datalogger
        self.uart = UART(1, baudrate = 9600, tx = 33, rx = 32)
        
        # Abrir o crear el archivo
        try:
            with open(filename, "r") as f: # r: leer, w: escribir, a: append (adicionar)
                print("[INFO] file already exists!")
        except Exception as e:
            print("[INFO] Creating new file...")
            with open(filename, "w") as f:
                # Headers
                f.write("timestamp,pluviometer,ultrason,termocouple,humidity \n\r")
                print("[INFO] file created succesfully!")
        
    def log(self,lluvia, dist, temp, humed):
        if self.enable == True:
            #print("[INFO] logging...")
            
            # Registro de tiempo
            #now = self.rtc.datetime()
            now = self.ds.date_time()
            now = "{}-{}-{} {}:{}:{}".format(now[0], now[1], now[2], now[4], now[5], now[6])
            print("[INFO] Current timestamp: {}".format(now))
            
            # Fecha y valor de sensores
            newline = "{},{},{},{},{} \n\r".format(now,lluvia,dist,temp,humed)
            print(newline)
            
            # Anadir nueva linea
            with open(self.filename, "a") as f: # a hace append en el txt, no sobreescribe
                f.write(newline)
            #time.sleep(self.sampleTime)
                
    # Comunicacion con el PC
    def send_file(self):
        #characters = self.uart.any()
        #if characters != 0:
            #rcv_characters = self.uart.read()
            #print("[INFO] Received character: {}".format(rcv_characters))
            with open(self.filename,'r') as f:
                filecontents = f.read()
            self.uart.write(filecontents.encode("UTF-8"))
            valor = 'p'
            self.uart.write(valor.encode("UTF-8"))

#----------------
def sensar():
    gc.collect()
        
    # Sensor de humedad
    sensorH.__init__()
    sensorH.measure()
    volt = sensorH.valueV
    porc = sensorH.valueP
    #print("[INFO] Humedad en Voltios: {}".format(volt))
    print("[INFO] Humedad en %: {}".format(porc))
          
    # Sensor Ultrasonido
    sensorU.__init__()
    sensorU.calculate_distance();
    dist = sensorU.distance;
       
    # Sensor Temperatura
    sensorT.__init__();
    sensorT.measure();
    temp = sensorT.temperature;
    print("[INFO] Temperature: {} °C".format(temp))
        
    #Sensor de lluvia
    lluvia = sensorP.rain;
    print("[INFO] Rain = {} mm/5s".format(lluvia))
    
    datalogger.log(lluvia, dist, temp, porc);
    
if __name__ == "__main__":
    
    # Datalogger y habilitador
    datalogger = datalogger()
    datalogger.enable = True;

    #Humedad
    sensorH = mauroSoltanos();
    #Ultrasonido
    sensorU = mauroNoNosPegues();
    #Temperatura
    sensorT = thermocouple();
    #Pluviometer
    sensorP = pluviometer();
    
    while True:
        sensar();
        datalogger.send_file();
        
        print("----------------");
        print("----------------");
        print("----------------");
        
        time.sleep(10)
        
#def send_file(self):
#        while True:
#            characters = self.uart.any()
#            if characters != 0:
#                rcv_characters = self.uart.read()
#                print("[INFO] Received character: {}".format(rcv_character))
#                with open(self.filename,'r') as f:
#                    filecontents = f.read()
#                self.uart.write(filecontents.encode("UTF-8"))
        
