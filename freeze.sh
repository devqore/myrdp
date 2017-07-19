#!/usr/bin/env bash
rm build/ -rf
rm dist/ -rf
pyinstaller2 myrdp.spec
cp conf dist/myrdp -R
