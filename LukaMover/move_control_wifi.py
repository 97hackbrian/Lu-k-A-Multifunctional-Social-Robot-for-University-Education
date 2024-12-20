import network
import socket
from machine import Pin, PWM



class MotorSeeker:
    def __init__(self,RPWMA, LPWMA, RENA,LENA, RPWMB, LPWMB, LENB,RENB):
        self.Max = 1023  # Valor máximo de PWM en ESP32
        
        # Inicializa los pines como salida y PWM
        self.RPWMA = PWM(Pin(RPWMA), freq=10000)
        self.LPWMA = PWM(Pin(LPWMA), freq=10000)
        self.RENA = Pin(RENA, Pin.OUT)
        self.LENA = Pin(LENA, Pin.OUT)
        
        self.RPWMB = PWM(Pin(RPWMB), freq=10000)
        self.LPWMB = PWM(Pin(LPWMB), freq=10000)
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

    def move(self, Velright, Velleft):
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
RENA = 32#puenteado con el de abajo
LENA = 13#cambiar antes 35


RPWMB = 14
LPWMB = 12
RENB = 26
LENB = 27





motores = MotorSeeker(RPWMA, LPWMA, RENA,LENA, RPWMB, LPWMB, LENB,RENB)


# Configuración del LED (opcional)
led = Pin(4, Pin.OUT)

# Conectar a la red Wi-Fi
ssid = 'luka'
password = '123456789'
wlan = None

def conectar_wifi():
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        print('Error de conexión, intentando conectar...')
        pass

    print('Conexión Wi-Fi establecida a', ssid, ', IP:', wlan.ifconfig()[0])

# Servidor HTTP simple
# Servidor HTTP simple
def iniciar_servidor():
    global wlan
    addr = socket.getaddrinfo(wlan.ifconfig()[0], 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Escuchando en', addr, '. Listo para recibir comandos...')

    while True:
        cl, addr = s.accept()
        print('Cliente conectado desde', addr)
        request = cl.recv(1024)
        request = str(request)
        print('Solicitud completa: ', request)

        # Filtra la solicitud para eliminar encabezados HTTP
        command = request.split(' ')[1].lstrip('/')
        print('Comando recibido: ', command)

        if 'move' in command:
            try:
                # Parsear el comando correctamente
                parts = command.split(',')
                vel_left = int(parts[1])
                vel_right = int(parts[2])
                motores.move(vel_left, vel_right)
                respuesta = f'Moviendo motores: izquierda {vel_left}, derecha {vel_right}'
            except Exception as e:
                print(f"Error procesando el comando: {e}")
                respuesta = 'Error en el comando. Usa move,<vel_izquierda>,<vel_derecha>'
        
        elif 'stop' in command:
            motores.stop()
            respuesta = 'Motores detenidos.'

        else:
            respuesta = 'Comando desconocido.'

        print('Respuesta: ', respuesta)
        cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
        cl.send(respuesta)
        cl.close()


# Conectar a Wi-Fi e iniciar el servidor
conectar_wifi()
iniciar_servidor()
