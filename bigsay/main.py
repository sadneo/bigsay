#!/usr/bin/env python
import sys
import contextlib
import os
from importlib import resources

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, GLib

ui_file = str(resources.files("bigsay").joinpath("assets", "main.ui"))
css_file = str(resources.files("bigsay").joinpath("assets", "style.css"))

def on_activate(app):
    builder = Gtk.Builder.new_from_file(ui_file)
    window = builder.get_object("app_window")
    window.set_application(app)

    css_provider = Gtk.CssProvider.new()
    css_provider.load_from_path(css_file)
    Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    label = builder.get_object("label")
    label.props.label = " ".join(sys.argv[1:])

    window.fullscreen()
    window.present()

def run_app():
    if len(sys.argv) < 2:
        print("Specify argument")
        sys.exit(1)

    app = Gtk.Application(application_id="org.sadneo.bigsay")
    app.connect("activate", on_activate)
    app.run(None)
