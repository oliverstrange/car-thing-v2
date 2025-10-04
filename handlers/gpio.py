import sys

try:
    from gpiozero import RotaryEncoder, Button
    GPIO_AVAILABLE = True
except (ImportError, OSError) as e:
    # GPIOZero not available / not running on Pi
    print("Warning: GPIOZero not available, running in simulation mode:", e)
    GPIO_AVAILABLE = False


class GPIOHandler:
    def __init__(self, app, menu_length=3):
        self.app = app
        self.menu_length = menu_length

        if not GPIO_AVAILABLE:
            print("GPIOHandler disabled (not a Raspberry Pi environment)")
            return

        try:
            # Rotary encoder GPIO pins
            self.encoder = RotaryEncoder(a=17, b=18, max_steps=100)
            self.button = Button(27)  # optional push button

            # Track last position to detect rotation direction
            self.last_steps = 0
            self.encoder.steps = 0

            # Attach event handlers
            self.encoder.when_rotated = self._rotated
            self.button.when_pressed = self._pressed
        except Exception as e:
            print("Error initializing GPIOHandler:", e)
            print("GPIO input disabled")
            self.encoder = None
            self.button = None

    def _rotated(self):
        if not GPIO_AVAILABLE or self.encoder is None:
            return

        delta = self.encoder.steps - getattr(self, "last_steps", 0)
        self.last_steps = self.encoder.steps

        if delta > 0:
            self.app.move_down()
        elif delta < 0:
            self.app.move_up()

    def _pressed(self):
        if not GPIO_AVAILABLE or self.button is None:
            return

        self.app.enter()