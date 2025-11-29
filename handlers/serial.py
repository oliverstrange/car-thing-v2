import threading
from time import sleep

try:
    import serial
    SERIAL_AVAILABLE = True
except ImportError as e:
    # Serial library not available
    print("Warning: Serial library not available, running in simulation mode:", e)
    SERIAL_AVAILABLE = False


class SerialHandler:
    def __init__(self, app, port='/dev/ttyACM1', baudrate=9600):
        """
        Initialize SerialHandler with serial communication.
        
        Args:
            app: The application instance with move_up, move_down, and enter methods
            port: Serial port (default: 'COM3' for Windows, use '/dev/ttyUSB0' or '/dev/ttyACM0' for Linux)
            baudrate: Serial baud rate (default: 9600)
        """
        sleep(1)

        self.app = app
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None

        if not SERIAL_AVAILABLE:
            print("Serial handler disabled (serial library not available)")
            return

        try:
            print(f"Initializing serial connection on {port} at {baudrate} baud")
            self.serial_conn = serial.Serial(port=port, baudrate=baudrate, timeout=1)
            print("Serial connection established")
            
            # Start reading serial data in a separate thread
            self.running = True
            self.read_thread = threading.Thread(target=self._read_serial_loop, daemon=True)
            self.read_thread.start()
            print("Serial reader thread started")

        except Exception as e:
            print(f"Error initializing serial handler: {e}")
            print("Serial input disabled")
            self.serial_conn = None

    def _read_serial_loop(self):
        """Continuously read serial data and process commands."""
        if not self.serial_conn:
            return

        while self.running:
            print("Looping serial data... ")
            try:
                if self.serial_conn.in_waiting > 0:
                    # Read line from serial (assuming commands end with newline)
                    print("Reading serial data... ")
                    line = self.serial_conn.readline().decode('utf-8').rstrip()
                    
                    if line:
                        print(f"Received serial command: {line}")
                        self._process_command(line)
                
                sleep(0.01)  # Small delay to prevent excessive CPU usage
                
            except serial.SerialException as e:
                print(f"Serial error: {e}")
                break
            except Exception as e:
                print(f"Error reading serial: {e}")
                sleep(0.1)

    def _process_command(self, command):
        """
        Process serial commands and call appropriate app methods.
        
        Expected commands:
        - "UP" or "CW" (clockwise) -> move_up()
        - "DOWN" or "CCW" (counter-clockwise) -> move_down()
        - "ENTER" or "PRESS" -> enter()
        """
        command = command.upper()
        
        if command in ['UP', 'CW', 'CLOCKWISE']:
            print("Rotated clockwise")
            self.app.move_up()
        elif command in ['DOWN', 'CCW', 'COUNTERCLOCKWISE', 'COUNTER-CLOCKWISE']:
            print("Rotated counterclockwise")
            self.app.move_down()
        elif command in ['ENTER', 'PRESS', 'BUTTON']:
            print("Button pressed")
            self.app.enter() 
        else:     
            print(f"Unknown command: {command}")

    def cleanup(self):
        """Close serial connection and stop reading thread."""
        self.running = False
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("Serial connection closed")