
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
        self.timelapse_on = False
        try:
            print(gphoto.list_cameras())
            self.camera = gphoto.Camera()
            print(self.camera.supported_operations)
            self.camera_connected = True
        except AttributeError:
            print("Please Connect a Camera")
        except Exception:
            print("Unknown error")

    def _take_photo(self):
        image = self.camera.capture()
        with open(self.path + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), "wb") as photo:
            photo.write(image)
        print(self.path + str(self.count) + " saved")

    def _wait_int(self, delay, offset):
        delay = delay - offset
        print("offset =", offset)
        while delay > 0:
            delay -= 0.1
            time.sleep(0.1)

    def start_timelapse(self):

        while self.timelapse_on:
            self.count += 1
            # take initial time to calculate offset for variable capture time
            init_time = time.time()

            try:
                self._take_photo()
            except AttributeError:
                print("failed to take")
            # calculate the offset
            offset_time = time.time() - init_time
            self._wait_int(delay=self.interval, offset=offset_time)
        self.count = 0










