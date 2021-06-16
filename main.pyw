from PyQt5 import QtWidgets, uic
from library.login.login import UI
import sys

class ToolUI(UI):
    
    def __init__(self):
        self.load_login_ui()

    

app = QtWidgets.QApplication(sys.argv)
window = ToolUI()
app.exec_()