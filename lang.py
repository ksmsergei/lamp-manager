from PyQt5.QtCore import QCoreApplication as QA


#Константы с переводом
class LangConstants:
    @classmethod
    def retranslate(cls):
        cls.startServices = QA.translate("main", "Start services")
        cls.stopServices = QA.translate("main", "Stop services")
        cls.restartServices = QA.translate("main", "Restart services")
        
        cls.show = QA.translate("tray", "Show")
        cls.close = QA.translate("tray", "Close")

        cls.status = QA.translate("status", "Status of <b>{}</b>: ")
        cls.active = QA.translate("status", "active")
        cls.inactive = QA.translate("status", "inactive")