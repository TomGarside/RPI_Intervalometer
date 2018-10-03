from RPI import GPIO


class buttons:
    intervalUp = False
    intervalDown = False
    runTimeLapse = False

    def __init__(self, pin_one, pin_two, pin_three):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup([pin_one, pin_two, pin_three], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(pin_one, GPIO.BOTH, callback=self.__switch_tlapse_state, bouncetime=400)
        GPIO.add_event_detect(pin_two, GPIO.FALLING, callback=self.__up_interval, bouncetime=400)
        GPIO.add_event_detect(pin_three, GPIO.FALLING, callback=self.__down_interval, bouncetime=400)

    def __switch_tlapse_state(self, channel):
        self.runTimeLapse = not self.runTimeLapse
        print(self.runTimeLapse)

    def __up_interval(self, channel):
        self.intervalUp = True
        self.intervalDown = False

    def __down_interval(self, channel):
        self.intervalUp = False
        self.intervalDown = True

    def read_interval_state(self):
        up = self.intervalUp
        down = self.intervalDown
        self.intervalUp = False
        self.intervalDown = False
        return [up, down]

    def run_time_lapse(self):
        return self.runTimeLapse
