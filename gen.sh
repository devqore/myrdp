#!/usr/bin/env bash
for i in `ls ui/*.ui`; do
    echo "Generating python file for $i"
    pyuic4 --from-imports $i -o app/gui/$(basename ${i%.ui})_ui.py
done

echo "Generating python files for resource file"
pyrcc4 -py3 app/resources/resources.qrc -o app/gui/resources_rc.py
