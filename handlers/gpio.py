import sys

try:
    from gpiozero import RotaryEncoder, Button
    GPIO_AVAILABLE = True
except (ImportError, OSError) as e:
    # GPIOZero not available / not running on Pi
    print("Warning: GPIOZero not available, running in simulation mode:", e)
    GPIO_AVAILABLE = False


class GPIOHandler:
    def __init__(self, app):
        self.app = app

        if not GPIO_AVAILABLE:
            print("GPIOHandler disabled (not a Raspberry Pi environment)")
            return

        try:
            # Rotary encoder GPIO pins
            self.encoder = RotaryEncoder(a=19, b=26, max_steps=16, wrap=True)
            self.button = Button(22)

            # Attach event handlers
            self.encoder.when_rotated_clockwise = self._rotated_clockwise
            self.encoder.when_rotated_counterclockwise = self._rotated_counterclockwise
            self.button.when_pressed = self._pressed

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