#!/usr/bin/env bash
rm build/ -rf
rm dist/ -rf
pyinstaller main.py -n myrdp
cp conf dist/myrdp -R
