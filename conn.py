#conn.py
import socket
from PyQt5.QtCore import pyqtSignal,QObject,QThread
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit,QLabel
actualip=""
class conn_mgr(QWidget):
    conn_success = pyqtSignal(str)
    new_message = pyqtSignal(str, str)
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
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.settimeout(5)  # timeout breve per evitare blocchi infiniti
            self.s.connect((ip, port))
            self.s.settimeout(None) 
            self.thread = QThread()
            self.worker = self.Ricevitore(self.s)
            self.worker.moveToThread(self.thread)
            self.worker.new_message.connect(self.new_message)
            self.thread.started.connect(self.worker.run)
            self.thread.start()    
            print(port)
            actualip=ip
            self.conn_success.emit(ip)
            self.close()
        except socket.timeout:
            self.setWindowTitle(f"Errore: Timeout raggiunto mentre cercavi di connetterti a {ip}:{port}")
        except socket.error as e:
            self.setWindowTitle(f"Errore di connessione: {e}")
    def invio_messaggio(self,otp,key,messaggio_criptato):
         if self.s:
            try:
                self.s.sendall((otp + "//" + key + "//" + messaggio_criptato).encode('utf-8'))
            except socket.error as e:
                print(f"Errore invio messaggio: {e}")
   
    class Ricevitore(QObject):
      new_message = pyqtSignal(str, str)  # chiave_criptata, messaggio_criptato

      def __init__(self, sock):
        super().__init__()
        self.sock = sock
        self.running = True

      def run(self):
        while self.running:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break
                decoded = data.decode('utf-8')
                parts = decoded.split("//", 2)
                if len(parts) == 3:
                    otp,key,messaggio_criptato = parts
                    self.new_message.emit(otp,key,messaggio_criptato)
            except Exception as e:
                print(f"Errore ricezione: {e}")
                break



        
        

        




    









