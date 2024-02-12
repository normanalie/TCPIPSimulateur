from tkinter import *
from PIL import Image, ImageTk
import time

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.geometry("680x1000")
        self.master.title("TCP/IP Simulateur")

        self.imgSize = (40, 40)

        self.frameComputer = LabelFrame(master, text="Computer", padx=20, pady=20)
        self.frameServer = LabelFrame(master, text="Server", padx=20, pady=20)

        self.cumulativedelay = 0

        self.load_images()
        self.setup_ui()

    def load_images(self):
        self.imgComputer = self.resize_image("computer.png", self.imgSize)
        self.imgServer = self.resize_image("server.png", self.imgSize)

    def resize_image(self, image_path, img_size):
        original_image = Image.open(image_path)
        resized_image = original_image.resize(img_size)
        return ImageTk.PhotoImage(resized_image)

    def setup_ui(self):
        self.frameComputer.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.frameServer.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.labelComputer = Label(self.frameComputer, image=self.imgComputer)
        self.labelComputer.pack()

        self.labelServer = Label(self.frameServer, image=self.imgServer)
        self.labelServer.pack()

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.rowconfigure(0, weight=1)

    def write_to_computer(self, text):
        Label(self.frameComputer, text=text).pack(fill="both")
        Label(self.frameServer, text=" ").pack(fill="both")

    def write_to_server(self, text):
        Label(self.frameServer, text=text).pack(fill="both")
        Label(self.frameComputer, text=" ").pack(fill="both")

    def write_delayed(self, destination, text, cumulativedelay=0):
        self.cumulativedelay += cumulativedelay
        if destination=="computer":
            self.master.after(self.cumulativedelay, self.write_to_computer, text)
        elif destination=="server":
            self.master.after(self.cumulativedelay, self.write_to_server, text)

def main():
    root = Tk()
    app = MainWindow(root)
    app.write_delayed("computer", "Envoi SYN", 0)
    app.write_delayed("server", "Envoi SYN+ACK", 1000)
    app.write_delayed("computer", "Connexion réussie au serveur", 1000)
    app.write_delayed("computer", "Envoi ACK=0, N=10, rcvwindow=1000o", 0)
    app.write_delayed("server", "Le serveur doit envoyer 10 paquets de 100o chacun", 1000)
    app.write_delayed("server", "Envoi SEQ=1, size(data)=100o", 0)
    app.write_delayed("server", "Envoi SEQ=101, size(data)=100o", 100)
    app.write_delayed("server", "Envoi SEQ=201, size(data)=100o", 100)
    app.write_delayed("server", "Envoi SEQ=301, size(data)=100o", 100)
    app.write_delayed("server", "Envoi SEQ=401, size(data)=100o", 100)
    app.write_delayed("server", "Envoi SEQ=1001, size(data)=100o", 100)
    app.write_delayed("server", "Envoi SEQ=601, size(data)=100o", 100)
    app.write_delayed("server", "Envoi SEQ=701, size(data)=100o", 100)
    app.write_delayed("server", "Envoi SEQ=801, size(data)=100o", 100)
    app.write_delayed("server", "Envoi SEQ=901, size(data)=100o", 100)
    app.write_delayed("computer", "Recu 100o de données SEQ=1", 1000)
    app.write_delayed("computer", "Recu 100o de données SEQ=101", 100)
    app.write_delayed("computer", "Recu 100o de données SEQ=201", 100)
    app.write_delayed("computer", "Recu 100o de données SEQ=301", 100)
    app.write_delayed("computer", "Recu 100o de données SEQ=401", 100)
    app.write_delayed("computer", "Recu 100o de données SEQ=501", 100)
    app.write_delayed("computer", "Recu 100o de données SEQ=601", 100)
    app.write_delayed("computer", "Recu 100o de données SEQ=801", 100)
    app.write_delayed("computer", "Envoi ACK=901, N=1, rcvwindow=100o", 1000)
    app.write_delayed("server", "Envoi SEQ=901, size(data)=100o", 1000)
    app.write_delayed("computer", "Recu 100o de données SEQ=901", 1000)
    app.write_delayed("computer", "Envoi ACK=1001, N=0, rcvwindow=1000o", 0)
    app.write_delayed("computer", "Envoi FIN", 100)
    app.write_delayed("server", "Envoi ACK", 1000)
    app.write_delayed("server", "Envoi FIN", 1000)
    app.write_delayed("computer", "Envoi ACK", 1000)
    app.write_delayed("computer", "Wait 30sec before close", 0)
    app.write_delayed("server", "Connection closed", 1000)
    app.write_delayed("computer", "Connection closed", 30000)

    root.mainloop()

if __name__ == "__main__":
    main()
