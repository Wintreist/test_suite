import importlib
import os
import sys

from logging_lib import RootLogger as logger

from test_suite.helpers.path_helpers import path_rel2abs


def get_pythonpath():
    return os.getenv("PYTHONPATH", "")


class updated_pythonpath(object):
    """
    При использовании с with обновляется os.environ['PYTHONPATH'] и sys.path. Сам по себе экземпляр
    класса -- это список os.environ['PYTHONPATH'], обновленный в момент создания self. Это же
    возвращается в as-переменную в коснтрукции with-as.
    """

    def __init__(self, relative_PYTHONPATH=None, absolute_PYTHONPATH=None):
        if relative_PYTHONPATH and not get_pythonpath():
            raise AssertionError("There is no PYTHONPATH")

        if isinstance(relative_PYTHONPATH, str):
            self._relative_PYTHONPATH = [relative_PYTHONPATH]
        elif not relative_PYTHONPATH:
            self._relative_PYTHONPATH = []
        else:
            self._relative_PYTHONPATH = relative_PYTHONPATH

        if isinstance(absolute_PYTHONPATH, str):
            self._absolute_PYTHONPATH = [absolute_PYTHONPATH]
        elif not absolute_PYTHONPATH:
            self._absolute_PYTHONPATH = []
        else:
            self._absolute_PYTHONPATH = absolute_PYTHONPATH

        self._abs_addon_pathes = list(map(path_rel2abs, self._relative_PYTHONPATH))

        self._abs_addon_pathes.extend(self._absolute_PYTHONPATH)

    def __enter__(self):
        self._backup_environ_paths()

        python_path_list = self._envpath_to_list(get_pythonpath())
        new_pythonpath = python_path_list + self._abs_addon_pathes
        os.environ["PYTHONPATH"] = self._list_to_envpath(new_pythonpath)

        sys.path[:] = self._abs_addon_pathes + sys.path
        return self._abs_addon_pathes

    def __exit__(self, type, value, traceback):
        self._restore_environ_paths()

    def _envpath_to_list(self, envpath):
        if not envpath:
            return []
        return list(map(os.path.normpath, envpath.split(os.pathsep)))

    def _list_to_envpath(self, listpath):
        if not listpath:
            return ""
        return os.pathsep.join(listpath)

    def _backup_environ_paths(self):
        self._backup_pythonpath = get_pythonpath()
        self._backup_syspath = list(sys.path)  # make copy!

    def _restore_environ_paths(self):
        os.environ["PYTHONPATH"] = self._backup_pythonpath
        sys.path[:] = self._backup_syspath


def import_module(module_name, relative_path=None, abs_path=None):
    try:
        with updated_pythonpath(relative_PYTHONPATH=relative_path, absolute_PYTHONPATH=abs_path):
            return importlib.import_module(module_name)
    except Exception as ex:
        logger.exception(ex)
        raise


def import_from_module(module_name, object_name, relative_path=None, abs_path=None):
    """
    Импортирует из модуля с именем `module_name` объект с именем `object_name`.

    Получаем список классов из модуля `module_name`, которые необходимо "экспортировать" -- которые
    должны быть доступны для удаленного вызова. В самом модуле список этих классов хранится в
    структуре, имя которой передается в настоящую функцию через `object_name`.

    Эта функция должна вызываться на удаленных машинах, где запущен сервер, предоставляющий методы
    для удаленного запуска. Т.к. она импортирует модуль через `importlib.import_module`, то она
    должна вызываться исключительно в дочерних серверах (не parent_server.py)
    """
    relative_path = relative_path or []
    abs_path = abs_path or []

    try:
        module = import_module(module_name, relative_path, abs_path)
        obj = getattr(module, object_name)
    except Exception as ex:
        msg = "Can't import '{}' from module '{}': {}\n".format(object_name, module_name, ex)
        msg = "  \n".join(
            [
                msg,
                'sys.path = "{}"'.format(sys.path),
                '$PYTHONPATH = "{}"'.format(get_pythonpath()),
                'relative_path = "{}"'.format(relative_path),
                'abs_path = "{}"'.format(abs_path),
            ]
        )
        logger.debug(msg)
        raise ImportError(
            "{}".format(
                msg,
            )
        )

    return obj
