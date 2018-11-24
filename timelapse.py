import threading
import buttons
import display
import time
import gphoto2cffi as gphoto

# add automated build/test on rpi
# add remote control options
# ability to stream images back to source
# web front end to control camera


class TimeLapse:
    camera_connected = False

    def __init__(self, interval, path):
        self.path = path
        self.interval = interval
        self.count = 0
        self.buttons = buttons.buttons(35, 40, 38)
        self.display = display.Display()
        try:
            print(gphoto.list_cameras())
            self.camera = gphoto.Camera()
            print(self.camera.supported_operations)
            self.camera_connected = True
        except AttributeError:
            print("Please Connect a Camera")

    def _take_photo(self):
        image = self.camera.capture()
        with open(self.path + time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime()), "wb") as photo:
            photo.write(image)
        print(self.path + str(self.count) + " saved")

    def _wait_int(self, delay, offset):
        delay = delay - offset
        print("offset =",offset)
        while delay > 0:
            self.display.update_display(count = self.count,
                                        interval = self.interval,
                                        counter = delay,
                                        camera_connected = self.camera_connected)
            delay -= 0.1
            time.sleep(0.1)

    def start_timelapse(self):
        self.display.update_display(count=self.count,
                                    interval=self.interval,
                                    camera_connected=self.camera_connected)
        self._update_interval()
        while self.buttons.run_time_lapse():
            print(str(self.buttons.run_time_lapse) + str(self.count))
            self.count += 1
            # take initial time to calculate offset for variable capture time
            init_time = time.time()
            self.display.update_display(count=self.count,
                                        interval=self.interval,
                                        camera_connected=self.camera_connected)
            try:
                self._take_photo()
            except AttributeError:
                print("failed to take")
            # calculate the offset
            offset_time = time.time() - init_time
            self._wait_int(delay = self.interval,offset = offset_time)
        self.count = 0

    def _update_interval(self):
        interval_state = self.buttons.read_interval_state()
        if interval_state[0]:
            self.interval += 1
        if interval_state[1] and self.interval > 9:
            self.interval -= 1


timel = TimeLapse(30, "/home/pi/Timelapse_Photos/")

while True:
    timel.start_timelapse()






