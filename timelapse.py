import threading
from RPi import GPIO
from RPLCD.gpio import CharLCD
import time
import gphoto2cffi as gphoto


class TimeLapse:
    camera_connected = False

    def __init__(self, interval, path):
        self.path = path
        self.interval = interval
        self.count = 0
        self.lcd = CharLCD(pin_rs=15, pin_rw=18, pin_e=16, pins_data=[21, 22, 23, 24], numbering_mode=GPIO.BOARD)
        self.buttons = Buttons(35, 40, 38)
        self._create_chars()
        try:
            print(gphoto.list_cameras())
            self.camera = gphoto.Camera()
            self.camera_connected = True
        except:
            print("Please Connect a Camera")

    def _update_display(self, counter=0):
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Interval:")
        self.lcd.cursor_pos = (0, 9)
        self.lcd.write_string(str(self.interval + " "))
        if not counter == 0:
            self.lcd.cursor_pos = (0, 13)
            self.lcd.write_string(str(counter))
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string("Shots:" + str(self.count) + " ")
        if self.camera_connected:
            self.lcd.cursor_pos = (1, 13)
            self.lcd.write_string("\x00\x01\x02")

    def _create_chars(self):
        bitmap0 = (
            0b00000,
            0b00000,
            0b00011,
            0b00011,
            0b00011,
            0b00011,
            0b00011,
            0b00011)
        bitmap1 = (
            0b01110,
            0b11111,
            0b11011,
            0b10001,
            0b00000,
            0b10001,
            0b11011,
            0b11111)
        bitmap2 = (
            0b00000,
            0b00000,
            0b11000,
            0b01000,
            0b11000,
            0b11000,
            0b11000,
            0b11000)
        self.lcd.create_char(0, bitmap0)
        self.lcd.create_char(1, bitmap1)
        self.lcd.create_char(2, bitmap2)

    def _take_photo(self):
        # run in separate thread to maintain timings
        image = self.camera.capture()
        with open("/home/pi/tlapse/" + self.path + str(self.count), "wb") as photo:
            photo.write(image)
        print(self.path + str(self.count) + " saved")

    def _wait_int(self, delay):
        while delay > 0:
            self._update_display(delay)
            delay -= 1
            time.sleep(1)

    def start_timelapse(self):
        self._update_display()
        self._update_interval()
        while self.buttons.run_time_lapse():
            print(str(self.buttons.run_time_lapse) + str(self.count))
            self.count += 1
            self._update_display(self.interval)
            t = threading.Thread(self._take_photo())
            t.start()
            self._wait_int(self.interval)
            t.join()
        self.count = 0

    def _update_interval(self):
        interval_state = self.buttons.read_interval_state()
        if interval_state[0]:
            self.interval += 1
        if interval_state[1] and self.interval > 0:
            self.interval -= 1


class Buttons:
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


timel = TimeLapse(10, "Frame")

while (True):
    timel.start_timelapse()






