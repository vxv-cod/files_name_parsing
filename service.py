import os
import pathlib
from PyQt5 import QtCore, QtWidgets



class Signals(QtCore.QObject):
    signal_label = QtCore.pyqtSignal(QtWidgets.QWidget, str)
    signal_err = QtCore.pyqtSignal(QtWidgets.QWidget, str)
    signal_bool = QtCore.pyqtSignal(QtWidgets.QWidget, bool)
    signal_Probar = QtCore.pyqtSignal(QtWidgets.QWidget, int)

    def __init__(self, parent=None):
        self.connectionType = QtCore.Qt.ConnectionType.QueuedConnection
        QtCore.QThread.__init__(self, parent)
        self.signal_label.connect(self.on_change_label, self.connectionType)
        self.signal_err.connect(self.on_change_err, self.connectionType)
        self.signal_bool.connect(self.on_change_bool, self.connectionType)
        self.signal_Probar.connect(self.on_change_Probar, self.connectionType)


    def on_change_label(self, s1: QtWidgets.QLabel, s2: str):
        '''Отправляем текст в label'''
        s1.setText(s2)

    def on_change_err(self, s1, s2):
        '''Сообщение об ошибке'''
        QtWidgets.QMessageBox.information(s1, 'Предупреждение ! ! !', s2)

    def on_change_bool(self, el: QtWidgets.QPushButton, s2):
        el.setDisabled(s2)
    
    def on_change_Probar(self, el: QtWidgets.QProgressBar, s):
        el.setValue(s)        


class File_class:
    path: str
    stem: str
    suffix: str


def parse_directory(directory, suffix=".pdf") -> list[File_class]:
    '''Собираем полные пути '''
    res = []
    for root, dirs, files in os.walk(directory):
        if files != []:
            for name in files:
                send_data = File_class()
                path = os.path.join(root, name)
                file = pathlib.Path(path)
                # print(f"File: {file.__dir__()}")
                if file.suffix == suffix:
                    send_data.path = path               # полный путь файла
                    send_data.stem = file.stem          # имя файла без расширения
                    send_data.suffix = file.suffix      # расширение файла
                    # yield send_data
                    res.append(send_data)
    return res