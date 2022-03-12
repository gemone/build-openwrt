#!/usr/bin/env python
# encoding: utf-8

import os
import json
import argparse
from typing import Literal, Optional
import toml
from pydash import get


OUTPUT_METHOD = Literal["file", "print"]


def toml_parse(file: str, search: str) -> object:
    configs = toml.load(file)
    return get(configs, search)


def kv_output(key: str, value: object) -> str:
    v = json.dumps(value);
    return "{key}={value}".format(key=key, value=v)


def path_concat(path: str, *paths: str) -> str:
    result = os.path.join(path)
    for p in paths:
        result = os.path.join(result, p)

    return result


def args_parse():
    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers()

    path_concat = sub_parser.add_parser('path', help="Path splicing.")
    toml_parse = sub_parser.add_parser('toml', help="Toml Parse.")

    path_concat.add_argument('-f', '--file', type=str,
                             help="Specify the path to a file.")
    path_concat.add_argument('-t', '--search-text',
                             type=str, help="Specify the path to a file.")

    toml_parse.add_argument("-p", "--path", action="append",
                            help="Add directory path. like -p path/ -p xx/path")
    toml_parse.add_argument(
        "-k", "--keys", action="store_true", help="Use Kyes output")

    parser.add_argument("-c", "--compress",
                        action="store_true", help="Compress output.")
    parser.add_argument("-K", "--key-value", action="store_true", help="")
    parser.add_argument("-o", "--output", choices=[
                        "file", "print"], default="print", help="Output mode, support to file or print.")
    parser.add_argument("-F", "--file-path", default="./parse.output",
                        help="When -- output is specified as file, the file path needs to be specified.")

    args = parser.parse_args()

    return (args, parser)


def output_handler(method: OUTPUT_METHOD, output: str, file_path: Optional[os.PathLike[str]]):
    def output_print():
        print(output)

    def output_file():
        if (file_path == None):
            # 路径若为空，则不输出
            return

        with open(file_path, 'a') as f:
            f.write(output)

    switch = {
        "file": output_file(),
        "print": output_print()
    }

    handler = switch.get(method, None)
    if (handler == None):
        return

    handler()


def output_compress(output: object) -> str:
    print(str(output))
    return ''


def handler():
    args, _ = args_parse()


if __name__ == "__main__":
    arsgs, _ = args_parse()
