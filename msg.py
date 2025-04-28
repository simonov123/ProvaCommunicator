#msg.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit,QLabel
from conn import conn_mgr
from cryptmgr import cryptmgr
crmgr=cryptmgr()
class messenger(QWidget):
    actualip=""
    


    def __init__(self):
        super().__init__()
        print("Люблю Анну")
        self.setWindowTitle('Messenger Sicuro')
        self.setGeometry(100, 100, 400, 400)
        layout = QVBoxLayout()
        self.chat_window = QTextEdit(self)
        self.chat_window.setReadOnly(True)
        self.chat_window.verticalScrollBar().setValue(self.chat_window.verticalScrollBar().maximum())
        self.message_input = QLineEdit(self)
        send_button = QPushButton('Invia', self)
        conn_button = QPushButton('Connettiti',self)
        conn_button.clicked.connect(self.connessione)
        send_button.clicked.connect(self.invio)
        layout.addWidget(self.chat_window)
        layout.addWidget(self.message_input)
        layout.addWidget(send_button)
        layout.addWidget(conn_button)
        self.setLayout(layout)
    def connessione(self):
        self.cmgr = conn_mgr() 
        self.cmgr.conn_success.connect(self.received_ip)  
        self.cmgr.show()  
    def received_ip(self, ip):
        print(f"Connessione riuscita all'IP: {ip}")
        self.chat_window.append(f"Connesso a: {ip}") 
        self.actualip=ip
    def invio(self):
        clear_msg=self.message_input.text()
        #if self.actualip != "":      controllo bloccato per debug 
        self.chat_window.append("tu:"+clear_msg)
        key=crmgr.keygen(clear_msg)
        cryptmsg=crmgr.OTPcrypt(clear_msg,key)
        print(cryptmsg)
        enkey=crmgr.encrypt_otp(key)
        print(enkey)
        

        
    
app=QApplication(sys.argv)
mess=messenger()
mess.show()
sys.exit(app.exec_())





