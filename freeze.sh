#!/usr/bin/env bash
rm build/ -rf
rm dist/ -rf
pyinstaller myrdp.spec
cp conf dist/myrdp -R
