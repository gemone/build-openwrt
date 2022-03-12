#!/usr/bin/env python
# encoding: utf-8

import os
import json
import argparse
from typing import Literal
import toml
from pydash import get, keys, is_string


OUTPUT_METHOD = Literal["file", "print"]


def toml_parse(file: str, search: str) -> object:
    configs = toml.load(file)
    return get(configs, search)


def kv_output(key: str, value: object) -> str:
    v = json.dumps(value)
    return "{key}={value}".format(key=key, value=v)


def keys_output(output: object):
    return keys(output)


def path_concat(path: str, *paths: str) -> str:
    result = os.path.join(path)
    for p in paths:
        result = os.path.join(result, p)

    return result


def args_parse():
    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers(dest="function")

    path_concat = sub_parser.add_parser('path', help="Path splicing.")
    toml_parse = sub_parser.add_parser('toml', help="Toml Parse.")
    kv_output = sub_parser.add_parser('kv', help="Output key=value.")

    toml_parse.add_argument('-f', '--file', type=str,
                            help="Specify the path to a file.")
    toml_parse.add_argument('-t', '--search-text',
                            type=str, help="Specify the path to a file.")
    toml_parse.add_argument(
        "-k", "--keys", action="store_true", help="Use Kyes output")

    path_concat.add_argument("-p", "--path", action="append",
                             help="Add directory path. like -p path/ -p xx/path")
    path_concat.add_argument("-e", "--key-path", type=str, help="output use key. key=path")

    kv_output.add_argument("-k", "--key", help="Key.")
    kv_output.add_argument("-v", "--value", help="Value.")

    parser.add_argument("-c", "--compress",
                        action="store_true", help="Compress output.")
    parser.add_argument("-o", "--output", choices=[
                        "file", "print"], default="print", help="Output mode, support to file or print.")
    parser.add_argument("-F", "--file-path", default="./parse.output",
                        help="When -- output is specified as file, the file path needs to be specified.")

    args = parser.parse_args()

    return (args, parser)


def output_handler(method: OUTPUT_METHOD, output: object, file_path: str):
    def output_print():
        print(output)

    def output_file():
        if (file_path == None):
            # 路径若为空，则不输出
            return

        with open(file_path, 'a') as f:
            o = output
            if not is_string(o):
                o = json.dumps(output)

            f.write(str(output))
            f.write('\n')

    switch = {
        "file": output_file,
        "print": output_print
    }

    handler = switch.get(method, None)
    if (handler == None):
        return

    handler()


def output_compress(output: object):
    if is_string(output):
        return output
    return json.dumps(output, separators=(',', ':'))


def path_handler(paths: list[str], key_path: str):
    p = path_concat(*paths)
    if key_path == None:
        return p

    return kv_output(key_path, p)


def toml_handler(file: str, search_text: str, keys: bool):
    toml_obj = toml_parse(file, search_text)
    if keys:
        toml_obj = keys_output(toml_obj)

    return toml_obj


def handler():
    args, parser = args_parse()

    function = args.function

    result = []

    if function == 'path':
        paths = args.path
        key_path = args.key_path

        result.append(path_handler(paths=paths, key_path=key_path))
    elif function == 'toml':
        file: str = args.file
        search_text: str = args.search_text
        keys: bool = args.keys

        result.append(toml_handler(
            file=file, search_text=search_text, keys=keys))
    elif function == 'kv':
        key: str = args.key
        value: str = args.value

        result.append(kv_output(key, value))
    else:
        parser.print_help()
        return

    if len(result) == 0:
        # 空
        return

    res = result[0]

    compress: bool = args.compress
    output: OUTPUT_METHOD = args.output
    file_path: str = args.file_path

    if compress:
        res = output_compress(res)

    output_handler(output, res, file_path)

if __name__ == "__main__":
    handler()
