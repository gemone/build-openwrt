#!/usr/bin/env bash

# env SRC_DIR=xxx x.sh

CLASH_DIR=${SRC_DIR}/package/luci-app-openclash

rm -rf ${CLASH_DIR}
mkdir ${CLASH_DIR}

SVN=$(which svn)

[[ -e ${SVN} ]] || exit 1

svn co https://github.com/vernesong/OpenClash/trunk/luci-app-openclash ${CLASH_DIR}

# 编译 po2lmo (如果有po2lmo可跳过)
PO2LMO=$(which po2lmo)
[[ -e ${PO2LMO} ]] && exit 0
pushd ${CLASH_DIR}/tools/po2lmo
make && sudo make install
popd
