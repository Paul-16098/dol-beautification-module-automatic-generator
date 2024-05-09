# -*- coding: utf-8 -*-
import os
from typing import Literal
import colorama
from datetime import datetime
from colorama import Fore
import atexit
import shutil

__all__ = ["logger"]

_print = print
_input = input


class logger:
    """logger mod
    """
    ver = "2.0.10.0"

    def __init__(self, debug: bool = False, temp_path: str = "temp", log_file: str = "log.log", is_log: bool = False, ignore_errors: bool = False):  # 初始化
        """init

        Args:
            debug (bool, optional): if True, the log is not been del. Defaults to False.
            temp_path (str, optional): Temporary path to store log files. Defaults to "temp".
            log_file (str, optional): Log file name. Defaults to "log.log".
            is_log (bool, optional): _description_. Defaults to False.
        """
        try:
            # 初始化 colorama
            colorama.init()
            self._is_log = is_log
            self._temp_path = temp_path
            self._debug = debug
            self._ignore_errors = ignore_errors
            if debug == True:
                self._is_log = True
            if self._is_log == True:
                os.makedirs(f'{self._temp_path}', exist_ok=True)
                atexit.register(self.del_temp)
                self._log_path = os.path.join(self._temp_path, log_file)
                self._log_file = open(self._log_path, "a", encoding='utf-8')
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
            if self._is_log:
                self._closed = True
                self._log_file.close()
                if self._debug == False:
                    shutil.rmtree(self._temp_path)
                return True
            else:
                self.log_(values="is_log is False so not call this", type="warn")
                return False
        except Exception as e:
            if self._ignore_errors:
                pass
            else:
                _color, color = self._color(type="error")
                del _color
                _print(color + str(e) + Fore.RESET)
                # os.system(f"rmdir /s /q {self._temp_path}")
            return False

    def write_log(self, message: object, type: str = 'log', type2=None, z=None, x=None, time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")) -> None:
        """write the log in log files:
        [{datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")}] [type:{type2}][{type}]{z}{x}: {message}\n

        Args:
            message (object): _description_
            type (str, optional): _description_. Defaults to 'log'.
            type2 (_type_, optional): _description_. Defaults to None.
            z (_type_, optional): _description_. Defaults to None.
            x (_type_, optional): _description_. Defaults to None.
        """
        if self._is_log == False:
            return None
        if self._log_file.closed:
            if self._closed == False:
                _print("文件已關閉，無法寫入日誌")
                self._closed = True
                return None
            else:
                return None
        if type2 == None:
            type2 = "write_log"
        if z == None:
            z = ""
        if x == None:
            x = ""
        # todo \ --> \\
        if self._debug == True:
            _print("=====debug=====")
            _print("1: ", message)
            _print("1.encode: ", message.encode())  # type: ignore
            _print("2: ", type)
            _print("3:", type2)
            _print("4: ", z)
            _print("5: ", x)
            _print("=====debug=====")
        self._log_file.write(f'[{time}] [type:{type2}][{type}]{
                             z}{x}: {message}\n')
        self._log_file.flush()
        return None

    def _color(self, type: str, color: str = "") -> tuple[str, str]:
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

            if color == "RED":
                color = Fore.RED  # 紅色
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

    def log_(self, values: object, type: str = 'log', color: str = "", _x: str = "", sep: str | None = " ", end: str | None = "\n", file: None = None, flush: Literal[False] = False) -> None:
        """in cmd and log files write log

        Args:
            message (object): message
            type (str, optional): _description_. Defaults to 'log'.
            color (str, optional): _description_. Defaults to "".
            _x (str, optional): _description_. Defaults to "".
        """
        _color, color = self._color(type=type, color=color)
        values = str(values)
        self.write_log(values, type, "log", _color, x=_x)
        values = color + values + Fore.RESET

        _print(values, sep=sep, end=end, file=file, flush=flush)

    def input_(self, prompt: object = "", type: str = 'log', color: str = "", _x: str = "") -> str:
        """in cmd and log files write log

        Args:
            message (object): message
            type (str, optional): _description_. Defaults to 'log'.
            color (str, optional): _description_. Defaults to "".
            _x (str, optional): _description_. Defaults to "".

        Returns:
            str: from input return result
        """
        message = str(prompt)
        _color, color = self._color(type=type, color=color)

        self.write_log(message, type, "input", _color, x=_x)
        try:
            r: str = _input(color + message + Fore.RESET)
        except KeyboardInterrupt as e:
            r: str = ""
            _print()
        self.write_log(r, type, "input_return")
        return r


def print(*values: object, sep: str | None = " ", end: str | None = "\n", file: None = None,):
    logger_obj = logger(is_log=True, ignore_errors=True)
    logger_obj.log_(*values, _x="[劫持print]", sep=sep,  # type: ignore
                    end=end, file=file)


def input(prompt: object = ""):
    logger_obj = logger(is_log=True, ignore_errors=True)
    return logger_obj.input_(prompt, _x="[劫持input]")  # type: ignore
