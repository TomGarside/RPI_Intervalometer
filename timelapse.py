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
            self.camera_connected = True
        except AttributeError:
            print("Please Connect a Camera")

    def _take_photo(self):
        # run in separate thread to maintain timings - try this on a multi-core cpu
        image = self.camera.capture()
        with open("/home/pi/tlapse/" + self.path + str(self.count), "wb") as photo:
            photo.write(image)
        print(self.path + str(self.count) + " saved")

    def _wait_int(self, delay, offset):
        delay = delay - offset
        while delay > 0:
            self.display.update_display(delay)
            delay -= 1
            time.sleep(1)

    def start_timelapse(self):
        self.display.update_display()
        self._update_interval()
        while self.buttons.run_time_lapse():
            print(str(self.buttons.run_time_lapse) + str(self.count))
            self.count += 1
            # take initial time to calculate offset for variable capture time
            init_time = time.time()
            self.display.update_display(self.interval)
            t = threading.Thread(self._take_photo())
            try:
                t.start()
            except AttributeError:
                print("failed to take")
            # calculate the offset
            offset_time = time.time() - init_time
            self._wait_int(self.interval, offset_time)
            t.join()
        self.count = 0

    def _update_interval(self):
        interval_state = self.buttons.read_interval_state()
        if interval_state[0]:
            self.interval += 1
        if interval_state[1] and self.interval > 0:
            self.interval -= 1


timel = TimeLapse(10, "Frame")

while True:
    timel.start_timelapse()






