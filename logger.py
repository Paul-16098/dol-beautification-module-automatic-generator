# coding=utf-8
import os
import colorama
from datetime import datetime
from colorama import Fore
import atexit
import shutil

class logger:
    ver = "1.0.7.1"
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
            self.write_log(str(e), type="error")
            raise e

    def write_log(self, message: object, type: str = 'log', type2 = None, z = None) -> None:
        """write the log in log files:
        {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [type:{type2}][{type}]{z}: {message}\n
        
        Args:
            message (object): message
            type (str, optional): _description_. Defaults to 'log'.
            type2 (_type_, optional): _description_. Defaults to None.
            z (_type_, optional): _description_. Defaults to None.
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
    
    def log_(self, message: object, type: str = 'log', color: str = "") -> None:
        """in cmd and log files write log

        Args:
            message (object): message
            type (str, optional): _description_. Defaults to 'log'.
            color (str, optional): _description_. Defaults to "".
        """
        message = str(message)
        _color, color = self._color(type = type, color = color)

        print(color + message + Fore.RESET)
        self.write_log(message, type, "log", _color)

    def input_(self, message: object, type: str = 'log', color: str = "") -> str:
        """in cmd and log files write log

        Args:
            message (object): message
            type (str, optional): _description_. Defaults to 'log'.
            color (str, optional): _description_. Defaults to "".

        Returns:
            str: from input return result
        """
        message = str(message)
        _color, color = self._color(type = type, color = color)

        self.write_log(message, type, "input", _color)
        r = input(color + message + Fore.RESET)
        self.write_log(r, type, "input_return")
        return r
