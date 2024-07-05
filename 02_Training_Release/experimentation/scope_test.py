from cv2 import VideoCapture

my_device = None


def init():
    my_device=VideoCapture(0)


print(my_device)


def f1():
    f2()


def f2():
    print("Eureka")

f1()