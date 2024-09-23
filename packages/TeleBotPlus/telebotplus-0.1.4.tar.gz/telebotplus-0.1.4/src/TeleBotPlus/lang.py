import os
from . import HTML
from logging import Logger
from MainShortcuts2 import ms
from typing import *


class Lang:
  """Работа с языками"""

  def __init__(self, path: str = "lang.json"):
    self._prefix = None
    self._suffix = None
    self.path = ms.path.path2str(path, to_abs=True)
    self.load()
    self.reload_categories()

  @property
  def prefix(self) -> Union[None, str]:
    """Префикс для каждого текста"""
    return self._prefix

  @prefix.setter
  def prefix(self, v):
    if v is None:
      self._prefix = None
    if type(v) == tuple:
      v = self.get(*v)
    if type(v) == dict:
      if ("category" in v) and ("name" in v):
        v = self.get(**v)
      else:
        v, allow_cache = HTML.from_dict(v)
    self._prefix = v

  @property
  def suffix(self) -> Union[None, str]:
    """Суффикс для каждого текста"""
    return self._suffix

  @suffix.setter
  def suffix(self, v):
    if v is None:
      self._suffix = None
    if type(v) == tuple:
      v = self.get(*v)
    if type(v) == dict:
      if ("category" in v) and ("name" in v):
        v = self.get(**v)
      else:
        v, allow_cache = HTML.from_dict(v)
    self._suffix = v

  def reload_categories(self):
    """Создать для каждой категории метод с её названием"""
    def get_wrapper(cat: str):
      def wrapper(name: str, values: Union[Iterable, dict[str, Any]] = {}, lang: dict[str, dict[str, Any]] = None, *, add_prefix: bool = True, add_suffix: bool = True) -> str:
        return self.get(cat, name, values, lang, add_prefix=add_prefix, add_suffix=add_suffix)
      return wrapper
    for cat in self.data:
      if not (cat.startswith("_") or hasattr(self, cat)):
        setattr(self, cat, get_wrapper(cat))

  def load(self, **kw):
    """Загрузить основной языковой файл"""
    if os.path.exists(self.path):
      kw["path"] = self.path
      if not "like_json5" in kw:
        kw["like_json5"] = False
      self.data: dict[str, dict[str, Any]] = ms.json.read(**kw)
    else:
      self.data: dict[str, dict[str, Any]] = {}
    self.cache = {}

  def save(self, **kw):
    """Сохранить основной языковой файл"""
    self.data["_format"] = "TeleBotPlus.lang"
    kw["data"] = self.data
    kw["path"] = self.path
    ms.json.write(**kw)

  def build_cache(self):
    """Построить кеш для всех языков"""
    for category in self.data:
      if not category.startswith("_"):
        for name in self.data[category]:
          text, allow_cache = HTML.from_dict(self.data[category][name])
          if allow_cache:
            self.cache[category, name] = text

  def get(self, category: str, name: str, values: Union[str, list, tuple, dict[str, Any]] = {}, lang: dict[str, dict[str, Any]] = None, *, add_prefix: bool = True, add_suffix: bool = True) -> str:
    """Получить отформатированный текст"""
    result = ""
    if not self.prefix is None:
      if add_prefix:
        result += self.prefix
    result += self._get(category, name, values, lang)
    if not self.suffix is None:
      if add_suffix:
        result += self.suffix
    return result

  def _get(self, category: str, name: str, values: Union[str, list, tuple, dict[str, Any]] = {}, lang: dict[str, dict[str, Any]] = None) -> str:
    v = values
    if type(values) in [list, tuple]:
      v = []
      for i in values:
        if type(i) == str:
          v.append(HTML.normal(i))
        else:
          v.append(i)
    if type(values) == dict:
      v = {}
      for i, obj in values.items():
        if type(obj) == str:
          v[i] = HTML.normal(obj)
        else:
          v[i] = obj
    if type(values) == str:
      v = HTML.normal(values)
    if not lang is None:
      if category in lang:
        if name in lang[category]:
          text, allow_cache = HTML.from_dict(lang[category][name])
          return text % v
    if not (category, name) in self.cache:
      text, allow_cache = HTML.from_dict(self.data[category][name])
      if allow_cache:
        self.cache[category, name] = text
      return text % v
    return self.cache[category, name] % v


Path = ms.path.Path


class _MultiLang_base:
  def __enter__(self):
    return self

  def __exit__(self, type, value, trace):
    pass


class _MultiLang_cat(_MultiLang_base):
  def __init__(self, root, lang, cat):
    self.cat: str = cat
    self.lang: Union[str, None] = lang
    self.root: MultiLang = root

  def __call__(self, name: str, values: Union[dict, Iterable] = None, *, add_prefix: bool = None, add_suffix: bool = None, **kw) -> str:
    """Получить готовый HTML текст"""
    kw["add_prefix"] = add_prefix
    kw["add_suffix"] = add_suffix
    kw["cat"] = self.cat
    kw["lang"] = self.lang
    kw["name"] = name
    kw["values"] = values
    return self.root.get(**kw)


class _MultiLang_lang(_MultiLang_base):
  def __init__(self, root, lang):
    self.cache = {}
    self.lang: Union[str, None] = lang
    self.root: MultiLang = root

  def __call__(self, cat: str) -> _MultiLang_cat:
    """Получить указанную категорию"""
    if not cat in self.cache:
      self.cache[cat] = _MultiLang_cat(self.root, self.lang, cat)
    return self.cache[cat]


class MultiLang(_MultiLang_base):
  """Работа с несколькими языками в разных файлах"""

  def __init__(self, main_lang: str, other_langs: dict[str, str] = {}, logger: Logger = None):
    self.cache = {"langs": {}, "texts": {}}
    self.log: Union[None, Logger] = logger
    self.main_lang_path: Path = Path(main_lang)
    self.other_langs_path: dict[str, Path] = {}
    self.prefix: str = None
    self.suffix: str = None
    for k, v in other_langs.items():
      self.other_langs_path[k] = Path(v)
    self.load()

  def _index(self, k: Union[dict, list, str, tuple]) -> tuple[Union[None, str], Union[None, str], Union[None, str]]:
    """lang,cat,name"""
    lang, cat, name = None, None, None
    type_k = type(k)
    if type_k == dict:
      lang = k.get("lang")
      cat = k.get("cat")
      name = k.get("name")
    if type_k == str:
      lang = k
    if type_k in [list, tuple]:
      lang = k[0]
      len_k = len(k)
      if len_k > 1:
        cat = k[1]
        if len_k > 2:
          name = k[2]
          if len_k > 3:
            raise ValueError("There may be a maximum of 3 values, given %i" % len_k)
    return lang, cat, name

  def __call__(self, lang: Union[None, str] = None) -> _MultiLang_lang:
    """Получить указанный язык"""
    if not lang in self.cache["langs"]:
      self.cache["langs"][lang] = _MultiLang_lang(self, lang)
    return self.cache["langs"][lang]

  def __coitains__(self, k) -> bool:
    lang, cat, name = self._index(k)
    if cat is None:
      return lang in self.langs
    if lang in self.langs:
      if name is None:
        return cat in self.langs[lang]
      if cat in self.langs[lang]:
        return name in self.langs[lang][cat]
    return False

  def __delitem__(self, k):
    lang, cat, name = self._index(k)
    if cat is None:
      del self.langs[lang]
    else:
      if name is None:
        del self.langs[lang][cat]
      else:
        del self.langs[lang][cat][name]

  def __getitem__(self, k) -> Union[dict, str]:
    lang, cat, name = self._index(k)
    if cat is None:
      return self.langs[lang]
    if name is None:
      return self.langs[lang][cat]
    return self.langs[lang][cat][name]

  def __setitem__(self, k, v):
    lang, cat, name = self._index(k)
    if cat is None:
      self.langs[lang] = dict(v)
      return
    if name is None:
      self.langs[lang][cat] = dict(v)
      return
    self.langs[lang][cat][name] = v

  def load(self, langs: list[str] = None, ignore_errors: bool = False):
    """Загрузить языки из языковых файлов"""
    if langs is None:
      langs = [None] + list(self.other_langs_path.keys())
    self.langs: dict[Union[None, str], dict[str, dict[str, Any]]] = {}
    for i in langs:
      if i is None:
        path = self.main_lang_path.path
      else:
        path = self.other_langs_path[i].path
      try:
        self.langs[i] = ms.json.read(path)["texts"]
      except Exception as err:
        if not self.log is None:
          self.log.exception("Error when loading language %r from file %r", i, path)
        if (not ignore_errors) or (i is None):
          raise

  def save(self, langs: list[str] = None, ignore_errors: bool = False, **kw):
    """Сохранить языки в языковые файлы"""
    if langs is None:
      langs = [None] + list(self.other_langs_path.keys())
    kw["data"] = {}
    kw["data"]["format"] = "TeleBotPlus.MultiLang"
    for i in langs:
      if i is None:
        path = self.main_lang_path.path
      else:
        path = self.other_langs_path[i].path
      try:
        kw["data"]["texts"] = self.langs[i]
        kw["path"] = path
        ms.json.write(**kw)
      except Exception as err:
        if not self.log is None:
          self.log.exception("Error when saving language %r to file %r", i, path)
        if (not ignore_errors) or (i is None):
          raise

  def build_all_cache(self):
    """Пересоздать кеш для всех текстов"""
    self.cache["texts"] = {}
    for lang in self.langs:
      self.cache["texts"][lang] = {}
      for cat in self.langs[lang]:
        self.cache["texts"][lang][cat] = {}
        for name in self.langs[lang][cat]:
          text, allow_cache = HTML.from_dict(self.langs[lang][cat][name])
          if allow_cache:
            self.cache["texts"][lang][cat][name] = text

  def get(self, cat: str, name: str, values: Union[dict, list, str, tuple] = None, *, add_prefix: bool = None, add_suffix: bool = None, lang: Union[None, str] = None) -> str:
    """Получить готовый HTML текст"""
    result = ""
    if (True if add_prefix is None else bool(add_prefix)) and self.prefix:
      result += self.prefix
    result += self._get(cat=cat, lang=lang, name=name, values=values)
    if (True if add_suffix is None else bool(add_suffix)) and self.suffix:
      result += self.suffix
    return result

  def _get(self, *, lang, cat, name, values):
    if not lang in self.cache["texts"]:
      self.cache["texts"][lang] = {}
    if not cat in self.cache["texts"][lang]:
      self.cache["texts"][lang][cat] = {}
    if name in self.cache["texts"][lang][cat]:
      text = self.cache["texts"][lang][cat][name]
    else:
      text = None
      if (lang in self.langs) or (lang is None):
        if (cat in self.langs[lang]) or (lang is None):
          if (name in self.langs[lang][cat]) or (lang is None):
            text, allow_cache = HTML.from_dict(self.langs[lang][cat][name])
            if allow_cache:
              self.cache["texts"][lang][cat][name] = text
    if text is None:
      return self._get(cat=cat, lang=None, name=name, values=values)
    if values is None:
      return text
    v = values
    if type(values) == dict:
      v = {}
      for i, obj in values.items():
        if type(obj) == str:
          v[i] = HTML.normal(obj)
        else:
          v[i] = obj
    if type(values) in [list, tuple]:
      v = []
      for i in values:
        if type(i) == str:
          v.append(HTML.normal(i))
        else:
          v.append(i)
    if type(values) == str:
      v = HTML.normal(values)
    return text % v
