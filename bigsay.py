import gi
from gi.repository import Gtk, Gdk, Pango, PangoCairo
gi.require_version("Gtk", "4.0")

class BigSayStyled(Gtk.Window):
    def __init__(self, application):
        super().__init__(application=application, title="bigsay")
        self.set_default_size(800, 400)
        
        self.text = "Type something..."

        # Main container
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_child(vbox)

        # 1. The Canvas
        self.canvas = Gtk.DrawingArea()
        self.canvas.set_vexpand(True) 
        self.canvas.set_hexpand(True)
        self.canvas.set_draw_func(self.on_draw)
        
        # 2. The Input Entry
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Type here...")
        self.entry.connect("changed", self.on_text_changed)
        
        # Add the CSS class "square-entry" to this specific widget
        # so we can target it in our CSS below
        self.entry.add_css_class("square-entry")

        vbox.append(self.canvas)
        vbox.append(self.entry)

    def on_text_changed(self, widget):
        # Simply update the text and redraw. No fancy enter logic.
        current_text = widget.get_text()
        self.text = current_text if current_text else ""
        self.canvas.queue_draw()

    def on_draw(self, area, cr, width, height):
        # 1. Force Background White (Manual Paint)
        # While CSS handles the window, painting the canvas explicitly 
        # ensures no transparency issues.
        cr.set_source_rgb(1, 1, 1) # White
        cr.paint()

        # 2. Draw Text (Force Black)
        cr.set_source_rgb(0, 0, 0) # Black

        # Layout logic (same as before)
        layout = PangoCairo.create_layout(cr)
        layout.set_text(self.text, -1)
        desc = Pango.FontDescription("Noto Sans")
        layout.set_font_description(desc)

        text_width, text_height = layout.get_pixel_size()

        if text_width > 0 and text_height > 0:
            scale_x = (width * 0.9) / text_width
            scale_y = (height * 0.9) / text_height
            scale = min(scale_x, scale_y)
            
            cr.move_to(
                (width - (text_width * scale)) / 2,
                (height - (text_height * scale)) / 2
            )
            cr.scale(scale, scale)

        PangoCairo.show_layout(cr, layout)

def on_activate(app):
    # --- CSS STYLING START ---
    css_provider = Gtk.CssProvider()
    
    # CSS to force white background and square borders
    css_data = """
    window {
        background-color: white;
        color: black;
    }
    
    entry.square-entry {
        background-color: white;
        color: black;
        border-radius: 0px;       /* Removes rounded corners */
        border: 2px solid black;  /* Thick square border */
        margin: 10px;             /* Spacing from window edge */
    }
    
    /* Ensure the text inside the entry is visible */
    entry.square-entry text {
        color: black;
    }
    """
    
    css_provider.load_from_data(css_data.encode('utf-8'))
    
    # Apply this CSS to the default display (globally for this app)
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(),
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
    # --- CSS STYLING END ---

    win = BigSayStyled(application=app)
    win.present()

if __name__ == "__main__":
    app = Gtk.Application(application_id="com.example.bigsay")
    app.connect('activate', on_activate)
    app.run(None)
