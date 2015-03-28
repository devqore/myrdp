#!/usr/bin/env bash
python2-pyuic4 ui/mainwindow.ui -o app/gui/mainwindow_ui.py
python2-pyuic4 ui/hostconfig.ui -o app/gui/hostconfig_ui.py
pyrcc4 resources/resources.qrc -o app/gui/resources_rc.py
