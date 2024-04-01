import os
import colorama
from datetime import datetime
from colorama import Fore
import atexit
import shutil

class log:
    ver = "1.0.0.0"
    def __init__(self, temp_path = 'temp') -> None: # 初始化
        # 初始化 colorama
        colorama.init()
        self.temp_path = temp_path
        os.makedirs(f'{self.temp_path}', exist_ok=True)
        atexit.register(self.del_temp)
        self.log_path=os.path.join(self.temp_path, 'log.log')
        with open(self.log_path, "a", encoding='utf-8') as file:
            file.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [type:init]: done\n')
            
    def del_temp(self):
        shutil.rmtree(self.temp_path)

    def write_log(self, message: str, type='log'):
        with open(self.log_path, "a", encoding='utf-8') as file:
            file.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [type:write_log][{type}]: {message}\n')
    
    def _log(self, message: str, type='log', color: str = "") -> None:
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
            if color=="red":
                color = Fore.RED # 紅色
            elif color == "yellow":
                color = Fore.YELLOW  # 黃色

        print(color + message + Fore.RESET)
        with open(self.log_path, "a", encoding='utf-8') as file:
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
        with open(self.log_path, "a", encoding='utf-8') as file:
            file.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [type:input][{type}]{_color}: {message}\n')
            file.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [type:input_return][{type}]: {r}\n')
        return r
