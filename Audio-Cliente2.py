import socket
import time

host ="localhost"
port = 5000
buffer_size=40960
# Creamos un socket para el cliente y establecemos conexion con el servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

#Ubicamos el archivo
filesong = 'navi-hey-look.wav'
# Abrimos el archivo
with open(filesong, 'rb') as FileToSend:
    while True:
        data = FileToSend.read(buffer_size)
        if not data:
            break
        try:
            # Enviar datos al servidor
            client.sendall(data)
            time.sleep(0.01)  # Pausa para evitar saturación del socket
        except socket.error:
            pass  # Ignorar errores de no bloqueo

print("Archivo enviado con éxito")

# Cerrar el socket del cliente
client.close()
