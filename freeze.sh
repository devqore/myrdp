#!/usr/bin/env bash
rm build/ -rf
rm dist/ -rf
. /opt/python2-venvs/myrdp/bin/activate
pyinstaller myrdp.spec