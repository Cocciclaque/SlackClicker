import valuesapi
import pystray
from pystray import Menu
from pystray import MenuItem as item
from PIL import Image
import threading
from functools import partial
class GameApp:
    def __init__(self, path, localization, start="en", visibility=True ):
        self.opened = False
        self.icon = None
        self.path = path
        self.visibility = visibility
        self.localization = localization
        self.selected_lang = start
    
    # Function to create an icon image (using your custom image)
    def create_image(self):
        # Load your custom icon (make sure the path is correct)
        icon_image = Image.open(self.path)  # Change this to the path of your image
        return icon_image
    
    # Function to quit the program (remove icon from taskbar)
    def on_quit(self, icon):
        self.opened = False  # Mark the app as closed
        icon.stop()
    
    def toggle_mode(self):
        self.visibility = not self.visibility

    def get_visibility(self):
        return self.visibility

    def set_localization(self, lang, icon=0, menu_item=0):
        self.selected_lang = lang

    def get_localization(self):
        return self.selected_lang

    # Function to run the taskbar icon
    def setup_icon(self):

        submenu_items = [
            item(lang,
                 partial(self.set_localization, lang))
            for lang in self.localization
        ]

        self.icon = pystray.Icon("I'll Work After This", self.create_image(), title="I'll Work After This", menu=(
            item('Quit the game', self.on_quit),  
            item('Toggle visibility mode', self.toggle_mode),
            item('Select Language', Menu(*submenu_items)
        )))
        self.opened = True  # Mark the app as opened
        self.icon.run()
    
    # Thread to run the taskbar icon in the background
    def run_icon(self):
        icon_thread = threading.Thread(target=self.setup_icon)
        icon_thread.daemon = True  # Allow the icon thread to close when the program ends
        icon_thread.start()

    # Start the application
    def start(self):
        self.run_icon()
        self.opened = True  # App is now running
        valuesapi.show_notification("How to close the game", "Go in the app system tray right below to close the game.")

# Example of using the class
if __name__ == "__main__":
    app = GameApp()
    app.start()
