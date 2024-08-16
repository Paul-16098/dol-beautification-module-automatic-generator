from .init import *

# i18n
import json
import locale
from pathlib import Path
from enum import Enum


class I18n:
    """A i18n module
    By Paul-16098
    """

    ver = "1.0.0.0"

    def __init__(self) -> None:
        """LANGS"""
        self._DIR_ROOT: Path = Path(__file__).parent
        self._DIR_LANGS_ROOT: Path = self._DIR_ROOT / "langs"

        self._SYS_LANG: str = (locale.getdefaultlocale()[
                               0]).lower()  # type: ignore
        self._SYS_LANG_FILE: Path = self._DIR_LANGS_ROOT / \
            f"{self._SYS_LANG}.json"
        self._EN_US_LANG_FILE: Path = (
            self._SYS_LANG_FILE
            if self._SYS_LANG_FILE.exists()
            else self._DIR_LANGS_ROOT / "en_us.json"
        )
        # self.__logger_obj.write_log(
        #     f"SYS_LANG: {self._SYS_LANG}", type_="info")
        if self._SYS_LANG_FILE.exists():
            with open(self._SYS_LANG_FILE, "r", encoding="utf-8") as fp:
                self._LANGS = json.load(fp)
        else:
            # self.__logger_obj.write_log("No SYS_LANG_FILE", type_="warn")
            self._LANGS = {}
        if self._EN_US_LANG_FILE.exists():
            with open(self._DIR_LANGS_ROOT / "en_us.json", "r", encoding="utf-8") as fp:
                self._DEFAULT_LANGS = json.load(fp)
        else:
            # self.__logger_obj.write_log("No EN_US_LANG_FILE", type_="warn")
            self._DEFAULT_LANGS = {}

        self._DEFAULT_LANGS.update(self._LANGS)
        self._LANGS = self._DEFAULT_LANGS
        del self._DEFAULT_LANGS
        # inspect(self, all=True)

    class Langs(Enum):
        # sys
        updata = 0
        any = 1
        file_lang = 2
        # sys end
        # {file_name}__{class_name}__{func_name}__{id}

        pass

    def locale(self, raw: str | Langs, *kwargs):
        """get lang text

        Args:
            raw (str | Langs): `Langs.XXX` or `"{file_name}__{class_name}__{func_name}__{id}"`

        Returns:
            _type_: lang text
        """
        text = raw.name if isinstance(raw, self.Langs) else raw
        return str(self._LANGS.get(text, f"[no `{text}` in `en_us.json`]")).format(
            *kwargs
        )
