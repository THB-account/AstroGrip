from cv2 import VideoCapture
from PIL import Image
_cap_device = None

def cam_start_up():
    global _cap_device
    # Initialize the webcam
    _cap_device = VideoCapture(0)  # 0 corresponds to the first webcam connected, 1 for the second, and so on

    # Check if the webcam is opened successfully
    if not _cap_device.isOpened():
        print("Error: Unable to open webcam.")
        raise Exception("Cam is not open.")
    
# method for capturing image 
def capture_image():
    # Capture an image
    ret, image = _cap_device.read()

    if not ret:
        _cap_device.release()
        raise Exception("Exception when trying to capture image")
    
    return Image.open(image)
