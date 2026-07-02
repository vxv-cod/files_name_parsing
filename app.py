import os
import sys
import threading
import traceback
from PyQt5 import QtCore, QtWidgets, uic
from service import Signals

from loguru import logger

from okno_ui import Ui_Form
import main

_translate = QtCore.QCoreApplication.translate
Title = 'Сбор по именам файлов'

app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QWidget()
ui = Ui_Form()
ui.setupUi(Form)
Form.show()
Form.setWindowTitle(_translate("Form", Title))

'''Подгрузка интерфейса из файла "*.ui" без конвертации в "*.oy" '''
# app = QtWidgets.QApplication(sys.argv)
# ui: QtWidgets.QWidget = uic.loadUi("okno.ui")
# ui.show()
# ui.setWindowTitle(_translate("", Title))
        
sig = Signals()

'''Обертка функции в потопк (декоратор)'''
def thread(my_func1):
    def wrapper():
        threading.Thread(target=my_func1, daemon=True).start()
    return wrapper


def ChangedPT(plainTextEdit: QtWidgets.QPlainTextEdit):
    '''Отслеживаем сигнал в plainTextEdit на изменение данных и удаляем не нужный текст'''
    '''Удаления ненужного текста в plainTextEdit'''
    directory = plainTextEdit.toPlainText()
    if "file:///" in directory:
        xxx = directory.rfind("file:///")
        directory = directory[xxx + 8:]
        try:
            directory = directory.replace("/", "\\")
        except:
            pass
        plainTextEdit.setPlainText(rf"{directory}")

ui.plainTextEdit.textChanged.connect(lambda : ChangedPT(ui.plainTextEdit))


@thread
def startFun():
    '''Запуск алгоритма программы '''
    try:
        sig.signal_bool.emit(ui.pushButton, True)
        sig.signal_label.emit(ui.label, "Обработка данных . . .")
        main.go(sig, ui, Form)
        sig.signal_label.emit(ui.label, "Создан файл 'Сводная ведомость.xlsx'")
    except PermissionError as e:
        logger.error(traceback.format_exc())
        sig.signal_label.emit(ui.label, 'Статус выполнения: Ошибка!!!')
        text = "Ошибка доступа к файлу 'Сводная ведомость.xlsx'\n\nЗакройте файл и повторите попытку"
        sig.signal_err.emit(Form, text)
        
    except Exception as e:
        logger.error(traceback.format_exc())
        sig.signal_err.emit(Form, str(e))
        sig.signal_label.emit(ui.label, 'Статус выполнения: Ошибка!!!')

    sig.signal_bool.emit(ui.pushButton, False)


'''Чистим "plainTextEdit" для отображения текста по умолчанию'''
ui.plainTextEdit.clear()

ui.pushButton.clicked.connect(startFun)

directory = r"C:\Users\vxv\Documents\vxvPy\Work\AntonBikov\Задание\Без КС 3"
ui.plainTextEdit.setPlainText(directory)


if __name__ == "__main__":
    sys.exit(app.exec_())
