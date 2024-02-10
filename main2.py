# Client se connecte au serveur
# Le serveur envoie des données au client
# Le client ACK les données
# Le serveur envoie un paquet FIN
# Le client ferme la connexion

import time


bytesReceived = 0
def is_timeout_exceed(startT):
    timeout = 10
    duration = time.time()-startT
    return duration > timeout

def client_connect():
    print("CLIENT: Envoi SYN au serveur")
    startT = time.time()
    SYNACK = server_receive_syn()
    while (not SYNACK) and (not is_timeout_exceed(startT)):
        SYNACK = server_receive_syn()
    if is_timeout_exceed(startT):
        print("CLIENT: Impossible de se connecter au serveur (TimeOut)")
        return False
    print("CLIENT: Connexion résussie au serveur")
    server_request_data(60)
    return True



def client_receive_data(seqNum, data):
    global bytesReceived
    print(f"CLIENT: Reception de la sequence {seqNum} contenant {data}o")
    bytesReceived += data
    time.sleep(1)
    print(f"CLIENT: {bytesReceived}o reçus")
    return {'seqNum': seqNum+data, 'rcvwindow': 60}

def client_receive_fin():
    print("CLIENT: Reception du paquet FIN. Connexion fermée.")
    return

def client_send_ack(seqNum, rcvwindow, scalingFactor):
    pass



bytesToSend = 342
def server_receive_syn():
    time.sleep(1)
    print("SERVEUR: Envoi du paquet SYN+ACK")
    return True

def server_request_data(rcvwindow):
    server_send_packet(0, rcvwindow)


def server_send_packet(seqNum, packetMaxSize):
    global bytesToSend
    if(packetMaxSize<bytesToSend):
        print(f"SERVEUR: Sequence {seqNum}, envoi d'un paquet de taille {packetMaxSize}o")
        ACK = client_receive_data(seqNum, packetMaxSize)
        while ACK['seqNum'] == seqNum:
            ACK = client_receive_data(seqNum, packetMaxSize)
        bytesToSend -= packetMaxSize
        print(f"SERVEUR: Reste {bytesToSend}o à envoyer")
        server_send_packet(ACK['seqNum'],ACK['rcvwindow'])
    else:
        print(f"SERVEUR: Sequence {seqNum}, envoi d'un paquet de taille {packetMaxSize}o")
        ACK = client_receive_data(seqNum, bytesToSend)
        while ACK['seqNum'] == seqNum:
            ACK = client_receive_data(seqNum, bytesToSend)
        bytesToSend = 0
        print(f"SERVEUR: Reste {bytesToSend}o à envoyer")
        server_send_fin()


def server_send_fin():
    print(f"SERVEUR: Envoi du paquet FIN. Fermeture de la connexion.")
    client_receive_fin()
    return


client_connect()
