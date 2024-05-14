# -*- coding: utf-8 -*-
# logger
import os
import colorama
import atexit
import shutil
from typing import Literal
from datetime import datetime
from colorama import Fore

# i18n
import json
import locale  # type: ignore
from enum import Enum
from pathlib import Path

__all__ = [
    "Logger",
    "I18n"
]


class Logger:
    """logger module
    """
    ver = "2.0.17.0"

    __print = print
    __input = input

    def __init__(self, debug: bool = False, temp_path: str = "temp", log_file: str = "log.log", is_log: bool = False, ignore_errors: bool = False):  # 初始化
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
            # try:
            #     no_cofg = False
            #     type(self.cofg)
            # except AttributeError as e:
            #     if e == " 'logger' object has no attribute 'cofg'":
            #         no_cofg = True
            #     else:
            #         no_cofg = False
            #     if debug:
            #         _print("e:", e)
            # if no_cofg:
            self.cofg = {}
            self.cofg["is_log"] = is_log
            self.cofg["temp_path"] = temp_path
            self.cofg["debug"] = debug
            self.cofg["ignore_errors"] = ignore_errors
            # if self.cofg["debug"]:
            #     _print("no cofg")
            # else:
            #     if debug:
            #         _print("has cofg")
            # del no_cofg
            if self.cofg["debug"]:
                self.cofg["is_log"] = True
            if self.cofg["is_log"]:
                os.makedirs(f'{self.cofg["temp_path"]}', exist_ok=True)
                atexit.register(self.exit)
                self._log_path = os.path.join(
                    self.cofg["temp_path"], log_file)
                self._log_file = open(self._log_path, "a", encoding='utf-8')
            self._closed = False
            self.log_file_name = log_file
            if self.cofg["debug"]:
                self.log_('========= init done =========', type_="info")
                self.log_(f"v{self.ver}", type_="info")
                self.log_(f"cofg: {self.cofg}", type_="info")
                self.log_(
                    f"SYS_LANG: {self.__i18n_obj._SYS_LANG}", type_="info")
            else:
                self.write_log('========= init done =========', type_="info")
                self.write_log(f"v{self.ver}", type_="info")
                self.write_log(f"cofg: {self.cofg}", type_="info")
                self.write_log(
                    f"SYS_LANG: {self.__i18n_obj._SYS_LANG}", type_="info")
        except Exception as e:
            self.log_(f'init error, {e}', 'error')

    def exit(self) -> None:
        if self.cofg["debug"]:
            self.log_("========= exit =========", type_="info")
        else:
            self.write_log("========= exit =========", type_="info")
        if self.cofg["debug"]:
            self.__print("exit run")
        _ = self.del_temp()
        if self.cofg["debug"]:
            self.__print(f"del_temp run: {_}")

    def del_temp(self) -> bool:
        """del all temp

        Returns:
            bool: If successful, return will be equal to True.
        """
        if self.cofg["debug"]:
            self.__print("del_temp run")
        try:
            if self.cofg["is_log"]:
                self._closed = True
                self._log_file.close()
            else:
                if self.cofg["debug"]:
                    self.log_(
                        self.__i18n_obj.locale(self.__i18n_obj.Langs.paul_tools__Logger__del_temp__not_call_this), type_="info")
                else:
                    self.write_log(
                        self.__i18n_obj.locale(self.__i18n_obj.Langs.paul_tools__Logger__del_temp__not_call_this), type_="info")
                # return False
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

    def write_log(self, message: object, type_: str = 'log', type2_=None, z=None, x=None, time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")) -> None:
        """write the log in log files:
        [{time}] [type:{_type2}][{_type}]{z}{x}: {message}\n

        Args:
            message (object): message
            type_ (str, optional): _description_. Defaults to 'log'.
            type2_ (_type_, optional): _description_. Defaults to None.
            z (_type_, optional): _description_. Defaults to None.
            x (_type_, optional): _description_. Defaults to None.
            time (_type_, optional): _description_. Defaults to datetime.now().strftime("%Y-%m-%d %H:%M:%S").

        Returns:
            None
        """
        if self.cofg["debug"]:
            self.__print("write_log run")
        if self.cofg["is_log"] == False:
            return None
        if self._log_file.closed:
            if self._closed == False:
                self.__print(self.__i18n_obj.locale(
                    self.__i18n_obj.Langs.paul_tools__Logger__write_log__file_closed, self.log_file_name))
                self._closed = True
                return None
            else:
                return None
        if type2_ == None:
            type2_ = "write_log"
        if z == None:
            z = ""
        if x == None:
            x = ""
        # TODO(Paul-16098) 2024-5-13 18:20, UTC+8 done \ --> \\
        message = fr"{message}"

        if self.cofg["debug"] == True:
            self.__print("=====/write_log debug=====")
            self.__print("message: ", message)
            self.__print("message.encode: ", message.encode())
            self.__print("message.type: ", type(message))
            self.__print("type: ", type_)
            self.__print("type2:", type2_)
            self.__print("z: ", z)
            self.__print("x: ", x)
            self.__print("=====write_log debug/=====")
        self._log_file.write(f'[{time}] [type:{type2_}][{type_}]{
                             z}{x}: {message}\n')
        self._log_file.flush()
        return None

    def _color(self, type_: str, color: str = "") -> tuple[str, str]:
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
                color2 = ""
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

    def log_(self, values: object = "", type_: str = 'log', color: str = "", _x: str = "", sep: str | None = " ", end: str | None = "\n", file: None = None, flush: Literal[False] = False) -> None:
        """in cmd and log files write log

        Args:
            values (object): message
            type_ (str, optional): _description_. Defaults to 'log'.
            color (str, optional): _description_. Defaults to "".
            _x (str, optional): _description_. Defaults to "".
            sep (str | None, optional): _description_. Defaults to " ".
            end (str | None, optional): _description_. Defaults to "\n".
            file (None, optional): _description_. Defaults to None.
            flush (Literal[False], optional): _description_. Defaults to False.
        """
        if self.cofg["debug"]:
            self.__print("log_ run")
        _color, color = self._color(type_=type_, color=color)
        values = str(values)
        values = fr"{values}"
        self.write_log(values, type_, "log", _color, x=_x)
        values = color + values + Fore.RESET

        self.__print(values, sep=sep, end=end, file=file, flush=flush)

    def input_(self, prompt: object = "", type_: str = 'log', color: str = "", x_: str = "") -> str:
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
        message = str(prompt)
        message = fr"{prompt}"
        _color, color = self._color(type_=type_, color=color)

        self.write_log(message, type_, "input", _color, x=x_)
        try:
            _: str = self.__input(color + message + Fore.RESET)  # type: ignore
        except KeyboardInterrupt as e:
            _: str = ""
            self.__print()
        self.write_log(_, type_, "input_return")
        return _


class I18n:
    """i18n module
    """
    ver = "1.0.0.0"

    def __init__(self) -> None:
        """ LANGS """
        self._DIR_ROOT: Path = Path(__file__).parent
        self._DIR_LANGS_ROOT: Path = self._DIR_ROOT / "langs"

        self._SYS_LANG: str = (locale.getdefaultlocale()[
            0]).lower()  # type: ignore
        self._SYS_LANG_FILE: Path = self._DIR_LANGS_ROOT / \
            f"{self._SYS_LANG}.json"
        self._EN_US_LANG_FILE: Path = self._SYS_LANG_FILE if self._SYS_LANG_FILE.exists(
        ) else self._DIR_LANGS_ROOT / "en_us.json"
        if self._SYS_LANG_FILE.exists():
            with open(self._SYS_LANG_FILE, "r", encoding="utf-8") as fp:
                self._LANGS = json.load(fp)
        else:
            self._LANGS = {}
        if self._EN_US_LANG_FILE.exists():
            with open(self._DIR_LANGS_ROOT / "en_us.json", "r", encoding="utf-8") as fp:
                self._DEFAULT_LANGS = json.load(fp)
        else:
            self._DEFAULT_LANGS = {}

        # print("SYS_LANG: ", self.SYS_LANG)

    class Langs(Enum):
        # sys
        updata = 0
        any = 1

        # {file_name}__{class_name}__{func}__{id}
        paul_tools__Logger__del_temp__not_call_this = 100
        paul_tools__Logger__write_log__file_closed = 101
        pass

    def locale(self, raw: Langs | str, *kwargs, DEFAULT_LANGS=False):
        # print(raw)
        # print(kwargs)
        text = raw.name if isinstance(raw, self.Langs) else raw  # type: ignore
        # print(text)
        # print(self._LANGS)
        if DEFAULT_LANGS:
            _ = self._DEFAULT_LANGS.get(
                text,
                self._LANGS.get(text, "")
            ).format(*kwargs)
        else:
            _ = self._LANGS.get(
                text,
                self._DEFAULT_LANGS.get(text, "")
            ).format(*kwargs)
        return _


# def print(*values: object, sep: str | None = " ", end: str | None = "\n", file: None = None,):
#     """Prints the values to a stream, or to sys.stdout by default.

# sep
#   string inserted between values, default a space.
# end
#   string appended after the last value, default a newline.
# file
#   a file-like object (stream); defaults to the current sys.stdout.
# flush
#   whether to forcibly flush the stream.
#     """
#     logger_obj = logger(is_log=False, ignore_errors=True)
#     logger_obj.log_(*values, x_="[劫持print]", sep=sep,  # type: ignore
#                     end=end, file=file)


# def input(prompt: object = ""):
#     """Read a string from standard input. The trailing newline is stripped.

# The prompt string, if given, is printed to standard output without a trailing newline before reading input.

# If the user hits EOF (*nix: Ctrl-D, Windows: Ctrl-Z+Return), raise EOFError. On *nix systems, readline is used if available.
#     """
#     logger_obj = logger(is_log=False, ignore_errors=True)
#     return logger_obj.input_(prompt, x_="[劫持input]")  # type: ignore
