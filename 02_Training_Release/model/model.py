# for control of system
from time import sleep
import plotext as pltx
from time import time
import RPi.GPIO as GPIO

# sensors
from sensor.sensor_adapter import AdapterSensor
from sensor.bmp581_sensor import BMP581Sensor
from sensor.spectrometer_sensor import SpectrometerSensor
from sensor.picamera_sensor import CameraSensor
from sensor.dummy_gaussian_sensor import GaussianSensor

# for data writing
from data.access import  initialize_session,read_sop_text
from model.csv_buffer import CSVBufferQueue
from model.camera_buffer import CameraBufferQueue

# for different views
from View.MainScreen import MainScreenView
from View.ManualScreen import ManualScreenView



# on start up
#List of data
writeBufferSize = 50

# state control
view_state = 1
main_view = None
manual_view = None
# for controlling passive sampling
PASSIVE_SAMPLE_PERIODS = 6
passive_sample_counter = PASSIVE_SAMPLE_PERIODS
CAMERA_STATE = 4

# Buttons
BUTTON_GPIO_ACTION = 21
BUTTON_GPIO_TRANSITION = 16

# 0.5 should be left this way, because pressure/temperature sensor could potentially not sample faster
# or needs to be adapted
sleep_time = 0.5




################################
# action control
################################
def on_start_up():
    global main_view,manual_view,CAMERA_STATE
    # set up buffers
    # the order of passing here is important, as the animation is hard coded based on the order
    """
    Order Should be:
    0. CSV over nm - Spectrometer
    1. CSV - Pressure
    2. CSV - Temperature
    3. CSV - Distance
    4. JPG - Image
    Make the passive sensors come first as they will always be on and not draw unnessecary power
    """

    labels = ["Spectrometer",
              "Pressure",
              "Temperature",
              "Distance",
              "Camera"
              ]
    shared_bmp = BMP581Sensor("Temperature-/Pressuresensor")
    """
    if not sensor implemented replace it with
    CSVBufferQueue(GaussianSensor(labels[INDEX OF ELEMENT IN LIST],2,0.3),writeBufferSize,data_buffer_size=10,time_buffer=True)
    
    """
    containers = [
        CSVBufferQueue(SpectrometerSensor(labels[0]),writeBufferSize,data_buffer_size=1,time_buffer=False),
        CSVBufferQueue(AdapterSensor(labels[1],shared_bmp,lambda x:x.sample_pressure())
                       ,storage_buffer_size=writeBufferSize,data_buffer_size=10,time_buffer=True),
        CSVBufferQueue(AdapterSensor(labels[2],shared_bmp,lambda x:x.sample_temperature())
                       ,storage_buffer_size=writeBufferSize,data_buffer_size=10,time_buffer=True),
        CSVBufferQueue(GaussianSensor(labels[3],2,0.3),writeBufferSize,data_buffer_size=10,time_buffer=True),
        CameraBufferQueue(CameraSensor(labels[4]))
    ]
    CAMERA_STATE = 4
    passive_containers = [1,2]
    # initialize data layer session
    initialize_session(labels,labels[:-1])



    # create Views
    main_view = MainScreenView(containers,passive_containers,labels)
    manual_view = ManualScreenView(read_sop_text())
    # needs to be here, otherwise you could call method before assignment of variables
    on_release_key('w', isr_state_transition)
    on_release_key('e', isr_state_action)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO_TRANSITION, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_GPIO_ACTION, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # needs to be here, otherwise you could call method before assignment of variables
    GPIO.add_event_detect(BUTTON_GPIO_TRANSITION, GPIO.RISING, 
            callback=isr_state_transition, bouncetime=50)
    GPIO.add_event_detect(BUTTON_GPIO_ACTION, GPIO.RISING, 
            callback=isr_state_action, bouncetime=50)

def on_shutdown():
    main_view.on_shutdown()

# method called for sampling passive sensors
def passive_sample():
    main_view.passive_sample()


################################
# state control
################################
# plot button, used for plot
def isr_state_transition(keyboard_event):
    global view_state
    if view_state==1: # if in manual mode
        view_state=0
    else:
        main_view.isr_state_transition()   
    
# sop button, used for sop
def isr_state_action(keyboard_event):
    global view_state
    if view_state==0: # if in plot mode
        # sensor is currently camera take a picture
        if main_view.state == CAMERA_STATE:
            main_view.isr_state_action()
        else:# otherwise go into SOP mode
            view_state=1
    else:
        # SOP screen scroll
        manual_view.isr_state_action()


################################
# set figure
################################
# main loop
def animate():   
    """
    Tip: check up if above the time, buffer is set when calling prepare time, otherwise error happens
    """
    # TODO add animate current View method
    if view_state==0:
        main_view.animate()
    else:
        manual_view.animate()
    

def action_loop():
    global passive_sample_counter, PASSIVE_SAMPLE_PERIODS
    # to ensure that the state does not get changed mid operation
    # TODO Replace passive sampling
    if not passive_sample_counter:
        passive_sample_counter-=1
        if not passive_sample_counter: passive_sample_counter= PASSIVE_SAMPLE_PERIODS
        passive_sample()
    animate()
    sleep(sleep_time)
