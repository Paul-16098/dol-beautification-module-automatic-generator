# coding=utf-8
import os
import colorama
from datetime import datetime
from colorama import Fore
import atexit
import shutil

class logger:
    ver = "1.0.4.0"
    def __init__(self, debug = False, temp_path = 'temp') -> None: # 初始化
        try:
            # 初始化 colorama
            colorama.init()
            self._temp_path = temp_path
            self._debug = debug
            os.makedirs(f'{self._temp_path}', exist_ok=True)
            atexit.register(self.del_temp)
            self._log_path = os.path.join(self._temp_path, 'log.log')
            self._log_file = open(self._log_path, "w", encoding='utf-8')
            self.write_log('========= init done =========')
        except Exception as e:
            self.log_(f'init error, {e}', 'error')
    
    def del_temp(self):
        r"""
        del temp
        """
        try:
            self._log_file.close()
            if self._debug == False:
                shutil.rmtree(self._temp_path)
        except PermissionError as e:
            self.write_log(str(e), type="error")
            # os.unlink(self._temp_path)
        except ValueError as e:
            # self.write_log(str(e), type="error")
            os.unlink(self._temp_path)

    def write_log(self, message: str, type='log', type2 = None, z = None):
        r"""
        write_log: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [type:{type2}][{type}]{z}: {message}\n
        """
        if self._log_file.closed:
            print("文件已關閉，無法寫入日誌")
            return
        if type2 == None:
            type2 = "write_log"
        if z == None:
            z = ""
        # todo \ --> \\
        self._log_file.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [type:{type2}][{type}]{z}: {message}\n')
        self._log_file.flush()
    
    def log_(self, message: str, type='log', color: str = "") -> None:
        color = color.upper()
        if color == "":
            if type == 'warn':
                color = Fore.YELLOW  # 黃色
                _color = "[yellow]"
            elif type == 'error':
                color = Fore.RED  # 紅色
                _color = "[red]"
            else:
                _color = ""
        else:
            _color = color
            _color = f"[{_color}]"
            
            if color=="RED":
                color = Fore.RED # 紅色
            elif color == "YELLOW":
                color = Fore.YELLOW  # 黃色
            elif color == "BLACK":
                color = Fore.BLACK
            elif color == "GREEN":
                color = Fore.GREEN
            elif color == "BLUE":
                color = Fore.BLUE
            elif color == "MAGENTA":
                color = Fore.MAGENTA
            elif color == "CYAN":
                color = Fore.CYAN
            elif color == "WHITE":
                color = Fore.WHITE

        print(color + message + Fore.RESET)
        self.write_log(message, type, "log", _color)

    def input_(self, message: str, type='log', color: str = "") -> str:
        color = color.upper()
        if color == "":
            _color = ""
            if type == 'warn':
                color = Fore.YELLOW  # 黃色
            elif type == 'error':
                color = Fore.RED  # 紅色
        else:
            _color = color
            _color = f"[{_color}]"
            if color=="RED":
                color = Fore.RED # 紅色
            elif color == "YELLOW":
                color = Fore.YELLOW  # 黃色
            elif color == "BLACK":
                color = Fore.BLACK
            elif color == "GREEN":
                color = Fore.GREEN
            elif color == "BLUE":
                color = Fore.BLUE
            elif color == "MAGENTA":
                color = Fore.MAGENTA
            elif color == "CYAN":
                color = Fore.CYAN
            elif color == "WHITE":
                color = Fore.WHITE

        self.write_log(message, type, "input", _color)
        r = input(color + message + Fore.RESET)
        self.write_log(r, type, "input_return")
        return r
