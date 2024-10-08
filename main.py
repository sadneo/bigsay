#!/usr/bin/env python
import time, sys
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, GLib

def on_activate(app):
    builder = Gtk.Builder.new_from_file("/usr/share/bigsay/main.ui")
    window = builder.get_object("app_window")
    window.set_application(app)

    css_provider = Gtk.CssProvider.new()
    css_provider.load_from_path("/usr/share/bigsay/style.css")
    Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    label = builder.get_object("label")
    label.props.label = sys.argv[1]

    window.fullscreen()
    window.present()

if len(sys.argv) < 2:
    print("Specify argument")
    sys.exit(1)

app = Gtk.Application(application_id="org.sadneo.bigsay")
app.connect("activate", on_activate)
app.run(None)
