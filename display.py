from RPi import GPIO
from RPLCD.gpio import CharLCD


class Display:

    def __init__(self):
        self.lcd = CharLCD(pin_rs=15, pin_rw=18,
                           pin_e=16, pins_data=[21, 22, 23, 24],
                           numbering_mode=GPIO.BOARD)
        self._create_chars()

    def update_display(self, count, interval, counter=0,camera_connected=False):
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Interval:")
        self.lcd.cursor_pos = (0, 9)
        self.lcd.write_string(str(interval) + " ")
        if not counter == 0:
            self.lcd.cursor_pos = (0, 13)
            self.lcd.write_string(str(counter)[:3] + " ")
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string("Shots:" + str(count) + " ")
        if camera_connected: #displays camera icon if camera connected
            self.lcd.cursor_pos = (1, 13)
            self.lcd.write_string("\x00\x01\x02")

    def _create_chars(self):
        # camera icon
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
