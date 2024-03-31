import os
import colorama
from datetime import datetime
from colorama import Fore

class c_log:
    ver = "1.0.0.0"
    def __init__(self) -> None:
        # 初始化
        # 初始化 colorama
        colorama.init()
        self.temp = "temp"
        os.makedirs(f'{self.temp}', exist_ok=True)
        if os.path.exists(f"{self.temp}/log.log") is not False: # 如果存在
            os.remove(f"{self.temp}/log.log") # 刪除

    def _log(self, message: str, type='log', color: str = "") -> None:
        if color == "":
            if type == 'warn':
                color = Fore.YELLOW  # 黃色
                _color = "yellow"
            elif type == 'error':
                color = Fore.RED  # 紅色
                _color = "red"
            else:
                _color = ""
        else:
            _color = color
            _color = f"[{_color}]"
            if color=="red":
                color = Fore.RED # 紅色
            elif color == "yellow":
                color = Fore.YELLOW  # 黃色

        print(color + message + Fore.RESET)

        with open(f"{self.temp}/log.log", "a", encoding='utf-8') as file:
            file.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [type:log][{type}]{_color}: {message}\n')

    def _input(self, message: str, type='log', color: str = "") -> str:
        if color == "":
            _color = ""
            if type == 'warn':
                color = Fore.YELLOW  # 黃色
            elif type == 'error':
                color = Fore.RED  # 紅色
        else:
            _color = color
            _color = f"[{_color}]"
            if color=="red":
                color = Fore.RED # 紅色
            elif color == "yellow":
                color = Fore.YELLOW  # 黃色

        r = input(color + message + Fore.RESET)

        with open(f"{self.temp}/log.log", "a", encoding='utf-8') as file:
            file.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [type:input][{type}]{_color}: {message}\n')
            file.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [type:input_return][{type}]: {r}\n')

        return r
