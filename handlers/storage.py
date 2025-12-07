class StorageHandler:
    def __init__(self, app):
        print("StorageHandler initialized")
        self.app = app
        print(self.app.dark_mode, type(self.app.dark_mode))
        print(self.app.accent_color, type(self.app.accent_color))
        print(self.app.start_screen_index, type(self.app.start_screen_index))