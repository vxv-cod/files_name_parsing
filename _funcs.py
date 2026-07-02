import uuid
import datetime
from functools import wraps
import inspect
import io
import json
import os
import shutil
import sys
# from typing_extensions import Self
from fastapi import HTTPException
from functools import wraps
from time import time
from typing import Self, Any, Callable, Type

# from docx.document import Document
from fastapi import UploadFile
from fastapi.responses import FileResponse, StreamingResponse


# from src.utils._loguru_log import logger
from ._loguru_log import logger
# from rich import print



def timer_(func):
    '''Время выполнения'''
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time()
        res =  await func(*args, **kwargs)
        logger.info(f'"{func.__name__}" : {round(time() - start_time, 8)} sec')
        return res
    return wrapper


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, (uuid.UUID, bytes)):
        return str(obj)
    raise TypeError ("Type %s not serializable" % type(obj))


def write_json(data, file_name):
    '''Запись объектов Python в файл json'''
    with open(f'{file_name}', 'w', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2, default=json_serial)


def read_txt(file_name):
    '''Чтение из файла txt, ini'''
    with open(file_name, 'r', encoding='utf-8') as fp:
        return fp.readlines()


def read_json(file_name):
    '''Чтение из файла json'''
    print(f"{file_name = }")
    with open(file_name, 'r', encoding='utf-8') as fp:
        return json.load(fp)


async def async_write_json(data, file_name):
    return  write_json(data, file_name)


async def async_read_json(file_name):
    # return  read_json(file_name)
    with open(file_name, 'r', encoding='utf-8') as fp:
        return json.load(fp)    


def read_py(file_name):
    '''Чтение из файла'''
    with open(file_name) as file:
        return file.read()


def write_py(data, file_name):
    '''Запись объектов в файл Python'''
    with open(file_name + ".py", "w") as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=2))



def int_to_datetime(epoch_seconds: int, tz=datetime.timezone.utc) -> datetime.datetime:
    ''' «Нормальный» тайм‑стамп (секунды от 1 января 1970) '''
    return datetime.datetime.fromtimestamp(epoch_seconds, tz)


def string_to_datetime(string: str, format: str = '%Y-%m-%d %H:%M:%S') -> datetime.datetime:
    # ''' Преобразуем dateime в строку 
    ''' Преобразуем строку в dateime
    format_example = %d.%m.%Y %H:%M:%S '''
    return datetime.datetime.strptime(string, format)


def datetime_to_string(date_time: datetime.datetime, format: str = '%Y-%m-%d %H:%M:%S') -> str:
    ''' Преобразуем dateime в строку 
    format_example = %Y-%m-%d %H:%M:%S '''
    return date_time.strftime(format)


def datetime_to_int(date_time: datetime.datetime) -> int:
    ''' «Нормальный» тайм‑стамп (секунды от 1 января 1970) '''
    return round(date_time.timestamp())


def find_classes(base_module_name, find_attr = "__tablename__"):
    '''Сбор всех классов в импортированных модулях'''
    clases = {}
    base_module = sys.modules[base_module_name]
    for base_attr in dir(base_module):
        '''# каждый атрибута'''
        parrent_attr = getattr(base_module, base_attr)
        '''# проверяем тип модуль'''
        if inspect.ismodule(parrent_attr):
            for name in dir(parrent_attr):
                attr = getattr(sys.modules[parrent_attr.__name__], name)
                # print(attr.__dict__)
                '''# перебрав все атрибуты ищем только классы с нужным атрибутом'''
                if inspect.isclass(attr) and attr.__dict__.get(find_attr, False):
                    clases[attr.__tablename__] = attr
    # print(clases)
    return clases

        
def save_file(fullname: str, file: UploadFile):
    dirname = os.path.dirname(fullname)
    if not os.path.isdir(dirname): 
        os.makedirs(dirname, exist_ok=True)  # Создаём структуру каталогов
    with open(fullname, "wb") as wf:
        wf.write(file.file.read())
        # shutil.copyfileobj(file.file, wf)
        file.file.close() # удалаяет временный
    

def delete_file(path):
    '''Удаление файла по полному его пути'''
    filename = os.path.basename(path)
    if os.path.isfile(path):
        os.remove(path)
        return True
    else:
        logger.error(f"Файл {filename} не существует по указанному пути")
        return False



# def decor_try_to_exept(func):
#     '''Декоратор для контекстного менеджера'''
#     # @cache(expire=30)
#     @wraps(func)
#     async def wrapper(self: Self, *args, **kwargs):
#         try:
#             return await func(self, *args, **kwargs)
#         except Exception as e:
#             logger.error(e)
#             raise HTTPException(status_code=500, detail = e)
#     return wrapper   


# async def unloading_docx_stream_from_io(filename: str, doc: Document):
#     '''Отправляем по стриму налету созданный файл docx'''
#     '''Заголовок ответа с указанием способа отображения после загрузки и имени файла'''
#     # headers = {'Content-Disposition': f'inline; filename="{filename}"'}
#     headers = {'Content-Disposition': f'attachment; filename="{filename}.docx"'}
#     '''Создание буфера обмена'''
#     buffer = io.BytesIO()
#     '''Сохранение документа в буфер обмена'''
#     doc.save(buffer)
#     buffer.seek(0)

#     '''Способ сохранения в темп-файл'''
#     import tempfile
#     with tempfile.NamedTemporaryFile(mode="w+b", suffix=".docx", delete=False) as temp_file:
#         temp_file.write(buffer.getvalue())
#     response = FileResponse(temp_file.name, headers=headers)
    
#     '''2ой способ выгрузки'''
#     # return FileResponse(buffer, headers=headers, media_type="application/docx" )        
#     return StreamingResponse(content=buffer, headers=headers, media_type="application/docx")
