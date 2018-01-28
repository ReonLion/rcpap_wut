import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from rcpap_wut_ui import Ui_MainWindow
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class main_form(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(main_form, self).__init__()
        self.setupUi(self)
        
        self.upload_lineEdit.setPlaceholderText('Please upload .txt files')
        self.tableview_show()
        
        self.image_1_label.setStyleSheet('QLabel {border-image: url(image1.png);}')
        self.image_2_label.setStyleSheet('QLabel {border-image: url(image2.png);}')
        self.icon_label.setStyleSheet('QLabel {border-image: url(icon.jpg);}')
        
    def tableview_show(self):
        model = QStandardItemModel(2, 4)
        row_1 = ['Path', 'path 1', 'path 2', 'path 3']
        row_2 = ['Delay(ns)', '70', '110', '160']
        
        for i in range(len(row_1)):
            item = QStandardItem(row_1[i])
            model.setItem(0, i, item)
            
        for i in range(len(row_2)):
            item = QStandardItem(row_2[i])
            model.setItem(1, i, item)
        
        self.tableView.setModel(model)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = main_form()
    win.show()
    sys.exit(app.exec_())