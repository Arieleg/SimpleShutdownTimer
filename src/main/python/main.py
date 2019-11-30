import configparser
import os
import sys

from PyQt5.QtCore import pyqtSlot, QTranslator
from PyQt5.QtWidgets import QMainWindow, QApplication

from fbs_runtime.application_context.PyQt5 import ApplicationContext

from ui.Ui_mainwindow import Ui_MainWindow


class ShutdownScheduler(QMainWindow):
    lang_conf_folder_path = str(os.getenv('APPDATA')) +'/SimpleShutdownTimer/'
    lang_conf_file_path= str(os.getenv('APPDATA')) + '/SimpleShutdownTimer/lang.ini'

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.pref_lang()
        self.ui.pushButtonOk.clicked.connect(self.program_new)
        self.ui.actionCancel_shutdown.triggered.connect(self.cancel)
        self.ui.actionEspa_ol.triggered.connect(self.tr_spanish)
        self.ui.actionEnglish.triggered.connect(self.tr_english)

    @pyqtSlot()
    def program_new(self):
        hours = self.ui.spinBoxHours.value()
        minutes = self.ui.spinBoxMinutes.value()
        seconds = self.ui.spinBoxSeconds.value()
        time = hours * 3600 + minutes * 60 + seconds
        os.system('shutdown /S /T {}'.format(time))


    @pyqtSlot()
    def cancel(self):
        os.system('shutdown /A')

    @pyqtSlot()
    def tr_spanish(self):
        translator = QTranslator()
        translator.load(":/Languages/Languages/mainwindow_es.qm")
        QApplication.instance().installTranslator(translator)
        self.ui.retranslateUi(self)
        config = configparser.ConfigParser()
        config['LANGUAGE'] = {'lang': 'es'}
        with open(self.lang_conf_file_path, 'w') as lang_configfile:
            config.write(lang_configfile)

    @pyqtSlot()
    def tr_english(self):
        translator = QTranslator()
        translator.load(":/Languages/Languages/mainwindow_en.qm")
        QApplication.instance().installTranslator(translator)
        self.ui.retranslateUi(self)
        config = configparser.ConfigParser()
        config['LANGUAGE'] = {'lang': 'es'}
        with open(self.lang_conf_file_path, 'w') as lang_configfile:
            config.write(lang_configfile)

    def pref_lang(self):
        config = configparser.ConfigParser()
        if config.read(self.lang_conf_file_path):
            lang = config['LANGUAGE']['lang']

            if lang == 'en':
                self.tr_english()
            elif lang == 'es':
                self.tr_spanish()
            else:
                self.tr_english()
        else:
            if not os.path.isdir(self.lang_conf_folder_path):
                os.makedirs(self.lang_conf_folder_path)
            print(self.lang_conf_folder_path)
            config['LANGUAGE'] = {'lang': 'en'}
            with open(self.lang_conf_file_path, 'w') as lang_configfile:
                config.write(lang_configfile)


if __name__ == "__main__":
    # app = QApplication([])
    appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
    window = ShutdownScheduler()
    window.show()
    exit_code = appctxt.app.exec_()  # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
    # sys.exit(app.exec_())
