import socket

# Configuración del servidor ESP32
ESP32_IP = '192.168.100.108'  # Reemplaza con la IP de tu ESP32 en la red local, verifica con nmap o revisa la salida en la consola de thonny
ESP32_PORT = 80  # Puerto del servidor HTTP en la ESP32, verifica con nmap o revisa la salida en la consola de thonny

def enviar_comando(comando):
    """Envía un comando al servidor HTTP de la ESP32."""
    try:
        # Crear un socket TCP/IP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Conectar con el servidor ESP32
        s.connect((ESP32_IP, ESP32_PORT))
        
        # Crear una solicitud HTTP GET para el comando
        http_request = f"GET /{comando} HTTP/1.1\r\nHost: {ESP32_IP}\r\n\r\n"
        
        # Enviar la solicitud HTTP
        s.sendall(http_request.encode())
        print('Comando ', comando,'  enviado!')
        
        # Recibir la respuesta del servidor
        response = s.recv(1024)
        print('Respuesta del servidor:', response.decode())
        
    except Exception as e:
        print(f'Error al enviar el comando: {e}')
    
    finally:
        # Cerrar el socket
        s.close()

if __name__ == "__main__":
    while True:
        comando = input("Ingrese el comando: ")
        enviar_comando(comando)
            
        
