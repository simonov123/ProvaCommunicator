import socket
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit,QLabel
actualip=""
class conn_mgr(QWidget):
    conn_success = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Inserire IP')
        self.setGeometry(100, 100, 400, 100)
        layout = QVBoxLayout()
        self.Iplabel = QLabel('IP:',self)
        self.ipcamp = QLineEdit(self)
        self.portlabel=QLabel('PORT:',self)
        self.portcamp=QLineEdit(self)
        self.default=QLabel('if empty port will be 3303',self)
        self.connbut = QPushButton('Connettiti',self)
        layout.addWidget(self.Iplabel)
        layout.addWidget(self.ipcamp)
        layout.addWidget(self.portlabel)
        layout.addWidget(self.portcamp)
        layout.addWidget(self.default)
        layout.addWidget(self.connbut)
        self.connbut.clicked.connect(self.connessione)
        self.setLayout(layout)
    def connessione(self):
        try:
            ip=self.ipcamp.text()
            print(ip)
            if self.portcamp.text().isdigit():  # Verifica se il testo inserito è numerico
                port = int(self.portcamp.text())
                if port < 0 or port > 65535:  # Controlla che la porta sia valida (da 0 a 65535)
                    self.setWindowTitle("Errore: Porta fuori dal range valido (0-65535).")
                    return
            else:
                # Se la porta non è valida, imposta una porta di default
                port = 3303  # Porta predefinita
                self.setWindowTitle(f"Porta non valida, utilizzando la porta di default: {port}")
            print(port)
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((ip,port))
            actualip=ip
            self.conn_success.emit(ip)
            self.close()
        except socket.timeout:
            self.setWindowTitle(f"Errore: Timeout raggiunto mentre cercavi di connetterti a {ip}:{porta}")
        except socket.error as e:
            self.setWindowTitle(f"Errore di connessione: {e}")
    def invio_messaggio(messaggio_crypt):
        print("todo")

        




    









