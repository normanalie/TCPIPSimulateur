import time

class Client:
    def __init__(self, server):
        self.server = server
        self.timeout = 10

    def connect(self):
        print("Client: Envoi du paquet SYN au serveur.")
        self.server.receive_syn()

    def request_data(self, num_packets, rcvwindow):
        print(f"Client: Demande de {num_packets} paquets avec une fenêtre de réception de {rcvwindow}.")
        self.server.send_data(self, num_packets, rcvwindow)

    def receive_ack(self, positive):
        if positive:
            print("Client: Acquittement positif reçu.")
        else:
            print("Client: Acquittement négatif reçu.")

    def send_fin(self):
        print("Client: Envoi du paquet FIN pour fermer la connexion.")
        self.server.receive_fin(self)


class Server:
    def __init__(self):
        pass

    def receive_syn(self):
        print("Serveur: Réception du paquet SYN du client.")
        print("Serveur: Envoi du paquet SYN + ACK au client.")
        time.sleep(1)  # Simulate network delay
        print("Serveur: Paquet SYN + ACK envoyé.")

    def send_data(self, client, num_packets, rcvwindow):
        print(f"Serveur: Envoi de {num_packets} paquets avec une fenêtre de réception de {rcvwindow}.")
        time.sleep(1)  # Simulate network delay
        print("Serveur: Paquets envoyés.")
        positive_ack = True  # Simulated positive acknowledgment
        client.receive_ack(positive_ack)

    def receive_fin(self, client):
        print("Serveur: Réception du paquet FIN du client.")
        print("Serveur: Acquittement du paquet FIN avec un paquet en cours de fermeture.")
        time.sleep(1)  # Simulate network delay
        print("Serveur: Paquet en cours de fermeture envoyé.")
        client.receive_ack(True)


# Simulation
server = Server()
client = Client(server)

client.connect()
client.request_data(5, 10)
client.send_fin()
