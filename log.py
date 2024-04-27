# -*- coding: utf-8 -*-
import os
import colorama
from datetime import datetime
from colorama import Fore
import atexit
import shutil

ver = "2.0.3.0"

__all__ = ["logger"]

_input = input
_print = print

class logger:
    def __init__(self, debug: bool = False, temp_path: str = "temp", log_file: str = "log.log") -> None: # 初始化
        """init

        Args:
            debug (bool, optional): if True, the log is not been del. Defaults to False.
            temp_path (str, optional): Temporary path to store log files. Defaults to "temp".
            log_file (str, optional): Log file name. Defaults to "log.log".
        """
        try:
            # 初始化 colorama
            colorama.init()
            self._temp_path = temp_path
            self._debug = debug
            os.makedirs(f'{self._temp_path}', exist_ok=True)
            atexit.register(self.del_temp)
            self._log_path = os.path.join(self._temp_path, log_file)
            self._log_file = open(self._log_path, "w", encoding='utf-8')
            self._closed = False
            self.write_log('========= init done =========')
        except Exception as e:
            self.log_(f'init error, {e}', 'error')
    
    def del_temp(self) -> bool:
        """del all temp

        Raises:
            e: all error

        Returns:
            bool: If successful, return will be equal to True.
        """
        try:
            self._log_file.close()
            if self._debug == False:
                shutil.rmtree(self._temp_path)
            return True
        except Exception as e:
            self.log_(str(e), type="error")
            os.system(f"rmdir /s /q {self._temp_path}")
            return False

    def write_log(self, message: object, type: str = 'log', type2 = None, z = None, x = None) -> None:
        """write the log in log files:
        {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [type:{type2}][{type}]{z}{x}: {message}\n

        Args:
            message (object): _description_
            type (str, optional): _description_. Defaults to 'log'.
            type2 (_type_, optional): _description_. Defaults to None.
            z (_type_, optional): _description_. Defaults to None.
            x (_type_, optional): _description_. Defaults to None.
        """
        if self._log_file.closed:
            if self._closed == False:
                _print("文件已關閉，無法寫入日誌")
                self._closed = True
                return
        if type2 == None:
            type2 = "write_log"
        if z == None:
            z = ""
        if x == None:
            x = ""
        # todo \ --> \\
        self._log_file.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [type:{type2}][{type}]{z}{x}: {message}\n')
        self._log_file.flush()
    
    def _color(self, type: str, color: str) -> tuple[str, str]:
        """Determine the displayed color based on type: str and color: str.

        Args:
            type (str): _description_
            color (str, optional): _description_.

        Returns:
            tuple[str, str]: _description_
        """
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
        return _color, color
    
    def log_(self, message: object, type: str = 'log', color: str = "", _x: str = "") -> None:
        """in cmd and log files write log

        Args:
            message (object): message
            type (str, optional): _description_. Defaults to 'log'.
            color (str, optional): _description_. Defaults to "".
            _x (str, optional): _description_. Defaults to "".
        """
        message = str(message)
        _color, color = self._color(type = type, color = color)

        _print(color + message + Fore.RESET)
        self.write_log(message, type, "log", _color, x=_x)

    def input_(self, message: object, type: str = 'log', color: str = "", _x: str = "") -> str:
        """in cmd and log files write log

        Args:
            message (object): message
            type (str, optional): _description_. Defaults to 'log'.
            color (str, optional): _description_. Defaults to "".
            _x (str, optional): _description_. Defaults to "".

        Returns:
            str: from input return result
        """
        message = str(message)
        _color, color = self._color(type = type, color = color)

        self.write_log(message, type, "input", _color, x=_x)
        r = _input(color + message + Fore.RESET)
        self.write_log(r, type, "input_return")
        return r

logger_obj = logger()

def print(*values: object) -> None:
    logger_obj.log_(values, _x="[劫持print]")

def input(*values: object) -> str:
    return logger_obj.input_(values, _x="[劫持input]")
