import threading

class Motor():
    STEP = 10
    DELAY = 0.1
    def __init__(self, pwm_pin, dir_pin):
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        self._power = 0
        self._except_power = 0

    def set_power(self, power):
        if power >= 0:
            direction = 0
        elif power < 0:
            direction = 1
        power = abs(power)
        if power != 0:
            power = int(power /2 ) + 50
        power = power

        direction = direction
        self.dir_pin.value(direction)
            
        self.pwm_pin.pulse_width_percent(power)