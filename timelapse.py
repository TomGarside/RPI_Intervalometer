import threading
from RPi import GPIO
from RPLCD.gpio import CharLCD
import time
import gphoto2cffi as gphoto


class timelapse:
    camera_conected = false

    def __init__(self, interval, path):
        self.path = path
        self.interval = interval
        self.count = 0
        self.lcd = CharLCD(pin_rs=15, pin_rw=18, pin_e=16, pins_data=[21, 22, 23, 24], numbering_mode=GPIO.BOARD)
        self.buttons = buttons(35, 40, 38)
        self._create_Chars()
        try:
            print(gphoto.list_cameras())
            self.camera = gphoto.Camera()
            self.camera_conected = True
        except:
            print("Please Connect a Camera")

    def _updateDisplay(self, counter=0):
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Interval:")
        self.lcd.cursor_pos = (0, 9)
        self.lcd.write_string(str(self.interval + " "))
        if not counter == 0:
            self.lcd.cursor_pos = (0, 13)
            self.lcd.write_string(str(counter))
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string("Shots:" + str(self.count) + " ")
        if self.camera_conected:
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

    def _takePhoto(self):
        # run in seperate thread to maintain timings
        image = self.camera.capture()
        with open("/home/pi/tlapse/" + self.path + str(self.count), "wb") as photo:
            photo.write(image)
        print(self.path + str(self.count) + " saved")

    def _wait_int(self, delay):
        while delay > 0:
            self._updateDisplay(delay)
            delay -= 1
            time.sleep(1)

    def startTimelapse(self):
        self._updateDisplay()
        self._update_interval()
        while (self.buttons.run_time_lapse()):
            print(str(self.buttons.run_time_lapse) + str(self.count))
            self.count += 1
            self._updateDisplay(self.interval)
            t = threading.Thread(self._takePhoto())
            t.start()
            self._wait_int(self.interval)
            t.join()
        self.count = 0

    def _update_interval(self):
        intervalState = self.buttons.readintervalstate()
        if intervalState[0]:
            self.interval += 1
        if intervalState[1] and self.interval > 0:
            self.interval -= 1


class buttons:
    intervalUp = False
    intervalDown = False
    runTimelapse = False

    def __init__(self, pinOne, pinTwo, pinThree):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup([pinOne, pinTwo, pinThree], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(pinOne, GPIO.BOTH, callback=self.__switchTlapseState, bouncetime=400)
        GPIO.add_event_detect(pinTwo, GPIO.FALLING, callback=self.__upInterval, bouncetime=400)
        GPIO.add_event_detect(pinThree, GPIO.FALLING, callback=self.__downInterval, bouncetime=400)

    def __switchTlapseState(self, channel):
        self.runTimelapse = not self.runTimelapse
        print(self.runTimelapse)

    def __upInterval(self, channel):
        self.intervalUp = True
        self.intervalDown = False

    def __downInterval(self, channel):
        self.intervalUp = False
        self.intervalDown = True

    def readintervalstate(self):
        up = self.intervalUp
        down = self.intervalDown
        self.intervalUp = False
        self.intervalDown = False
        return [up, down]

    def run_time_lapse(self):
        return self.runTimelapse


timel = timelapse(10, "Frame")

while (True):
    timel.startTimelapse()






