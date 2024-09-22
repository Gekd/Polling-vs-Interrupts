import RPi.GPIO as GPIO
from time import sleep

class TrafficLight:
    def __init__(self):

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        self.red_led_1 = 37
        self.yellow_led = 33
        self.green_led_1 = 32
        self.red_led_2 = 31
        self.green_led_2 = 29
        self.white_led = 18
        self.button_bin = 16

        GPIO.setup(self.red_led_1, GPIO.OUT)
        GPIO.setup(self.yellow_led, GPIO.OUT)
        GPIO.setup(self.green_led_1, GPIO.OUT)
        GPIO.setup(self.red_led_2, GPIO.OUT)
        GPIO.setup(self.green_led_2, GPIO.OUT)
        GPIO.setup(self.white_led, GPIO.OUT)
        GPIO.setup(self.button_bin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.button_pressed = False

    def check_button(self):
        if not self.button_pressed:
            if GPIO.input(self.button_bin) == GPIO.HIGH:
                GPIO.output(self.white_led, GPIO.LOW)
            else:
                GPIO.output(self.white_led, GPIO.HIGH)
                self.button_pressed = True
 
    def pedestrian_traffic_light(self, timer):
        GPIO.output(self.white_led, GPIO.LOW)
        GPIO.output(self.red_led_2, GPIO.LOW)
        GPIO.output(self.green_led_2, GPIO.HIGH)

        for i in range(int(timer)):
            sleep(1)
            self.check_button()

        GPIO.output(self.green_led_2, GPIO.LOW)
        GPIO.output(self.red_led_2, GPIO.HIGH)

    def car_traffic_light_red(self, timer):
        if self.button_pressed:
            GPIO.output(self.red_led_1, GPIO.HIGH)
            self.pedestrian_traffic_light(timer)
            GPIO.output(self.red_led_1, GPIO.LOW)
        else:
            GPIO.output(self.white_led, GPIO.LOW)
            GPIO.output(self.red_led_2, GPIO.HIGH)
            GPIO.output(self.red_led_1, GPIO.HIGH)

            for i in range(int(timer)):
                sleep(1)
                self.check_button()

            GPIO.output(self.red_led_1, GPIO.LOW)

    def car_traffic_light_yellow(self, timer):
        GPIO.output(self.yellow_led, GPIO.HIGH)

        if timer >= 1:
            for i in range(int(timer)):
                sleep(1)
                self.check_button()
        else:
            sleep(timer)
            self.check_button()

        GPIO.output(self.yellow_led, GPIO.LOW)

    def car_traffic_light_green(self, timer):
        GPIO.output(self.green_led_1, GPIO.HIGH)

        for i in range(int(timer)):
            sleep(1)
            self.check_button()

        GPIO.output(self.green_led_1, GPIO.LOW)

    def traffic_light_loop(self):

        self.car_traffic_light_red(5)
        self.car_traffic_light_yellow(1)
        self.car_traffic_light_green(5)

        for i in range(3):
            self.car_traffic_light_yellow(1/3)
            sleep(1/3)
            self.check_button()

    def run(self):
        try:
            while True:

                if GPIO.input(self.white_led) == GPIO.HIGH:
                    self.button_pressed = False

                self.traffic_light_loop(False)

        except KeyboardInterrupt:
            print("Keyboard interrupt")

        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    traffic_light = TrafficLight()
    traffic_light.run()
