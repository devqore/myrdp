import gi

from app.config import Config
from app.database import Database

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


class HeaderBarWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="MyRDP")
        self.set_border_width(10)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "MyRDP"
        self.set_titlebar(hb)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        button_menu = Gtk.Button()
        menu_icon = Gio.ThemedIcon(name="emblem-system")
        image = Gtk.Image.new_from_gicon(icon=menu_icon, size=Gtk.IconSize.BUTTON)
        button_menu.add(image)
        box.add(button_menu)

        entry = Gtk.Entry()
        box.add(entry)

        button_connect = Gtk.Button()
        icon = Gio.ThemedIcon(name="video-display-symbolic")
        image = Gtk.Image.new_from_gicon(icon=icon, size=Gtk.IconSize.BUTTON)
        button_connect.add(image)
        box.add(button_connect)
        hb.pack_start(box)

        self.add(Gtk.TextView())


if __name__ == "__main__":

    config = Config()
    config.set_log_level()

    db = Database(config.get_connection_string())
    db.create()
    db.update()

    win = HeaderBarWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
