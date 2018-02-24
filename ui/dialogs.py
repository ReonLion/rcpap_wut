# coding=utf-8

from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton, QWidget, QFormLayout, QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal
import sys

class delay_domain_dialog(QDialog):
    dialog_signal = pyqtSignal(dict)
    
    def __init__(self, parent = None):
        super(delay_domain_dialog, self).__init__(parent)
        self.setWindowTitle('Delay Domain Params')
        # 使用qdarkstyle主题
        # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        
        flo = QFormLayout()
        info_lineEdit = QLineEdit('All parameters have been set !')
        self.confirm_pushButton = QPushButton('Confirm')
        
        flo.addRow(info_lineEdit)
        flo.addRow(self.confirm_pushButton)
        
        self.confirm_pushButton.clicked.connect(self.confim_pushButton_clicked)
        # Confirm按钮连接accept()
        self.confirm_pushButton.clicked.connect(self.accept)
        
        self.setLayout(flo)
        
    def confim_pushButton_clicked(self):
        params_dict = {}
        self.dialog_signal.emit(params_dict)    
        
class frequency_domain_dialog(QDialog):
    dialog_signal = pyqtSignal(dict)
    
    def __init__(self, parent = None):
        super(frequency_domain_dialog, self).__init__(parent)
        self.setWindowTitle('frequency Domain Params')
        # 使用qdarkstyle主题
        # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        
        flo = QFormLayout()
        info_lineEdit = QLineEdit('All parameters have been set !')
        self.confirm_pushButton = QPushButton('Confirm')
        
        flo.addRow(info_lineEdit)
        flo.addRow(self.confirm_pushButton)
        
        self.confirm_pushButton.clicked.connect(self.confim_pushButton_clicked)
        # Confirm按钮连接accept()
        self.confirm_pushButton.clicked.connect(self.accept)
        
        self.setLayout(flo)
        
    def confim_pushButton_clicked(self):
        params_dict = {}
        self.dialog_signal.emit(params_dict)

class power_domain_dialog(QDialog):
    dialog_signal = pyqtSignal(dict)
    
    def __init__(self, parent = None):
        super(power_domain_dialog, self).__init__(parent)
        self.setWindowTitle('Power Domain Params')
        # 使用qdarkstyle主题
        # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        
        flo = QFormLayout()
        self.path_loss_polar_lineEdit = QLineEdit('3')
        self.path_loss_dielectric_lineEdit = QLineEdit('3')
        self.small_scale_beg_point_lineEdit = QLineEdit('7202')
        self.small_scale_end_point_lineEdit = QLineEdit('9300')
        self.small_scale_beg_ssf_point_lineEdit = QLineEdit('1')
        self.small_scale_end_ssf_point_lineEdit = QLineEdit('9300-7202')
        self.confirm_pushButton = QPushButton('Confirm')
        
        flo.addRow('Path Loss Polar', self.path_loss_polar_lineEdit)
        flo.addRow('Path Loss Dielectric', self.path_loss_dielectric_lineEdit)
        flo.addRow('Small Scale Begin Point ', self.small_scale_beg_point_lineEdit)
        flo.addRow('Small Scale End Point', self.small_scale_end_point_lineEdit)
        flo.addRow('Small Scale Begin SSF Point', self.small_scale_beg_ssf_point_lineEdit)
        flo.addRow('Small Scale End SSF Point', self.small_scale_end_ssf_point_lineEdit)
        flo.addRow(self.confirm_pushButton)
        
        self.confirm_pushButton.clicked.connect(self.confim_pushButton_clicked)
        # Confirm按钮连接accept()
        self.confirm_pushButton.clicked.connect(self.accept)
        
        self.setLayout(flo)
        
    def confim_pushButton_clicked(self):
        params_dict = {}
        try:
            params_dict['path_loss_polar'] = eval(self.path_loss_polar_lineEdit.text())
            params_dict['path_loss_dielectric'] = eval(self.path_loss_dielectric_lineEdit.text())
            params_dict['small_scale_beg_point'] = eval(self.small_scale_beg_point_lineEdit.text())
            params_dict['small_scale_end_point'] = eval(self.small_scale_end_point_lineEdit.text())
            params_dict['small_scale_beg_ssf_point'] = eval(self.small_scale_beg_ssf_point_lineEdit.text())
            params_dict['small_scale_end_ssf_point'] = eval(self.small_scale_end_ssf_point_lineEdit.text())
        except:
            QMessageBox.critical(self, 'Error', 'Params Input Error !')
            return
        
        self.dialog_signal.emit(params_dict)
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = power_domain_dialog()
    dialog.show()
    sys.exit(app.exec_())
        
