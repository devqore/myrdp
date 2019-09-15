#!/usr/bin/env bash
set -e
rm build/ -rf
rm dist/ -rf
. /opt/python3-venvs/myrdp/bin/activate
export VERSION=`python3 -c "import app; print(app.__version__)"`
# ensure that PyQt4 is properly installed by trying to import PyQt4
python3 -c "from PyQt4 import QtGui"
export VERSIONED_NAME=myrdp-$VERSION
pyinstaller myrdp.spec
cd dist
mv myrdp $VERSIONED_NAME
tar -jcvf $VERSIONED_NAME.tar.bz2 $VERSIONED_NAME
