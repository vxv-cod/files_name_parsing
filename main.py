import json
import os
import pathlib
import shutil
from openpyxl import load_workbook, Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.drawing.image import Image
from openpyxl.drawing.spreadsheet_drawing import AnchorMarker, OneCellAnchor, AnchorMarker, AbsoluteAnchor
from openpyxl.drawing.xdr import XDRPositiveSize2D, XDRPoint2D
from openpyxl.utils.units import pixels_to_EMU, cm_to_EMU
from PyQt5 import QtWidgets
from loguru import logger

from rich import print

from okno_ui import Ui_Form
from service import Signals, parse_directory, File_class
from _table_to_excel import db_xlxs


constructivs = ["фасад", "подвал", "ТС", "ЭЛ"]

def is_folder(Fullfilename, text):
    '''Проверка существуют ли указанные папки'''
    if os.path.exists(Fullfilename) == False:
        raise FileNotFoundError(text)

class Signature_class(File_class):
    surname: str
    initials: str

# class Cell_class:
#     row: int
#     col: int
#     value: str
#     initials: str
#     surname: str
#     initials: str


class Column:
    def __init__(self, names: str, labels: str):
        self.name = names
        self.label = labels
    # names: str
    # labels: str


# columns = [
#     Column(name="filename", label="Имя файла"),
#     Column(name="address", label="Адрес"),
#     Column(name="type_constr", label="Тип конструкции")
# ]

columns = [
    {"name": "filename", "label": "Имя файла"},
    {"name": "address", "label": "Адрес"},
    {"name": "type_constr", "label": "Тип работ"},
    {"name": "plan_god", "label": "Плановый год ремонта"},
    {"name": "opisanie", "label": "Описание"},
]

def go(sig: Signals, ui: Ui_Form, Form):
    # Сбор данных из интерфейса
    directory = ui.plainTextEdit.toPlainText()
    
    # Проверка данных
    is_folder(directory, "Папка со сметами указана не корректно !!!")

    # Сбор данных по исходным файлам
    files: list[File_class] = parse_directory(directory)

    # Дополняем полями с фамилией и инициалами
    
    # # Создание папки для Результатов
    # result_folder = directory.rsplit("\\", 1)[0] + "\\Result"

    # try:
    #     os.mkdir(result_folder)
    # except:
    #     try:
    #         shutil.rmtree(result_folder)
    #     except FileNotFoundError:
    #         return print("Адресс не найден ! ! !")
    #     os.mkdir(result_folder)
        
    sig.signal_Probar.emit(ui.progressBar_1, 0)

    count_files = len(os.listdir(path=directory))
    rows = []
    
    for index_, file in enumerate(files, 1):
        filename = file.stem
        spl = filename.split()
        address = " ".join(filename.split()[3 : -1]).strip().strip(",")
        type_constr = spl[-1]
        row = {
            "filename": filename + file.suffix,
            "address": address,
            "type_constr": type_constr,
            "plan_god": "",
            "opisanie": ""
        }
        rows.append(row)
        procwnt = int((index_)*100 / count_files)
        text = f"Обработка файлов: {index_} из {count_files} ({procwnt:.2f}%)"
        # import time
        # time.sleep(1)
        sig.signal_Probar.emit(ui.progressBar_1, procwnt)
        sig.signal_label.emit(ui.label, text)
        
    
    sig.signal_label.emit(ui.label, "Сохраняем данные в файл 'Сводная ведомость.xlsx' ...")
    db_xlxs("Сводная ведомость", directory, columns, rows)
    sig.signal_Probar.emit(ui.progressBar_1, 100)
        





if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    directory = r"C:\Users\vxv\Documents\vxvPy\Work\AntonBikov\Задание\Без КС 3"

    sig = Signals()
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()

    directory = r"C:\Users\vxv\Documents\vxvPy\Work\AntonBikov\Задание\Без КС 3"
    ui.plainTextEdit.setPlainText(directory)
    go(sig, ui, Form)

    sys.exit(app.exec_())

