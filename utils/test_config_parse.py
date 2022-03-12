#!/usr/bin/env python
# encoding: utf-8

from argparse import Namespace
import pytest

from .config_parse import args_parse, path_concat, toml_parse


@pytest.mark.parametrize(["params", "result"], [
    (
        ["path"], Namespace(compress=False, key_value=False, output="print",
                            file_path="./parse.output", file=None, search_text=None)
    ),
    (
        ["toml"], Namespace(compress=False, key_value=False, output="print",
                            file_path="./parse.output", path=None, keys=False)
    ),
    (
        ["-c", "toml"], Namespace(compress=True, key_value=False, output="print",
                            file_path="./parse.output", path=None, keys=False)
    ),
    (
        ["-c", "-F", "./xxx", "toml"], Namespace(compress=True, key_value=False, output="print",
                            file_path="./xxx", path=None, keys=False)
    ),

])
def test_args_parse(params: list[str], result: object):
    """
    Test args_parse
    """
    _, parser = args_parse()
    assert parser.parse_args(params) == result


@pytest.mark.parametrize(["target", "src", "path"], [(
    "/home/xx/xx", "/home", ["xx/xx"]
), (
    "/home/xx/xx/xxx/xxx", "/home", ["xx/xx", "xxx/xxx"]
)])
def test_path_concat(target: str, src: str, path: list[str]):
    assert path_concat(src, *path) == target


@pytest.mark.parametrize(["search", "target"], [(
    ".conf", "hello"
), (
    ".path", "/home/xxx"
), (
    ".configs", [{"hello": 1}, {"hello": 2}]
), (
    ".configs[0]", {"hello": 1}
), (
    ".configs[1]", {"hello": 2}
)])
def test_toml_parse(search: str, target: str):
    assert toml_parse('./test_toml.toml', search) == target
