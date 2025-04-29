#conn.py
import socket
from PyQt5.QtCore import pyqtSignal, QObject, QThread, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel

class conn_mgr(QWidget):
    conn_success = pyqtSignal(str)
    new_message = pyqtSignal(str, str,str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Inserire IP')
        self.setGeometry(100, 100, 400, 100)

        layout = QVBoxLayout()
        self.Iplabel = QLabel('IP:', self)
        self.ipcamp = QLineEdit(self)
        self.portlabel = QLabel('PORT:', self)
        self.portcamp = QLineEdit(self)
        self.default = QLabel('if empty port will be 33000', self)
        self.connbut = QPushButton('Connettiti', self)

        layout.addWidget(self.Iplabel)
        layout.addWidget(self.ipcamp)
        layout.addWidget(self.portlabel)
        layout.addWidget(self.portcamp)
        layout.addWidget(self.default)
        layout.addWidget(self.connbut)
        self.setLayout(layout)

        self.connbut.clicked.connect(self.connessione)

        self.start_server()  # Avvia server all'avvio

    def connessione(self):
        try:
            ip = self.ipcamp.text()
            if not ip:
                self.setWindowTitle("Errore: Campo IP vuoto.")
                return

            if self.portcamp.text().isdigit():
                port = int(self.portcamp.text())
                if not (0 <= port <= 65535):
                    self.setWindowTitle("Errore: Porta fuori range.")
                    return
            else:
                port = 33000
                self.setWindowTitle("Porta non valida, uso 33000")
            self.remote_ip = ip
            
            self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_sock.settimeout(5)
            self.client_sock.connect((ip, port))
            self.client_sock.settimeout(None)

            self.client_thread = QThread()
            self.client_worker = self.Ricevitore(self.client_sock)
            self.client_worker.moveToThread(self.client_thread)
            self.client_worker.new_message.connect(self.new_message)
            self.client_thread.started.connect(self.client_worker.run)
            self.client_thread.start()

            self.conn_success.emit(ip)
            self.close()

        except Exception as e:
            self.setWindowTitle(f"Errore di connessione: {e}")

    def start_server(self):
        self.server_thread = QThread()
        self.server_worker = self.Server(self)
        self.server_worker.moveToThread(self.server_thread)
        self.server_worker.new_message.connect(self.new_message)
        self.server_thread.started.connect(self.server_worker.run)
        self.server_thread.start()

    def invio_messaggio(self, otp, key, messaggio_criptato):
        try:
            self.client_sock.sendall((otp + "//" + key + "//" + messaggio_criptato).encode('utf-8'))
        except Exception as e:
            print(f"Errore invio: {e}")

    class Ricevitore(QObject):
        new_message = pyqtSignal(str, str,str)

        def __init__(self, sock):
            super().__init__()
            self.sock = sock

        def run(self):
            while True:
                try:
                    data = self.sock.recv(4096)
                    if not data:
                        break
                    parts = data.decode().split("//", 2)
                    if len(parts) == 3:
                        otp, key, msg = parts
                        self.new_message.emit(otp, key,msg)
                except Exception as e:
                    print(f"Errore ricezione client: {e}")
                    break

    class Server(QObject):
        new_message = pyqtSignal(str, str,str)

        def run(self):
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind(("0.0.0.0", 33000))
            server_sock.listen(1)
            print("Server in ascolto su porta 33000...")
            while True:
                try:
                    conn, addr = server_sock.accept()
                    print(f"Connessione accettata da {addr}")
                    while True:
                        data = conn.recv(4096)
                        if not data:
                            break
                        parts = data.decode().split("//", 2)
                        if len(parts) == 3:
                            otp, key, msg = parts
                            self.new_message.emit(otp, key,msg)
                except Exception as e:
                    print(f"Errore server: {e}")
                    break
