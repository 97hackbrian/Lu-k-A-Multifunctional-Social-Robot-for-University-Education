import network
import socket
from machine import Pin, PWM

class MotorSeeker:
    def __init__(self,RPWMA, LPWMA, RENA,LENA, RPWMB, LPWMB, LENB,RENB):
        self.Max = 1023  # Valor máximo de PWM en ESP32
        
        # Inicializa los pines como salida y PWM
        self.RPWMA = PWM(Pin(RPWMA), freq=1000)
        self.LPWMA = PWM(Pin(LPWMA), freq=1000)
        self.RENA = Pin(RENA, Pin.OUT)
        self.LENA = Pin(LENA, Pin.OUT)
        
        self.RPWMB = PWM(Pin(RPWMB), freq=1000)
        self.LPWMB = PWM(Pin(LPWMB), freq=1000)
        self.RENB = Pin(RENB, Pin.OUT)
        self.LENB = Pin(LENB, Pin.OUT)
        
        
        # Inicialmente los motores están apagados
        self.stop()

    def stop(self):
        # Detiene todos los motores
        self.RPWMA.duty(0)
        self.LPWMA.duty(0)
        self.RPWMB.duty(0)
        self.LPWMB.duty(0)
        self.RENA.off()
        self.LENA.off()
        self.RENB.off()
        self.LENB.off()

    def move(self, Velleft, Velright):
        # Mapea de -100 a 100 al rango 0 a 1023
        def map_speed(value):
            return int((value + 100) * (self.Max / 200))  # Mapea de -100/100 a 0/1023
        
        # Configura velocidad para el motor izquierdo
        if Velleft < 0:
            self.RPWMA.duty(0)
            self.LPWMA.duty(map_speed(Velleft))
            self.RENA.on()
            self.LENA.on()
            
        else:
            self.RPWMA.duty(map_speed(Velleft))
            self.LPWMA.duty(0)
            self.RENA.on()
            self.LENA.on()

        # Configura velocidad para el motor derecho
        if Velright < 0:
            self.RPWMB.duty(0)
            self.LPWMB.duty(map_speed(Velright))
            self.RENB.on()
            self.LENB.on()
        else:
            self.RPWMB.duty(map_speed(Velright))
            self.LPWMB.duty(0)
            self.RENB.on()
            self.LENB.on()

        # Si ambos motores están en 0, apaga los pines de enable
        if Velleft == 0 and Velright == 0:
            self.RENA.off()
            self.LENA.off()
            self.RENB.off()
            self.LENA.off()
        else:
            self.RENA.on()
            self.LENA.on()
            self.RENB.on()
            self.LENA.on()


# Pines del ESP32 para los motores
RPWMA = 25
LPWMA = 33
RENA = 32
LENA = 13#cambiar antes 35


RPWMB = 14
LPWMB = 12
RENB = 26
LENB = 27





motores = MotorSeeker(RPWMA, LPWMA, RENA,LENA, RPWMB, LPWMB, LENB,RENB)
while True:
    motores.move(100,100)