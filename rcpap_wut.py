# coding=utf-8

import os, datetime
import qdarkstyle
from ui.rcpap_wut_ui import Ui_MainWindow
from ui.dialogs import delay_domain_dialog, frequency_domain_dialog, power_domain_dialog
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QMessageBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QMovie

from work_threads import main_doppler_thread, delay_domain_thread, frequency_domain_thread, power_domain_thread
from check_directory import check_directory
from img_label_plot import img_label_plot

from multiprocessing import freeze_support

class main_form(QMainWindow, Ui_MainWindow):
    is_main_doppler_done = False
    txt_folder = ''
    xls_folder = ''
    
    def __init__(self):
        super(main_form, self).__init__()
        self.setupUi(self)
        # 禁止最大化按钮
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        # 禁止窗口调整大小
        self.setFixedSize(self.width(), self.height())
        
        # 检测目录是否存在，不存在则创建
        self.current_directory = os.getcwd()
        check_directory()
        
        # 使用qdarkstyle主题
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        
        # 初始化自定义ui显示
        self.custom_ui()
        
        # 连接各按钮的功能
        self.button_conn()
        
        # 连接tableWidget的点击操作
        self.main_doppler_tableWidget.itemClicked.connect(self.main_doppler_tableWidget_click)
        self.delay_domain_tableWidget.itemClicked.connect(self.delay_domain_tableWidget_click)
        self.frequency_domain_tableWidget.itemClicked.connect(self.frequency_domain_tableWidget_click)
        self.power_domain_tableWidget.itemClicked.connect(self.power_domain_tableWidget_click)
        
        # 保存图片在table中的位置的字典
        self.location_img = {}
        
        # loading gif 动画
        self.movie = QMovie(os.path.join('.', 'icon', 'loading.gif'))
        
        # 设置最近一次Main Doppler的时间
        self.set_latest_params_time()
        
    def custom_ui(self):
        '''
        lineEdit显示初始化
        '''
        self.upload_txt_lineEdit.setPlaceholderText('Select .txt directory')
        self.upload_excel_lineEdit.setPlaceholderText('Select .xls directory')
        
        
        '''
        tableWidget显示初始化
        '''
        # 禁止tableWidget可编辑
        self.main_doppler_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.delay_domain_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.frequency_domain_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.power_domain_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 水平方向表头隐藏
        self.main_doppler_tableWidget.verticalHeader().setVisible(False)
        self.delay_domain_tableWidget.verticalHeader().setVisible(False)
        self.frequency_domain_tableWidget.verticalHeader().setVisible(False)
        self.power_domain_tableWidget.verticalHeader().setVisible(False)
        # 垂直方向表头隐藏
        self.main_doppler_tableWidget.horizontalHeader().setVisible(False)
        self.delay_domain_tableWidget.horizontalHeader().setVisible(False)
        self.frequency_domain_tableWidget.horizontalHeader().setVisible(False)
        self.power_domain_tableWidget.horizontalHeader().setVisible(False)
        # 不显示网格线
        self.main_doppler_tableWidget.setShowGrid(False)
        self.delay_domain_tableWidget.setShowGrid(False)
        self.frequency_domain_tableWidget.setShowGrid(False)
        self.power_domain_tableWidget.setShowGrid(False)
        # 设置表格头为伸缩模式
        self.main_doppler_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.delay_domain_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.frequency_domain_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.power_domain_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 初始化为一行一列，显示'Results will be here'
        self.tablewidget_clear('main_doppler_tableWidget')
        self.tablewidget_clear('delay_domain_tableWidget')
        self.tablewidget_clear('frequency_domain_tableWidget')
        self.tablewidget_clear('power_domain_tableWidget')
        
    def button_conn(self):
        # 上传txt文件
        self.upload_txt_pushButton.clicked.connect(self.upload_txt_files)
        # 上传excel文件
        self.upload_excel_pushButton.clicked.connect(self.upload_excel_files)
        # main_doppler参数确定，多线程实例化main_doppler
        self.confirm_pushButton.clicked.connect(self.main_doppler_start)
        # delay_domain参数确定，多线程实例化rmsdelay_pathnum_analysis
        self.delay_pushButton.clicked.connect(self.delay_domain_setup)
        # frequency_domain参数确定，多线程实例化rmsdop
        self.frequency_pushButton.clicked.connect(self.frequency_domain_setup)
        # power_domain参数确定，多线程实例化small_scale_fading, AIC_Amp_determination, Propagation_path_loss
        self.power_pushButton.clicked.connect(self.power_domain_setup)
        # 禁止Detail按钮
        self.details_pushButton.setEnabled(False)
        # Detail按钮显示详情
        self.details_pushButton.clicked.connect(self.details_show)
        # 鼠标经过import_params按钮，显示上一次Main Doppler时间
        
        # import_params按钮导入最近一次运行的结果
        self.import_params_pushButton.clicked.connect(self.import_latest_params)
        
    def upload_txt_files(self):
        self.txt_folder = QFileDialog.getExistingDirectory(self, "Upload .txt files", "C:/")
        self.upload_txt_lineEdit.setReadOnly(True)
        self.upload_txt_lineEdit.setText(self.txt_folder)
        return
    
    def upload_excel_files(self):
        self.xls_folder = QFileDialog.getExistingDirectory(self, "Upload .xls files", "C:/")
        self.upload_excel_lineEdit.setReadOnly(True)
        self.upload_excel_lineEdit.setText(self.xls_folder)
        return
    
    def main_doppler_start(self):
        # 清空图片保存在表格中的位置
        self.location_img = {}
        
        '''
        参数从UI界面输入
        '''
        try:
            window = eval(self.window_lineEdit.text())
            TX_power = eval(self.tx_power_lineEdit.text())
            TX_Gain = eval(self.tx_gain_lineEdit.text())
            RX_Gain = eval(self.rx_gain_lineEdit.text())
            TX_heigh = eval(self.tx_heigh_lineEdit.text())
            RX_heigh = eval(self.rx_heigh_lineEdit.text())
            fc = eval(self.fc_lineEdit.text())
            ATT_mark = eval(self.att_mark_lineEdit.text())
            cable = eval(self.cable_lineEdit.text())
            chirp_num = eval(self.chirp_num_lineEdit.text())
        except:
            QMessageBox.critical(self, 'Error', 'Params Input Error !')
            return
        '''
        检测txt和excel目录是否有效
        '''
        if not os.path.isdir(self.txt_folder):
            QMessageBox.critical(self, 'Error', '.txt directory invalid !')
            return
        if not os.path.isdir(self.xls_folder):
            QMessageBox.critical(self, 'Error', '.xls directory invalid !')
            return
        
        # 初始化为一行一列，显示'Results will be here'
        self.tablewidget_clear('main_doppler_tableWidget')
        self.tablewidget_clear('delay_domain_tableWidget')
        self.tablewidget_clear('frequency_domain_tableWidget')
        self.tablewidget_clear('power_domain_tableWidget')
        
        # toolBox切换到索引0
        self.toolBox.setCurrentIndex(0)
        # loading gif 开始
        self.img_label.setMovie(self.movie)
        self.movie.start()
        # 禁止Detail按钮
        self.details_pushButton.setEnabled(False)
        
        # main_doppler_tableWidget显示Results will be here
        self.tablewidget_clear('main_doppler_tableWidget')
        
        
        '''
        main_doppler_thread线程开始
        '''
        self.main_doppler_workthread = main_doppler_thread(window = window, TX_power = TX_power, 
                                                           TX_Gain = TX_Gain, RX_Gain = RX_Gain,
                                                           TX_heigh = TX_heigh, RX_heigh = RX_heigh, 
                                                           fc = fc, ATT_mark = ATT_mark, cable = cable, 
                                                           chirp_num = chirp_num, txt_folder = self.txt_folder, 
                                                           xls_folder = self.xls_folder)
        self.main_doppler_workthread.start()
        self.main_doppler_workthread.sin_out.connect(self.main_doppler_done)
        return
    
    def main_doppler_done(self):
        # toolBox切换到索引0
        self.toolBox.setCurrentIndex(0)
        # 获取文件夹下排序后的图片名路径
        img_list = self.read_results_directory(os.path.join('.' , 'results', 'Main_function_and_doppler'))
        # 控制对应的table_widget显示n行2列的图片, 并且默认在view_label中显示0行0列的图片
        self.tablewidget_show('main_doppler_tableWidget', img_list)
        # 激活Detail按钮
        self.details_pushButton.setEnabled(True)
        
        # 确认main_doppler结束
        self.is_main_doppler_done = True
        
        ## 关闭main_doppler线程
        #self.main_doppler_workthread.quit()
        ## 等待main_doppler线程退出完毕
        #self.main_doppler_workthread.wait()
        ## 删除线程
        #del self.main_doppler_workthread
        ## 内存回收
        #gc.collect()
        
        
        # 设置最近一次Main Doppler时间
        self.set_latest_params_time()
        
    def delay_domain_setup(self):
        if not self.is_main_doppler_done:
            QMessageBox.critical(self, 'Error', 'Please run Main Doppler first !')
            return
        dialog = delay_domain_dialog()
        # 连接子窗口的自定义信号与主窗体的槽函数
        dialog.dialog_signal.connect(self.delay_domain_start)
        dialog.show()
        dialog.exec_()
        return
    
    def delay_domain_start(self):
        # toolBox切换到索引1
        self.toolBox.setCurrentIndex(1)
        # loading gif 开始
        self.img_label.setMovie(self.movie)
        self.movie.start()
        # img_label的toolTip清空
        self.img_label.setToolTip('')
        # 禁止Detali按钮
        self.details_pushButton.setEnabled(False)
    
        # delay_domain_tableWidget显示Results will be here
        self.tablewidget_clear('delay_domain_tableWidget')
        
        # 多线程实例化delay_domain中的类
        self.delay_domain_workthread = delay_domain_thread()
        self.delay_domain_workthread.start()
        self.delay_domain_workthread.sin_out.connect(self.delay_domain_done)
        
        return
    
    def delay_domain_done(self):
        # toolBox切换到索引1
        self.toolBox.setCurrentIndex(1)
        # 获取文件夹下排序后的图片名路径
        img_list = self.read_results_directory(os.path.join('.' , 'results', 'delay_domain'))
        # 控制对应的table_widget显示n行2列的图片, 并且默认在view_label中显示0行0列的图片
        self.tablewidget_show('delay_domain_tableWidget', img_list)
        # 激活Detai按钮
        self.details_pushButton.setEnabled(True)
        return
    
    def frequency_domain_setup(self):
        if not self.is_main_doppler_done:
            QMessageBox.critical(self, 'Error', 'Please run Main Doppler first !')
            return
        
        dialog = frequency_domain_dialog()
        # 连接子窗口的自定义信号与主窗体的槽函数
        dialog.dialog_signal.connect(self.frequency_domain_start)
        dialog.show()
        dialog.exec_()
        return
    
    def frequency_domain_start(self):
        # toolBox切换到索引2
        self.toolBox.setCurrentIndex(2)
        # loading gif 开始
        self.img_label.setMovie(self.movie)
        self.movie.start()
        # img_label的toolTip清空
        self.img_label.setToolTip('')
        # 禁止Detali按钮
        self.details_pushButton.setEnabled(False)
    
        # delay_domain_tableWidget显示Results will be here
        self.tablewidget_clear('frequency_domain_tableWidget')
    
        # 多线程实例化delay_domain中的类
        self.frequency_domain_workthread = frequency_domain_thread()
        self.frequency_domain_workthread.start()
        self.frequency_domain_workthread.sin_out.connect(self.frequency_domain_done)
        return
    
    def frequency_domain_done(self):
        # toolBox切换到索引2
        self.toolBox.setCurrentIndex(2)
        # 获取文件夹下排序后的图片名路径
        img_list = self.read_results_directory(os.path.join('.' , 'results', 'frequency_domain'))
        # 控制对应的table_widget显示n行2列的图片, 并且默认在view_label中显示0行0列的图片
        self.tablewidget_show('frequency_domain_tableWidget', img_list)
        # 激活Detai按钮
        self.details_pushButton.setEnabled(True)
        return
    
    def power_domain_setup(self):
        if not self.is_main_doppler_done:
            QMessageBox.critical(self, 'Error', 'Please run Main Doppler first !')
            return
        
        dialog = power_domain_dialog()
        # 连接子窗口的自定义信号与主窗体的槽函数
        dialog.dialog_signal.connect(self.power_domain_start)
        dialog.show()
        dialog.exec_()
        return
    
    def power_domain_start(self, params_dict):
        # toolBox切换到索引3
        self.toolBox.setCurrentIndex(3)
        # loading gif 开始
        self.img_label.setMovie(self.movie)
        self.movie.start()
        # img_label的toolTip清空
        self.img_label.setToolTip('')
        # 禁止Detali按钮
        self.details_pushButton.setEnabled(False)
    
        # delay_domain_tableWidget显示Results will be here
        self.tablewidget_clear('power_domain_tableWidget')
    
        # 多线程实例化delay_domain中的类
        self.power_domain_workthread = power_domain_thread(params_dict)
        self.power_domain_workthread.start()
        self.power_domain_workthread.sin_out.connect(self.power_domain_done)
        return
    
    def power_domain_done(self):
        # toolBox切换到索引3
        self.toolBox.setCurrentIndex(3)        
        # 获取文件夹下排序后的图片名路径
        img_list = self.read_results_directory(os.path.join('.' , 'results', 'power_domain'))
        # 控制对应的table_widget显示n行2列的图片, 并且默认在view_label中显示0行0列的图片
        self.tablewidget_show('power_domain_tableWidget', img_list)
        # 激活Detai按钮
        self.details_pushButton.setEnabled(True)
        return
    
    
    '''
    ------------------------------------------------------------------------
    读取results子文件夹下的图片，排序，返回图片路径列表
    ------------------------------------------------------------------------
    '''
    def read_results_directory(self, directory):
        img_list = os.listdir(directory)
        img_list.sort()
        img_list = [os.path.join(directory, img) for img in img_list]
        return img_list
    
    '''
    ------------------------------------------------------------------------
    初始化对应table_name的tableWidget为一行一列，
    显示'Results will be here'
    ------------------------------------------------------------------------
    '''
    def tablewidget_clear(self, table_name):
        new_item = QTableWidgetItem('Results will\n be here')
        new_item.setTextAlignment(Qt.AlignCenter)
        
        table_widget = self.findChild((QTableWidget,), table_name)
        table_widget.setRowCount(1)
        table_widget.setColumnCount(1)
        table_widget.setItem(0, 0, new_item)
        table_widget.verticalHeader().setStretchLastSection(True)                                       # 最后一行填满表格        
    
    
    '''
    ------------------------------------------------------------------------
    控制对应的table_widget显示n行2列的图片, 并且默认在view_label中显示0行0列的图片
    ------------------------------------------------------------------------
    '''
    def tablewidget_show(self, table_name, img_list):
        img_num = len(img_list)
        table_widget = self.findChild((QTableWidget,), table_name)
        table_widget.verticalHeader().setStretchLastSection(False)                                       # 取消最后一行填满表格
        table_widget.setColumnCount(2)                                                                   # 分两列显示
        table_widget.setRowCount(int(img_num / 2 + 0.5))                                                 # 设置行数
        table_widget.setIconSize(QSize(64, 48))                                                          # 设置图片大小64*48
        
        for i in range(0, table_widget.columnCount()):
            table_widget.setColumnWidth(i, 64 + 10)
        for i in range(0, table_widget.rowCount()):
            table_widget.setRowHeight(i, 48 + 10)
        
        # 显示img_list的图片
        i = 0
        j = 0
        for img in img_list:
            new_item = QTableWidgetItem(QIcon(img), '')
            # 字典保存图片在几张table的位置
            self.location_img['%28s%2d%2d' % (table_name, i, j)] = img
            table_widget.setItem(i, j, new_item)
            j += 1
            if j == 2:
                j = 0
                i += 1
                
        # img_label显示第一张图片
        self.movie.stop()
        key = '%28s%2d%2d' % (table_name, 0, 0)
        self.img_label.setPixmap(QPixmap(self.location_img[key]))
        # 给label设置toolTip为文件名，方便Detail时索引
        self.img_label.setToolTip(os.path.basename(self.location_img[key]))
        return
        
    '''
    --------------------------------------------------------------------------
    tableWidget点击操作
    --------------------------------------------------------------------------
    '''
    def main_doppler_tableWidget_click(self, item):
        i = item.row()
        j = item.column()
        key = '%28s%2d%2d' % ('main_doppler_tableWidget', i, j)
        try:
            img = self.location_img[key]
            self.img_label.setPixmap(QPixmap(img).scaled(640, 480))
            # 给label设置toolTip为文件名，方便Detail时索引
            self.img_label.setToolTip(os.path.basename(img))
            # 设置detail按钮为True
            self.details_pushButton.setEnabled(True)
        except:
            pass
        return
    
    def delay_domain_tableWidget_click(self, item):
        i = item.row()
        j = item.column()
        key = '%28s%2d%2d' % ('delay_domain_tableWidget', i, j)
        try:
            img = self.location_img[key]
            self.img_label.setPixmap(QPixmap(img).scaled(640, 480))
            # 给label设置toolTip为文件名，方便Detail时索引
            self.img_label.setToolTip(os.path.basename(img))
            # 设置detail按钮为True
            self.details_pushButton.setEnabled(True)
        except:
            pass
        return
    
    def frequency_domain_tableWidget_click(self, item):
        i = item.row()
        j = item.column()
        key = '%28s%2d%2d' % ('frequency_domain_tableWidget', i, j)
        try:
            img = self.location_img[key]
            self.img_label.setPixmap(QPixmap(img).scaled(640, 480))
            # 给label设置toolTip为文件名，方便Detail时索引
            self.img_label.setToolTip(os.path.basename(img))
            # 设置detail按钮为True
            self.details_pushButton.setEnabled(True)
        except:
            pass
        return
    
    def power_domain_tableWidget_click(self, item):
        i = item.row()
        j = item.column()
        key = '%28s%2d%2d' % ('power_domain_tableWidget', i, j)
        try:
            img = self.location_img[key]
            self.img_label.setPixmap(QPixmap(img).scaled(640, 480))
            # 给label设置toolTip为文件名，方便Detail时索引
            self.img_label.setToolTip(os.path.basename(img))
            # 设置detail按钮为True
            self.details_pushButton.setEnabled(True)
        except:
            pass
        return
    
    def details_show(self):
        self.details_plot = img_label_plot(self.img_label.toolTip())
        
    def import_latest_params(self):
        # 清除所有的table_widget
        self.tablewidget_clear('main_doppler_tableWidget')
        self.tablewidget_clear('delay_domain_tableWidget')
        self.tablewidget_clear('frequency_domain_tableWidget')
        self.tablewidget_clear('power_domain_tableWidget')
        
        main_doppler_file = os.path.join('.', 'results', 'Main_function_and_doppler', 'Main_function_and_doppler_fig1.png')
        if os.path.isfile(main_doppler_file):
            self.main_doppler_done()
        else:
            QMessageBox.critical(self, 'Error', 'The import failured !')
            return
        
        delay_domain_file = os.path.join('.', 'results', 'delay_domain', 'rmsdelay_pathnum_analysis_main_function_fig1.png')
        if os.path.isfile(delay_domain_file):
            # 比较时间
            main_doppler_file_mtime = os.path.getmtime(main_doppler_file)
            delay_domain_file_mtime = os.path.getmtime(delay_domain_file)
            print(datetime.datetime.fromtimestamp(delay_domain_file_mtime))
            print(datetime.datetime.fromtimestamp(main_doppler_file_mtime))
            if datetime.datetime.fromtimestamp(delay_domain_file_mtime) > datetime.datetime.fromtimestamp(main_doppler_file_mtime):
                self.delay_domain_done()
        
        fre_domain_file = os.path.join('.', 'results', 'frequency_domain', 'rmsdop_main_function_fig3.png')
        if os.path.isfile(fre_domain_file):
            # 比较时间
            main_doppler_file_mtime = os.path.getmtime(main_doppler_file)
            fre_domain_file_mtime = os.path.getmtime(fre_domain_file)
            if datetime.datetime.fromtimestamp(fre_domain_file_mtime) > datetime.datetime.fromtimestamp(main_doppler_file_mtime):
                self.frequency_domain_done()
        
        power_domain_file = os.path.join('.', 'results', 'power_domain', 'AIC_dis_deter_mainfunction_a_fig1.png')
        if os.path.isfile(power_domain_file):
            # 比较时间
            main_doppler_file_mtime = os.path.getmtime(main_doppler_file)
            power_domain_file_mtime = os.path.getmtime(power_domain_file)
            if datetime.datetime.fromtimestamp(power_domain_file_mtime) > datetime.datetime.fromtimestamp(main_doppler_file_mtime):
                self.power_domain_done()
                
        self.main_doppler_done()
        
        QMessageBox.information(self, '', 'The import successed !')
        return
    
    def set_latest_params_time(self):
        if not os.path.exists(os.path.join('.', 'params', 'delay_paras.npz')):
            self.import_params_pushButton.setToolTip('No latest results !')
        else:
            timestamp  = os.path.getmtime(os.path.join('.', 'params', 'delay_paras.npz'))
            time = datetime.datetime.fromtimestamp(timestamp)
            time = time.strftime('%Y-%m-%d %H:%M:%S')
            self.import_params_pushButton.setToolTip('Latest: ' + time)
        
        
if __name__ == '__main__':
    # 多进程打包为exe需要
    freeze_support()
    
    app = QApplication(sys.argv)
    win_form = main_form()
    win_form.show()
    
    sys.exit(app.exec_())
    