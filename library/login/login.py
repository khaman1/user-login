from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore
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

    def check_all_items(self):
        if self.check_all_box.isChecked():
            checked_status = QtCore.Qt.Checked
        else:
            checked_status = QtCore.Qt.Unchecked
        
        for i in range(0, len(self.folder_list)):
            self.folder_list.item(i).setCheckState(checked_status)


    def load_main_ui(self):
        uic.loadUi('design/main.ui', self)
        

        # ##################################
        # ##################################
        # self.folder_list = self.findChild(QtWidgets.QListWidget, 'folderListWidget')
        # self.check_all_box = self.findChild(QtWidgets.QCheckBox, 'checkAll')
        # self.check_all_box.clicked.connect(self.check_all_items)         
        # self.add_items_to_folder()
        # ##################################
        # ##################################
        # self.import_button = self.findChild(QtWidgets.QPushButton, 'importButton')
        # self.import_button.clicked.connect(self.start_import_process)
        # ##################################
        # ##################################
        # try:
        #     self.test_button = self.findChild(QtWidgets.QPushButton, 'testButton')
        #     self.test_button.clicked.connect(self.test_function)
        # except:
        #     pass
        

        self.resize(800, 600)
        self.show()

        vswr_ratio, dpm_status = get_vswr()
        output_power, dpm_status = get_fwd_power()
        reserve_power, dpm_status = get_rev_power()

        print(vswr_ratio)
        print(output_power)
        print(reserve_power)
        print(dpm_status)

    def test_function(self):
        pass

    def get_username(self):
        return self.username_input.text()
    def get_password(self):
        return self.password_input.text()
    def check_username(self):
        pass

    def is_user_valid(self, username, password):
        if password=='123456':
            return True
        
        return False
    
    def get_item_list(self):
        self.item_list = File().get_file_list_2()
        
        return self.item_list

    def get_item_list_that_checked(self):
        output = []
        
        for i in range(0, len(self.folder_list)):
            item = self.folder_list.item(0)

            if item.isSelected:
                output.append(i)
        
        output2 = []
        
        for i in range(0, len(output)):
            output2.append(self.item_list[output[i]])
                
        return output2
    
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

    def add_item_to_folder_list(self, name='123'):
        item = QtWidgets.QListWidgetItem(self.folder_list)
        item.setText(name)
        #item.setText(QtGui.QApplication.translate("Dialog", x, None,    QtGui.QApplication.UnicodeUTF8))
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.folder_list.addItem(item)

    def add_items_to_folder(self):
        for i in range(0,len(self.get_item_list())):
            self.add_item_to_folder_list(self.item_list[i]['name'])

    def do_by_status(self, code=0):
        self.STATUS = code

        if self.DEBUG:
            print("STATUS: " + str(self.STATUS))
        
        if self.STATUS == 1:
            self.import_button.setStyleSheet('border:2px solid #ff0000;')
            self.import_button.setText('Vui lòng đăng nhập tài khoản mua bán shopee\nvà bấm vào nút này để tiếp tục.')
            
        elif self.STATUS == 2:
            self.import_button.setStyleSheet('border:2px solid #00ff00;')
            self.import_button.setText('Đã đăng nhập Shopee\nĐang thêm sản phẩm ...')


    def start_import_process(self):
        while True:
            if not self.STATUS:
                self.shopee_browser = Shopee_Browser()
                sleep(1)
                

            if self.STATUS < 2:
                if self.shopee_browser.is_logged_in():
                    self.do_by_status(code=2)
                else:
                    self.do_by_status(code=1)
            elif self.STATUS == 2: ## Da login
                self.item_list_that_checked = self.get_item_list_that_checked()
                if self.DEBUG:
                    print(self.item_list_that_checked)
                
                ## Tong bao nhieu san pham?
                if len(self.item_list_that_checked) > 0:
                    ## Step 1
                    self.shopee_browser.open_page('https://banhang.shopee.vn/portal/product/category')
                    for i in range(1,len(self.item_list_that_checked)):
                        self.shopee_browser.open_page('https://banhang.shopee.vn/portal/product/category',new_tab=True)
                    
                    # Step 2
                    self.shopee_browser.page_1(self.item_list_that_checked)
                    

                self.STATUS += 1

            elif self.STATUS ==3:
                self.shopee_browser.page_2(self.item_list_that_checked)
                
                self.STATUS += 1
