from tkinter import *
from PIL import Image, ImageTk
import random
import math

class ScrollableFrame(Frame):
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, **kwargs)

        self.canvas = Canvas(self)
        scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.geometry("680x800")  # Adjusted height
        self.master.title("TCP/IP Simulateur")

        self.imgSize = (40, 40)

        self.scrollable_frame = ScrollableFrame(master)
        self.scrollable_frame.pack(fill="both", expand=True)

        self.frameComputer = LabelFrame(self.scrollable_frame.scrollable_frame, text="Computer", padx=20, pady=20)
        self.frameServer = LabelFrame(self.scrollable_frame.scrollable_frame, text="Server", padx=20, pady=20)

        self.cumulativedelay = 0

        self.load_images()
        self.setup_ui()

    def load_images(self):
        self.imgComputer = self.resize_image("computer.png", self.imgSize)
        self.imgServer = self.resize_image("server.png", self.imgSize)

    def setup_ui(self):
        self.frameComputer.grid(row=0, column=0, padx=10, pady=10)
        self.frameServer.grid(row=0, column=1, padx=10, pady=10)

        self.labelComputer = Label(self.frameComputer, image=self.imgComputer)
        self.labelComputer.pack()

        self.labelServer = Label(self.frameServer, image=self.imgServer)
        self.labelServer.pack()

    def resize_image(self, image_path, img_size):
        original_image = Image.open(image_path)
        resized_image = original_image.resize(img_size)
        return ImageTk.PhotoImage(resized_image)

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
    def reset_delay(self):
        self.cumulativedelay = 0


state = "disconnected"
connectionBTN = None
dataBTN = None
closeBTN = None


def connection_msgs(app):
    app.reset_delay()
    app.write_delayed("computer", "Connexion au serveur")
    app.write_delayed("computer", "Envoi SYN", 0)
    app.write_delayed("server", "Envoi SYN+ACK", 1000)
    app.write_delayed("computer", "Evnoi ACK", 1000)
    app.write_delayed("server", "Connecté à l'ordinateur", 1000)

def data_transfer_msgs(app, n, rcvwindow):
    app.reset_delay()
    packetSize = math.floor(rcvwindow/n)
    seqNumber = 1
    app.write_delayed("computer", f"Envoi ACK=0, N={n}, rcvwindow={rcvwindow}o", 0)
    app.write_delayed("server", f"Le serveur doit envoyer {n} paquets de {packetSize}o chacun", 1000)
    for i in range(0, n):
        ack = False
        while not ack:
            app.write_delayed("server", f"Envoi SEQ={seqNumber}, size(data)={packetSize}o", 1000)
            app.write_delayed("computer", f"Recu {packetSize}o de données SEQ={seqNumber}", 1000)
            if random.randint(0, 5):
                ack = True
            else:
                app.write_delayed("computer", f"ERREUR: NACK={seqNumber}", 0)
        seqNumber += packetSize
        app.write_delayed("computer", f"Envoi ACK={seqNumber}", 0)

def close_msgs(app):
    app.reset_delay()
    app.write_delayed("computer", "Envoi FIN", 100)
    app.write_delayed("server", "Envoi ACK", 1000)
    app.write_delayed("server", "Envoi FIN", 1000)
    app.write_delayed("computer", "Envoi ACK", 1000)
    app.write_delayed("computer", "Wait 30sec before close", 0)
    app.write_delayed("server", "Connection closed", 1000)
    app.write_delayed("computer", "Connection closed", 30000)

def connection(app):
    set_state_working()
    connection_msgs(app)
    app.master.after(app.cumulativedelay, set_state_connected)

def data_transfer(app, n, rcvwindow):
    set_state_working()
    data_transfer_msgs(app, n, rcvwindow)
    app.master.after(app.cumulativedelay, set_state_connected)

def close(app):
    set_state_working()
    close_msgs(app)
    app.master.after(app.cumulativedelay, set_state_disconnected)

def enable_BTN(btn):
    btn.config(state="active")

def disable_BTN(btn):
    btn.config(state="disable")

def set_state_disconnected():
    global state
    state = "disconnected"
    update_btns()

def set_state_working():
    global state
    state = "working"
    update_btns()  

def set_state_connected():
    global state
    state = "connected"
    update_btns()

def update_btns():
    if state == "disconnected":
        enable_BTN(connectionBTN)
        disable_BTN(dataBTN)
        disable_BTN(closeBTN)
    elif state == "connected":
        disable_BTN(connectionBTN)
        enable_BTN(dataBTN)
        enable_BTN(closeBTN)
    elif state == "working":
        disable_BTN(connectionBTN)
        disable_BTN(dataBTN)
        disable_BTN(closeBTN)



def main():
    global state, connectionBTN, closeBTN, dataBTN
    root = Tk()
    app = MainWindow(root)

    n_label = Label(app.master, text="n:")
    n_label.pack(side="left", padx=5, pady=5)
    n_entry = Entry(app.master, width=5)
    n_entry.insert(0, "10") 
    n_entry.pack(side="left", padx=5, pady=5)

    rcvwindow_label = Label(app.master, text="rcvwindow:")
    rcvwindow_label.pack(side="left", padx=5, pady=5)
    rcvwindow_entry = Entry(app.master, width=5)
    rcvwindow_entry.insert(0, "1000")
    rcvwindow_entry.pack(side="left", padx=5, pady=5)

    connectionBTN = Button(app.master, text="Connection", command=lambda: connection(app))
    connectionBTN.pack(side='left', padx=10, pady=10)
    dataBTN = Button(app.master, text="Data transfer", command=lambda: data_transfer(app, int(n_entry.get()), int(rcvwindow_entry.get())))
    dataBTN.pack(side='left', padx=10, pady=10)
    closeBTN = Button(app.master, text="Close", command=lambda: close(app))
    closeBTN.pack(side='left', padx=10, pady=10)

    update_btns()

    root.mainloop()

if __name__ == "__main__":
    main()
