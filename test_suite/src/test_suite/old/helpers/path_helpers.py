import os

from logging_lib import RootLogger


class PathHelperLogger(RootLogger):
    level = "info"


logger = PathHelperLogger


def paths_to(path):
    """
    Возвращает абсолютный и относительный пути к файлу/директории `path` и имя этого файлового
    объекта.

    :returns: (abs_path, rel_path, name)
    """
    abs_path, name = os.path.split(os.path.abspath(path))
    return abs_path, path_abs2rel(abs_path), name


def get_pythonpaths():
    return list(dict.fromkeys(os.environ["PYTHONPATH"].split(os.pathsep)))


def base_of_path(path):
    path = os.path.abspath(path)
    r = []
    for python_path in get_pythonpaths():
        python_path_abs = os.path.abspath(python_path)

        if os.name != "nt" and os.path.relpath(path.lower(), python_path_abs.lower()).startswith(".."):
            continue

        if path.lower().startswith(python_path_abs.lower()):
            r.append(python_path)

    if not r:
        raise FileExistsError(f'The base path of "{path}" does not exist in the PYTHONPATH: {get_pythonpaths()}')

    if len(r) > 1:
        logger.warning(
            f"Target path: '{path}'\nThere are several paths that can be used as a base path from PYTHONPATH:\n{r}\nSo we use the first one: '{r[0]}'"
        )

    return r[0]


def path_abs2rel(path):
    """
    Преобразует абсолютный путь в относительный. Точка отсчета -- `PYTHONPATH`,
    который ссылается на `os.environ['PYTHONPATH']`.
    """
    path = os.path.abspath(path)
    rel = os.path.relpath(path, base_of_path(path))
    return rel


def path_rel2abs(rel_path):
    assert rel_path != ".", "Can't find . in PYTHONPATH"
    logger.debug(f"rel_path1: {rel_path}")
    rel_path = os.path.relpath(rel_path)
    logger.debug(f"rel_path2: {rel_path}")
    python_paths = get_pythonpaths()
    logger.debug(f"python_paths: {python_paths}")
    abs_paths = [os.path.join(python_path, rel_path) for python_path in python_paths]
    exists_abs_paths = [path for path in abs_paths if os.path.exists(path)]
    assert len(exists_abs_paths) == 1, (exists_abs_paths, python_paths, rel_path)
    return exists_abs_paths.pop()


def path_abs2import(path):
    relpath = path_abs2rel(path)
    result = relpath.replace(os.sep, ".")
    if result.endswith(".py"):
        result = result.rsplit(".py", 1)[0]
    if result.endswith(".pyc"):
        result = result.rsplit(".py", 1)[0]
    return result


def get_module_abs_path(module):
    try:
        module_path = module.__file__
    except AttributeError:
        raise Exception("Module {} does not have __file__ defined".format(module))
    else:
        if module_path.endswith(".pyc") and os.path.exists(module_path[:-1]):
            module_path = module_path[:-1]
    return os.path.abspath(module_path)
