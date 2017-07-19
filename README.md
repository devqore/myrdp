MyRDP - Remote desktop manager  

[![MyRDP movie](https://docs.google.com/uc?export=download&id=0B6f0xD4xZ3ABQ2g2dGxhdS1vcms)](https://youtu.be/2FoynZj-QFM)

To start MyRDP run:

`````
git clone https://github.com/szatanszmatan/myrdp.git   
cd myrdp   
python main.py
`````

You need:
- python 2.7
	+ PyQt4
    + SQLAlchemy
    + alembic
- xfreerdp command line tools


Release notes
=============

2017.1:
-------

- config.yaml removed, settings are available from ui
- default location of database file changed to $HOME/.config/myrdp/myrdp.sqlite (file should be moved manually or file location can be selected in the settings tab)
- rdesktop removed from settings