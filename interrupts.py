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

        GPIO.add_event_detect(self.button_bin, GPIO.RISING, callback=self.button_callback, bouncetime=300)

    def pedestrian_traffic_light(self, timer):
        GPIO.output(self.white_led, GPIO.LOW)
        GPIO.output(self.red_led_2, GPIO.LOW)
        GPIO.output(self.green_led_2, GPIO.HIGH)
        sleep(timer)
        GPIO.output(self.green_led_2, GPIO.LOW)
        GPIO.output(self.red_led_2, GPIO.HIGH)

    def car_traffic_light_red(self, timer, pressed):
        if pressed:
            GPIO.output(self.red_led_1, GPIO.HIGH)
            self.pedestrian_traffic_light(timer)
            GPIO.output(self.red_led_1, GPIO.LOW)
        else:
            GPIO.output(self.white_led, GPIO.LOW)
            GPIO.output(self.red_led_2, GPIO.HIGH)
            GPIO.output(self.red_led_1, GPIO.HIGH)
            sleep(timer)
            GPIO.output(self.red_led_1, GPIO.LOW)

    def car_traffic_light_yellow(self, timer):
        GPIO.output(self.yellow_led, GPIO.HIGH)
        sleep(timer)
        GPIO.output(self.yellow_led, GPIO.LOW)

    def car_traffic_light_green(self, timer):
        GPIO.output(self.green_led_1, GPIO.HIGH)
        sleep(timer)
        GPIO.output(self.green_led_1, GPIO.LOW)

    def traffic_light_loop(self, pressed):
        if pressed:
            self.car_traffic_light_red(5, True)
        else:
            self.car_traffic_light_red(5, False)

        self.car_traffic_light_yellow(1)
        self.car_traffic_light_green(5)

        for i in range(3):
            self.car_traffic_light_yellow(1/3)
            sleep(1/3)

    def button_callback(self, channel):
        GPIO.output(self.white_led, GPIO.HIGH)

    def run(self):
        try:
            while True:
                if GPIO.input(self.white_led) == GPIO.HIGH:
                    self.traffic_light_loop(True)
                else:
                    self.traffic_light_loop(False)

        except KeyboardInterrupt:
            print("Keyboard interrupt")

        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    traffic_light = TrafficLight()
    traffic_light.run()
