# Client se connecte au serveur
# Le serveur envoie des données au client
# Le client ACK les données
# Le serveur envoie un paquet FIN
# Le client ferme la connexion

import time

timeout = 10
bytesToSend = 342
rcvwindow = 60

def is_timeout_exceed(startT):
    global timeout
    duration = time.time()-startT
    return duration > timeout



bytesReceived = 0
def client_connect():
    global rcvwindow
    print("CLIENT: Envoi SYN au serveur")
    startT = time.time()
    SYNACK = server_receive_syn()
    # Connection not ACK
    while (not SYNACK) and (not is_timeout_exceed(startT)):
        SYNACK = server_receive_syn()
    print("CLIENT: Connexion résussie au serveur")
    server_request_data(rcvwindow)
    return True

def client_receive_data(seqNum, data):
    global bytesReceived, rcvwindow
    print(f"CLIENT: Reception de la sequence {seqNum} contenant {data}o")
    # If new data incoming
    if seqNum == bytesReceived:
        bytesReceived += data
    time.sleep(1) # Simulate network delay
    print(f"CLIENT: {bytesReceived}o reçus")
    return {'type': 'ACK', 'seqNum': bytesReceived, 'rcvwindow': rcvwindow}

def client_receive_fin():
    print("CLIENT: Reception du paquet FIN. Connexion fermée.")
    return




def server_receive_syn():
    time.sleep(1) # Simulate netword delay
    print("SERVEUR: Envoi du paquet SYN+ACK")
    return True

def server_request_data(rcvwindow):
    server_send_packet(0, rcvwindow)


def server_send_packet(seqNum, packetMaxSize):
    global bytesToSend
    packetSize = packetMaxSize if packetMaxSize<bytesToSend else bytesToSend

    print(f"SERVEUR: Sequence {seqNum}, envoi d'un paquet de taille {packetSize}o")
    startT = time.time()
    ACK = client_receive_data(seqNum, packetSize)
    # If packet not received
    while ACK['type'] != 'ACK' or ACK['seqNum'] == seqNum or is_timeout_exceed(startT):
        startT = time.time()
        ACK = client_receive_data(seqNum, packetSize)
    # Packet received
    bytesToSend -= packetSize
    print(f"SERVEUR: Reste {bytesToSend}o à envoyer")
    # End of transmission
    if(bytesToSend>0):
        server_send_packet(ACK['seqNum'],ACK['rcvwindow'])
    else:
        server_send_fin()


def server_send_fin():
    print(f"SERVEUR: Envoi du paquet FIN. Fermeture de la connexion.")
    client_receive_fin()
    return


client_connect()
