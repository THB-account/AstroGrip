from sensor.abstract_sensor import AbstractSensor
from cv2 import VideoCapture
from PIL import Image

class CameraSensor(AbstractSensor):
    def __init__(self,name):
        super().__init__(name)
        self.__initialize_sensor()
        
    def __initialize_sensor(self):
        global _cap_device
        # Initialize the webcam
        _cap_device = VideoCapture(0)  # 0 corresponds to the first webcam connected, 1 for the second, and so on
        # Check if the webcam is opened successfully
        if not _cap_device.isOpened():
            print("Error: Unable to open webcam.")
            raise Exception("Cam is not open.")

    def turn_on(self):
        pass

    def turn_off(self):
        pass

    def sample(self):
        # Capture an image
        ret, image = _cap_device.read()

        if not ret:
            _cap_device.release()
            raise Exception("Exception when trying to capture image")
        
        return Image.fromarray(image)
