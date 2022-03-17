#!/usr/bin/env bash

# WORKDIR
# ENV

ENV=${ENVPATH}/env
WORKSPACE=${GITHUB_WORKSPACE}
WORKDIR=${GITHUB_WORKDIR}

[[ ! -f ${GITHUB_ENV} ]] && touch ${GITHUB_ENV}

UTILS=${WORKDIR}/utils

parse() {
    python3 ${UTILS}/config_parse.py $@
}

get_config() {
    parse -c toml -f ${WORKDIR}/config.toml $@
}

path_concat() {
    parse -c path $@
}


set_global_env() {
    echo "${1}=${2}" >> ${GITHUB_ENV}
    parse -c -o file -F ${ENV} kv -k $1 -v $2
}

workspace_dir() {
    path_concat -p ${WORKSPACE} $@
}


scripts_dir=`get_config -t '.scripts_dir'`
feeds_dir=`get_config -t '.feeds_dir'`
config_dir=`get_config -t '.config_dir'`
src_repo=`get_config -t '.repo'`
src_branch=`get_config -t '.branch'`

upload_release=`get_config -t '.upload_release'`

SCRIPTS_DIR=`workspace_dir -p ${scripts_dir}`
FEEDS_DIR=`workspace_dir -p ${feeds_dir}`
CONFIG_DIR=`workspace_dir -p ${config_dir}`
SRC_DIR=`workspace_dir -p ${WORKDIR} -p openwrt`

set_global_env SCRIPTS_DIR ${SCRIPTS_DIR}
set_global_env FEEDS_DIR ${FEEDS_DIR}
set_global_env CONFIG_DIR ${CONFIG_DIR}
set_global_env SRC_DIR ${SRC_DIR}
set_global_env SRC_REPO ${src_repo}
set_global_env SRC_BRANCH ${src_branch}
set_global_env UPLOAD_RELEASE ${upload_release}

configs=`get_config -t ".configs" -k`
