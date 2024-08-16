'''init'''
from rich import inspect as info


class list(list):
    def join(self, sep) -> str:
        return str(sep).join(str(item) for item in self)
