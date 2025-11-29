import slint
from handlers.serial import SerialHandler


def main():
    """Main function to run the circular display app with Python backend."""
    try:
        # Load Slint app
        App = slint.load_file("main.slint").App
        app = App()

        # -------------------------------
        # Connect serial inputs
        # -------------------------------
        serial = SerialHandler(app)

        # Run Slint in the main thread
        app.run()
        print("Application exited normally")
        
    except Exception as e:
        print(f"Error running application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())