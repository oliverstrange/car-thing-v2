import slint
from time import sleep
from datetime import timedelta

try:
    import serial
    SERIAL_AVAILABLE = True
except ImportError as e:
    # Serial library not available
    print("Warning: Serial library not available, running in simulation mode:", e)
    SERIAL_AVAILABLE = False


class SerialHandler:
    def __init__(self, app, port=None, baudrate=115200):
        """
        Initialize SerialHandler with serial communication.
        
        Args:
            app: The application instance with move_up, move_down, and enter methods
            port: Serial port (default: None, will auto-detect ACM0/ACM1)
            baudrate: Serial baud rate (default: 115200)
        """
        sleep(1)

        self.app = app
        self.baudrate = baudrate
        self.serial_conn = None

        if not SERIAL_AVAILABLE:
            print("Serial handler disabled (serial library not available)")
            return

        ports_to_try = [port] if port else ['/dev/ttyACM0', '/dev/ttyACM1']
        
        for p in ports_to_try:
            try:
                print(f"Attempting to connect to {p} at {baudrate} baud...")
                self.serial_conn = serial.Serial(port=p, baudrate=baudrate, timeout=0) # Non-blocking
                print(f"Serial connection established on {p}")
                self.port = p
                break
            except Exception as e:
                print(f"Failed to connect to {p}: {e}")
        
        if self.serial_conn:
            # Start polling serial data using Slint Timer
            self.timer = slint.Timer()
            self.timer.start(slint.TimerMode.Repeated, timedelta(milliseconds=10), self._poll_serial)
            print("Serial polling timer started")
        else:
            print("Could not establish serial connection on any port")

    def _poll_serial(self):
        if not self.serial_conn:
            return

        try:
            if self.serial_conn.in_waiting > 0:
                # Read all available bytes to avoid lag
                line = self.serial_conn.readline().decode("utf-8", errors="ignore").rstrip()
                if line:
                    print(f"Received: {line}", flush=True)
                    self._process_command(line)
        except Exception as e:
            print(f"Serial poll exception: {e}", flush=True)

    def _process_command(self, command):
        """
        Process serial commands and call appropriate app methods.
        
        Expected commands:
        - "UP" or "CW" (clockwise) -> move_up()
        - "DOWN" or "CCW" (counter-clockwise) -> move_down()
        - "ENTER" or "PRESS" -> enter()
        """
        command = command.upper()
        
        # Since we are in a Timer callback (part of the event loop), we can call app methods directly!
        if command in ['UP', 'CW', 'CLOCKWISE']:
            print("Rotated clockwise", flush=True)
            self.app.move_up()
        elif command in ['DOWN', 'CCW', 'COUNTERCLOCKWISE', 'COUNTER-CLOCKWISE']:
            print("Rotated counterclockwise", flush=True)
            self.app.move_down()
        elif command in ['ENTER', 'PRESS', 'BUTTON']:
            print("Button pressed", flush=True)
            self.app.enter() 
        else:     
            print(f"Unknown command: {command}", flush=True)

    def cleanup(self):
        """Close serial connection and stop timer."""
        if hasattr(self, 'timer'):
            self.timer.stop()
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("Serial connection closed")