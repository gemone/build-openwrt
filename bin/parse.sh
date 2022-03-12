#!/usr/bin/env bash

ENVFILE=${ENVPATH}/env
UTILS=${WORKSPACE}/utils

parse() {
    python3 ${UTILS}/config_parse.py $@
}

get_config() {
    parse -c toml -f ${WORKSPACE}/config.toml $@
}

path_concat() {
    parse -c path $@
}


set_global_env() {
    echo "${1}=${2}" >> ${GITHUB_ENV}
    parse -c -o file -F ${ENVFILE} kv -k $1 -v $2
}

workspace_dir() {
    path_concat -p ${WORKSPACE} $@
}

