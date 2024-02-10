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
        for i in range(num_packets):
            while not self.server.send_packet(i + 1):
                print(f"Client: Acquittement négatif reçu pour le paquet {i + 1}. Retransmission...")
        print("Client: Tous les paquets envoyés avec succès.")

    def send_fin(self):
        print("Client: Envoi du paquet FIN pour fermer la connexion.")
        self.server.receive_fin()


class Server:
    def __init__(self):
        pass

    def receive_syn(self):
        print("Serveur: Réception du paquet SYN du client.")
        print("Serveur: Envoi du paquet SYN + ACK au client.")
        time.sleep(1)  # Simulate network delay
        print("Serveur: Paquet SYN + ACK envoyé.")

    def send_packet(self, packet_num):
        print(f"Serveur: Envoi du paquet {packet_num}.")
        time.sleep(1)  # Simulate network delay
        ack = True
        return ack  # Simulated positive acknowledgment

    def receive_fin(self):
        print("Serveur: Réception du paquet FIN du client.")
        print("Serveur: Acquittement du paquet FIN avec un paquet en cours de fermeture.")
        time.sleep(1)  # Simulate network delay
        print("Serveur: Paquet en cours de fermeture envoyé.")


# Simulation
server = Server()
client = Client(server)

client.connect()
client.request_data(5, 10)
client.send_fin()
