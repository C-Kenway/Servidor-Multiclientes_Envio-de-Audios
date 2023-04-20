import socket
import selectors

host = "localhost"
port = 5000;
# Definimos el tamaño del búfer para la transferencia
buffer_size=40960
# Creamos un nuevo selector | Se utiliza para registrar y monitorear eventos en los sockets
Selector = selectors.DefaultSelector()

#(read) Es la función de callback que se ejecutará cuando haya datos disponibles para leer en un socket
def read(conn):
    data = conn.recv(buffer_size)
    if data:
        #Obtenemos el puerto de la conexion entrante
        Cli_Port = conn.getpeername()[1]
        # Nombramos el archivo con su puerto
        NewFile = f'Audiox{Cli_Port}.wav'
        # Guardar los datos en el archivo
        with open(NewFile, 'ab') as Editorfile:
            Editorfile.write(data)
        print(f"{len(data)} bytes obtenidds y guardados en {NewFile}")
    else:
        print("Cliente desconectado")
        Selector.unregister(conn)
        conn.close()

#(accept) Se ejecutará cuando se acepte una nueva conexión entrante:
def accept(sock):
    conn, addr = sock.accept()
    print(f"Conexión aceptada desde {addr}")
    conn.setblocking(False)
    Selector.register(conn, selectors.EVENT_READ, read)

# Crear el socket del servidor y configurarlo
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(5)
print(f"Servidor escuchando en {port}")
#Configurado como no bloqueante
sock.setblocking(False)
"""
Registrar el socket del servidor con el objeto Selector, 
especificando que el evento a monitorear es selectors.EVENT_READ,
y que la función de callback es accept:
"""
Selector.register(sock, selectors.EVENT_READ, accept)

# Bucle principal del servidor
while True:
    events = Selector.select()
    for key, _ in events:
        callback = key.data
        callback(key.fileobj)