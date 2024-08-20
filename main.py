import sys
import os
import subprocess
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QSystemTrayIcon, QStyle, QAction, QMenu, qApp
from PyQt5.QtCore import QTimer, QThread, QTranslator, pyqtSignal
from mainWindow import Ui_MainWindow  # Импортируем сгенерированный класс интерфейса
from lang import LangConstants as LC

#Отдельный поток для выполнения всех команд, чтобы они не блокировали интерфейс
class CommandThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(Exception)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        try:
            subprocess.run(self.command, shell=True, check=True)
            self.finished.emit()
        except Exception as e:
            self.error.emit(e)
            

class MainWindow(QMainWindow, Ui_MainWindow):

    DIRNAME = os.path.dirname(__file__)

    CONFIG_FILE = os.path.join(DIRNAME, 'config.ini')
    LOCALES_PATH = os.path.join(DIRNAME, 'locales')

    LANG_PREFIX = 'lang_'
    LANG_EXTENSION = '.qm'

    config = {}

    translator = None

    trayIcon = None
    trayMenu = None
    trayStartStopAction = None
    trayRestartAction = None
    traySeparator = None
    trayShowAction = None
    trayCloseAction = None

    def __init__(self):
        super().__init__()

        self.translator = QTranslator()

        #Хранить все потоки будем тут, чтобы они не уничтожались после выполнения runCommand
        self.threads = []

        self.setupUi(self)  # Настраиваем UI
        self.setFixedSize(self.size())

        self.btnStartStop.clicked.connect(self.onBtnStartStopClick)
        self.btnRestart.clicked.connect(self.onBtnRestartClick)

        ### Работа с треем
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMenuButton))

        #Кнопки в трее
        self.trayStartStopAction = QAction(None, self)
        self.trayRestartAction = QAction(None, self)

        #События по нажатию на кнопки трея
        self.trayStartStopAction.triggered.connect(self.onBtnStartStopClick)
        self.trayRestartAction.triggered.connect(self.onBtnRestartClick)

        self.trayMenu = QMenu()

        #Добавить кнопкни запуска/остановки и перезапуска служб
        self.trayMenu.addAction(self.trayStartStopAction)
        self.trayMenu.addAction(self.trayRestartAction)

        self.traySeparator = self.trayMenu.addSeparator()

        #Кнопка показа окна
        self.trayShowAction = QAction(None, self)
        self.trayShowAction.triggered.connect(self.show)
        self.trayMenu.addAction(self.trayShowAction)

        #Кнопка закрытия программы
        self.trayCloseAction = QAction(None, self)
        self.trayCloseAction.triggered.connect(qApp.quit)
        self.trayMenu.addAction(self.trayCloseAction)

        self.trayIcon.setContextMenu(self.trayMenu)
        self.trayIcon.show()

        ###

        if not os.path.exists(self.LOCALES_PATH):
            os.makedirs(self.LOCALES_PATH)      

        #В папке с языками взять все файлы формата lang_*.qm и добавить их в список языков
        for filename in os.listdir(self.LOCALES_PATH):
            if filename.startswith(self.LANG_PREFIX) and filename.endswith(self.LANG_EXTENSION):
                lang = filename[len(self.LANG_PREFIX):-len(self.LANG_EXTENSION)]

                if lang != 'en':
                    action = QAction(lang, self)
                    action.setProperty("lang", os.path.join(self.LOCALES_PATH, filename))
                    action.triggered.connect(self.onLangActionClick)
                    self.menuLanguage.addAction(action)  
        
        self.langEn.triggered.connect(self.onLangActionClick)

        ###  

        #Если есть файл конфига, загрузить его
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, 'r') as f:
                self.config = json.load(f)

        #Поставить значения по умолчанию, если таковых нет
        if ('minimizeToTray' not in self.config):
            self.config['minimizeToTray'] = True
        
        if ('lang' not in self.config):
            self.config['lang'] = 'en' 


        #Выставить нужные настройки
        self.aToTray.setChecked(self.config['minimizeToTray'])
        self.changeLanguage(self.config['lang'])

        app.aboutToQuit.connect(self.saveConfig)

        ###

        self.updateLAMPStatus()

        #Каждые 5 секунд обновлять состояние служб
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateLAMPStatus)
        self.timer.start(5000)

    def closeEvent(self, event):
        if (self.aToTray.isChecked()):
            event.ignore()
            self.hide() 

    #Сохранить конфиг в файл
    def saveConfig(self):
        self.config['minimizeToTray'] = self.aToTray.isChecked()

        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=4)

    #Поменять язык программы
    def changeLanguage(self, language):
        #Изменить язык в конфиге
        self.config['lang'] = language

        #Убрать прошлый перевод
        QApplication.instance().removeTranslator(self.translator)

        #Загрузить язык из файла
        if language != 'en':
            self.translator.load(language)
            QApplication.instance().installTranslator(self.translator)  
        
        #Обновить константы с переводом и интерфейс
        LC.retranslate()
        self.retranslateUi(self)

        #Дальше идёт изменение текста всех компонентов

        self.updateLAMPStatus()

        self.btnRestart.setText(LC.restartServices)
        self.trayRestartAction.setText(LC.restartServices)
        self.trayShowAction.setText(LC.show)
        self.trayCloseAction.setText(LC.close)

    #Запустить команду в отдельном потоке
    def runCommand(self, command):
        thread = CommandThread(command)
        thread.finished.connect(self.updateLAMPStatus)
        thread.error.connect(self.logError)
        self.threads.append(thread)
        thread.start()

    #Вывести текст сообщение в консоль и на экран
    def logError(self, e):
        print(e)
        QMessageBox.critical(None, 'Error', str(e))

    #Дейсвие по нажатию кнопки смены языка
    def onLangActionClick(self):
        self.changeLanguage(self.sender().property("lang"))

    #Запустить или остановить службы
    def onBtnStartStopClick(self):
        try:
            if self.btnStartStop.property('active'):
                self.runCommand('sudo systemctl stop apache2')
                self.runCommand("sudo systemctl stop mysql")
            else:
                self.runCommand('sudo systemctl start apache2')
                self.runCommand("sudo systemctl start mysql")

        except subprocess.CalledProcessError as e:
            self.logError(e)

        self.updateLAMPStatus()  


    #Перезапустить службы
    def onBtnRestartClick(self):
        self.runCommand('sudo systemctl restart apache2')
        self.runCommand("sudo systemctl restart mysql")
        self.updateLAMPStatus()  

    #Изменить текст в UI в зависимости от активности служб
    def updateLAMPStatus(self):
        #HTML строки с состояниями

        LBL_STATUS_TEXT = """
            <table width="100%">
                <tr>
                    <td align="left">{}</td>
                    <td align="right">{}</td>
                </tr>
                <tr>
                    <td align="left">{}</td>
                    <td align="right">{}</td>
                </tr>
            </table>
        """

        APACHE2_STATUS_TEXT = LC.status.format("apache2")
        MYSQL_STATUS_TEXT = LC.status.format("mysql")

        #Текст для активной и неактивной служб
        ACTIVE_TEXT = f"<span style='color: green;'>{LC.active}</span>"
        INACTIVE_TEXT = f"<span style='color: red;'>{LC.inactive}</span>"

        #Состояния служб
        apache2_status = self.checkServiceStatus('apache2')
        mysql_status = self.checkServiceStatus('mysql')

        if apache2_status and mysql_status:
            self.btnStartStop.setText(LC.stopServices)
            self.btnStartStop.setProperty('active', True)
            self.btnRestart.setEnabled(True)

            self.trayStartStopAction.setText(LC.stopServices)
            self.trayMenu.insertAction(self.traySeparator, self.trayRestartAction)

            self.trayIcon.setIcon(self.style().standardIcon(QStyle.SP_DialogOkButton))
        else:
            self.btnStartStop.setText(LC.startServices)
            self.btnStartStop.setProperty('active', False)
            self.btnRestart.setEnabled(False)

            self.trayStartStopAction.setText(LC.startServices)
            self.trayMenu.removeAction(self.trayRestartAction)

            self.trayIcon.setIcon(self.style().standardIcon(QStyle.SP_DialogCancelButton))

        #Текст для состояния служб apache2 и mysql
        self.lblStatus.setText(LBL_STATUS_TEXT.format(
            APACHE2_STATUS_TEXT,
            ACTIVE_TEXT if apache2_status else INACTIVE_TEXT, 
            MYSQL_STATUS_TEXT,
            ACTIVE_TEXT if mysql_status else INACTIVE_TEXT
        ))

    #Проверить активна ли служба с указанным названием
    def checkServiceStatus(self, service):
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', service],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.stdout.strip() == 'active'
        except Exception as e:
            self.logError(e)
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
