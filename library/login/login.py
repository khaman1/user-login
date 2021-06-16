from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer,QDateTime
from time import sleep
from ..telnet.telnet import *

class UI(QtWidgets.QMainWindow):
    DEBUG = 1
    STATUS = 0
    
    def __init__(self):
        pass

    def load_login_ui(self):
        super(UI, self).__init__()
        uic.loadUi('design/login.ui', self)

        self.login_button = self.findChild(QtWidgets.QPushButton, 'loginButton') # Find the button
        self.login_button.clicked.connect(self.pressed_login_button) # Remember to pass the definition/method, not the return value!

        self.username_input = self.findChild(QtWidgets.QLineEdit, 'username_input')
        self.password_input = self.findChild(QtWidgets.QLineEdit, 'password_input')

        self.resize(670, 215)
        self.show()


    def load_main_ui(self):
        uic.loadUi('design/main.ui', self)
        
        ##################################
        ##################################
        self.resize(900, 600)
        self.show()

        self.timer=QTimer()
        self.timer.timeout.connect(self.exec)
        self.timer.start(5000)

    def exec(self): 
        vswr_ratio, dpm_status = get_vswr()
        output_power, dpm_status = get_fwd_power()
        reserve_power, dpm_status = get_rev_power()

        
        print(vswr_ratio)
        print(output_power)
        print(reserve_power)

        ####################
        ####################
        if vswr_ratio:
            self.findChild(QtWidgets.QLineEdit, 'VSWR1').setText(str(vswr_ratio).upper())

        if output_power:
            self.findChild(QtWidgets.QLineEdit, 'FWD1').setText(str(output_power).upper())

        if reserve_power:
            self.findChild(QtWidgets.QLineEdit, 'REV1').setText(str(reserve_power).upper())

        ####################
        ####################
        vswr_ratio_br = get_vswr_br()
        if vswr_ratio_br:
            self.findChild(QtWidgets.QLineEdit, 'VSWR_BR1').setText(str(vswr_ratio_br).upper())
            

        rssi_failure_cnt1, rssi_failure_cnt2, rssi_failure_cnt3 = get_rssi_br()
        if rssi_failure_cnt1 != '':
            self.findChild(QtWidgets.QLineEdit, 'RSSI1_BR1').setText(str(rssi_failure_cnt1).upper())

        if rssi_failure_cnt2 != '':
            self.findChild(QtWidgets.QLineEdit, 'RSSI2_BR1').setText(str(rssi_failure_cnt2).upper())

        if rssi_failure_cnt3 != '':
            self.findChild(QtWidgets.QLineEdit, 'RSSI3_BR1').setText(str(rssi_failure_cnt3).upper())
        

        

    def get_username(self):
        return self.username_input.text()
    def get_password(self):
        return self.password_input.text()
    def check_username(self):
        pass

    def is_user_valid(self, username, password):
        if password=='123456':
            return True
        
        return True
    
    def pressed_login_button(self):
        # This is executed when the button is pressed
        self.username = self.get_username()
        self.password = self.get_password()

        if self.DEBUG:
            print('Username: ' + self.username)
            print('Password: ' + self.password)

        if self.is_user_valid(self.username, self.password):
            if self.DEBUG:
                print("Logged in successfully ...")
                
            self.load_main_ui()