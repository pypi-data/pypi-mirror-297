import os
from . import HTML
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


class MultiLang:
  """В разработке"""
  pass
