#!/usr/bin/env bash

# env SRC_DIR=xxx x.sh

S_DIR=${SRC_DIR}/package/luci-app-unblockneteasemusic

GIT=$(which git)

${GIT} clone --depth 1 https://github.com/UnblockNeteaseMusic/luci-app-unblockneteasemusic.git ${S_DIR}


