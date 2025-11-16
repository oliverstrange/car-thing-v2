import sys
from time import sleep

try:
    from gpiozero import RotaryEncoder, Button
    GPIO_AVAILABLE = True
except (ImportError, OSError) as e:
    # GPIOZero not available / not running on Pi
    print("Warning: GPIOZero not available, running in simulation mode:", e)
    GPIO_AVAILABLE = False


class GPIOHandler:
    def __init__(self, app):

        sleep(1)

        self.app = app
        self.last_rotary_value = 0

        if not GPIO_AVAILABLE:
            print("GPIOHandler disabled (not a Raspberry Pi environment)")
            return

        try:
            # Rotary encoder GPIO pins
            print("Initializing rotary encoder")
            self.encoder = RotaryEncoder(a=19, b=26, max_steps=16, wrap=True)
            print("Initializing button")
            self.button = Button(22)
            print("GPIO initialized")

            while True:  # Infinite loop to continuously monitor the encoder
                self.current_rotary_value = self.encoder.steps  # Read current step count from rotary encoder

                # Check if the rotary encoder value has changed
                if self.last_rotary_value != self.current_rotary_value:
                    print("Result =", self.current_rotary_value)  # Print the current value
                    self.last_rotary_value = self.current_rotary_value  # Update the last value

                # Check if the rotary encoder is pressed
                if self.button.is_pressed:
                    print("Button pressed!")  # Print message on button press
                    self.app.enter()
                    self.button.wait_for_release()  # Wait until button is released

                sleep(0.1)  # Short delay to prevent excessive CPU usage

            # Attach event handlers
            #self.encoder.when_rotated_clockwise = self._rotated_clockwise
            #self.encoder.when_rotated_counterclockwise = self._rotated_counterclockwise
            #self.button.when_pressed = self._pressed

        except Exception as e:
            print("Error initializing GPIOHandler:", e)
            print("GPIO input disabled")
            self.encoder = None
            self.button = None

    def _rotated_clockwise(self):
        print("Rotated clockwise")
        if not GPIO_AVAILABLE or self.encoder is None:
            return
        self.app.move_up()

    def _rotated_counterclockwise(self):
        print("Rotated counterclockwise")
        if not GPIO_AVAILABLE or self.encoder is None:
            return
        self.app.move_down()

    def _pressed(self):
        print("Button pressed")
        if not GPIO_AVAILABLE or self.button is None:
            return
        self.app.enter()