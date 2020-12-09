import os
from typing import Callable, Any, Mapping, List

import javalang
from javalang.parser import JavaSyntaxError
from javalang.tree import CompilationUnit

from ..utils import yield_file_filter, load_text_file


def _is_java_file(path: str):
    return os.path.exists(path) and os.path.isfile(path) and path.lower().endswith('.java')


def _default_error_processor(path: str, err: JavaSyntaxError):
    raise err


def yield_java_file(path: str):
    return yield_file_filter(path, _is_java_file)


def parse_java_in_path(path: str, on_error: Callable[[str, JavaSyntaxError], Any] = None) \
        -> Mapping[str, List[CompilationUnit]]:
    _results = {}
    for _file in yield_java_file(path):
        try:
            root_node = javalang.parser.parse(load_text_file(_file))
        except JavaSyntaxError as err:
            (on_error or _default_error_processor)(_file, err)
        else:
            package_name = root_node.package.name if root_node.package else ''
            _current_package_info = _results.get(package_name, [])
            _current_package_info.append(root_node)
            _results[package_name] = _current_package_info

    return _results
