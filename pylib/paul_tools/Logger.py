from .init import *

# logger
import os
import colorama
import atexit
import shutil
from typing import Literal
from datetime import datetime
from colorama import Fore

from .I18n import I18n


class Logger:
    """A logger module 
    By Paul-16098
    """
    ver = "2.0.17.0"

    __print = print
    __input = input

    def __str__(self):
        info(self)
        return str(self)

    __repo__ = __str__

    def __init__(self, debug: bool = False, temp_path: str = "temp", log_file: str = "log.log", is_log: bool = False, ignore_errors: bool = False, del_tmp: bool = True):  # 初始化
        """init

        Args:
            debug (bool, optional): if True, the log is not been del. Defaults to False.
            temp_path (str, optional): Temporary path to store log files. Defaults to "temp".
            log_file (str, optional): Log file name. Defaults to "log.log".
            is_log (bool, optional): write in the log files. Defaults to False.
            ignore_errors (bool, optional): ignore errors. Defaults to False.
        """
        try:
            # 初始化 colorama
            colorama.init()
            self.__i18n_obj = I18n()
            self.cofg: dict = dict()
            self.cofg["is_log"] = is_log
            self.cofg["temp_path"] = temp_path
            self.cofg["debug"] = debug
            self.cofg["ignore_errors"] = ignore_errors
            self.cofg["del_tmp"] = del_tmp
            if self.cofg["is_log"]:
                os.makedirs(f'{self.cofg["temp_path"]}', exist_ok=True)
                atexit.register(self.exit)
                self._log_path = os.path.join(
                    self.cofg["temp_path"], log_file)
                self._log_file = open(self._log_path, "a", encoding='utf-8')
            self._closed = False
            self.log_file_name = log_file
            # inspect(self, all=True)

            if self.cofg["debug"]:
                self.print_(f'========= init done=========', type_="info")
                self.print_(f"v{self.ver}", type_="info")
                self.print_(f"cofg: {self.cofg}", type_="info")
            else:
                self.write_log(f'========= init done=========', type_="info")
                self.write_log(f"v{self.ver}", type_="info")
                self.write_log(f"cofg: {self.cofg}", type_="info")
        except Exception as e:
            self.print_(f'init error, {e}', 'error')

    def exit(self) -> None:
        if self.cofg["debug"]:
            self.print_("========= exit =========", type_="info")
        else:
            self.write_log("========= exit =========", type_="info")
        if self.cofg["debug"]:
            self.__print("exit run")
        _ = self.del_tmp()
        if self.cofg["debug"]:
            self.__print(f"del_temp run: {_}")

    def del_tmp(self) -> bool:
        """del all temp

        Returns:
            bool: If successful, return will be equal to True.
        """
        if not self.cofg["del_tmp"]:
            if self.cofg["debug"]:
                self.__print("del_tmp not run")
            return True
        if self.cofg["debug"]:
            self.__print("del_tmp run")
        try:
            if self.cofg["is_log"]:
                self._closed = True
                self._log_file.close()
            else:
                if self.cofg["debug"]:
                    self.print_(
                        self.__i18n_obj.locale("paul_tools__Logger__del_temp__not_call_this"), type_="info")
                else:
                    self.write_log(
                        self.__i18n_obj.locale("paul_tools__Logger__del_temp__not_call_this"), type_="info")
            if not self.cofg["debug"]:
                # if True:
                shutil.rmtree(self.cofg["temp_path"])
                if self.cofg["debug"]:
                    self.__print("rm temp run")
            if self.cofg["is_log"]:
                return True
            else:
                return False
        except Exception as e:
            if self.cofg["ignore_errors"]:
                pass
            else:
                _color, color = self._color(type_="error")
                del _color
                self.__print(color + str(e) + Fore.RESET)
                # os.system(f"rmdir /s /q {self._temp_path}")
            return False

    def write_log(self, message: object = "", type_: str = 'log', type2_=None, z=None, x=None, time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")) -> None:
        """write the log in log files:
        [{time}] [type:{type2_}][{type_}]{
                             z}{x}: {message}\\n

        Args:
            message (object, optional): message. Defaults to "".
            type_ (str, optional): _description_. Defaults to 'log'.
            type2_ (_type_, optional): _description_. Defaults to None.
            z (_type_, optional): _description_. Defaults to None.
            x (_type_, optional): _description_. Defaults to None.
            time (_type_, optional): _description_. Defaults to datetime.now().strftime("%Y-%m-%d %H:%M:%S").
        """
        if self.cofg["debug"]:
            self.__print("write_log run")
        if self.cofg["is_log"] == False:
            return None
        if self._log_file.closed:
            if self._closed == False:
                self.__print(self.__i18n_obj.locale(
                    "paul_tools__Logger__write_log__file_closed", self.log_file_name))
                self._closed = True
                return None
            else:
                return None
        if type2_ == None:
            type2_ = "write_log"
        # TODO: (Paul-16098) 2024-5-13 18:20, UTC+8 done \ --> \\
        message = fr"{message}"

        if self.cofg["debug"] == True:
            self.__print("=====/[write_log debug]=====")
            self.__print("message: ", message)
            self.__print("message.encode: ", message.encode())
            self.__print("message.type: ", type(message))
            self.__print("type: ", type_)
            self.__print("type2:", type2_)
            self.__print("z: ", z)
            self.__print("x: ", x)
            self.__print("=====[write_log debug]/=====\n")
        if z == None:
            z = ""
        if x == None:
            x = ""
        self._log_file.write(f'[{time}] [type:{type2_}][{type_}]{
                             z}{x}: {message}\n')
        self._log_file.flush()
        return None

    def _color(self, type_: str, color: str = "") -> tuple[str | None, str]:
        """Determine the displayed color based on type: str and color: str.

        Args:
            type_ (str): _description_
            color (str, optional): _description_. Defaults to "".

        Returns:
            tuple[str, str]: _description_
        """
        if self.cofg["debug"]:
            self.__print("_color run")
        color = color.upper()
        if color == "":
            if type_ == 'warn':
                color = Fore.YELLOW  # 黃色
                color2 = "[yellow]"
            elif type_ == 'error':
                color = Fore.RED  # 紅色
                color2 = "[red]"
            else:
                color2 = None
        else:
            color2 = color
            color2 = f"[{color2}]"

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
        return color2, color

    def print_(self, values: object = "", type_: str = 'log', color: str = "", _x=None, sep: str = " ", end: str = "\n", file: None = None, flush: Literal[False] = False) -> None:
        """in cmd write log

        Args:
            `values` (object): message. Defaults to `""`.
            `type_` (str, optional): _description_. Defaults to `'log'`.
            color (str, optional): _description_. Defaults to "".
            _x (str, optional): _description_. Defaults to "".
            sep (str | None, optional): _description_. Defaults to " ".
            end (str | None, optional): _description_. Defaults to "\n".
            file (None, optional): _description_. Defaults to None.
            flush (Literal[False], optional): _description_. Defaults to False.
        """
        if self.cofg["debug"]:
            self.__print("print_ run")
        _color, color = self._color(type_=type_, color=color)
        self.write_log(values, type_, "log", _color, x=_x)
        values = fr"{color}{values}{Fore.RESET}"

        self.__print(values, sep=sep, end=end, file=file, flush=flush)

    def input_(self, prompt: object = "", type_: str = 'log', color: str = "", x_=None) -> str:
        """in cmd and log files write log

        Args:
            prompt (object, optional): message. Defaults to "".
            type_ (str, optional): _description_. Defaults to 'log'.
            color (str, optional): _description_. Defaults to "".
            x_ (str, optional): _description_. Defaults to "".

        Returns:
            str: from input return result.
        """
        if self.cofg["debug"]:
            self.__print("input_ run")
        message = prompt
        _color, color = self._color(type_=type_, color=color)

        self.write_log(message, type_, "input", _color, x=x_)
        try:
            _: str = self.__input(
                f'{color}{message}{Fore.RESET}')  # type: ignore
        except KeyboardInterrupt as e:
            _: str = ""
            self.__print()
        self.write_log(_, type_, "input_return")
        return _

    def log_(self, *p) -> None:
        self.print_("not use log_, use print_", 'warn')
        self.print_(*p)
