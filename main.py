import slint
import threading
from pynput import keyboard


def on_press(key):
    print("Key pressed")

def run_keyboard_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()  # Keep the listener running

def main():
    """Main function to run the circular display app with Python backend."""
    try:
        # Load Slint app
        App = slint.load_file("main.slint").App
        app = App()

        # Start the keyboard listener in a separate thread
        listener_thread = threading.Thread(target=run_keyboard_listener, daemon=True)
        listener_thread.start()
        print("Keyboard listener started...")

        # Run Slint in the main thread
        app.run()
        
    except Exception as e:
        print(f"Error running application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())