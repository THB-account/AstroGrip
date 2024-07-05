from View.AbstractView import AbstractView
import plotext as pltx
from time import time
from data.access import create_access_path

def prepare_time_data(time_ar):
        t = time()
        return [x-t for x in time_ar]

class MainScreenView:
    def __init__(self,containers,passive_containers,labels):
        # TODO encapsulate attributes. This is dangerous at the moment
        
        self.state = 0
        self.NUM_STATES = len(containers)
        self.transition_signal = False

        self.containers = containers
        self.labels = labels
        self.passive_containers = passive_containers
        self.data_buffer = self.containers[self.state].data_buffer
        if self.containers[self.state].use_time:
            self.time_buffer = self.containers[self.state].time_buffer

    def isr_state_transition(self):
        self.transition_signal = True
    # aka plot button
    def transition_action(self):
        # transition of sensor and associated storage before into inactive state
        # as of now only active for taking image with camera
        self.containers[self.state].transition()
        self.state+=1
        if self.state==self.NUM_STATES:
            self.state=0

        self.data_buffer = self.containers[self.state].data_buffer
        if self.containers[self.state].use_time:
            self.time_buffer = self.containers[self.state].time_buffer
    
    # SOP plot button
    # just used for camera
    def isr_state_action(self):
        # this is just used for setting an open job
        # for taking a picture, but could be used for other tasks
        # should only change the internal state of a data collection object
        self.containers[self.state].open_job()

    def animate(self):
        # as this handles the internal state
        # and animate being the main sate of action
        # this should be done here
        if self.transition_signal:
            self.transition_signal = False
            self.transition_action()
        
        match self.state:
            case 0: # spectrometer - scatter
                self.containers[self.state].sample() 
                self.set_up_plot()  
                #pltx.plot(self.data_buffer)
                pltx.ylabel("x: wavelength nm",2)
                pltx.ylabel("y: amplitude")
                pltx.plot(self.data_buffer[0])
            case 1: # pressure - scatter
                self.containers[self.state].sample()
                self.set_up_plot()
                pltx.ylabel("x: time(s)",2)
                pltx.ylabel("y: pressure kPa") 
                pltx.plot(prepare_time_data(self.time_buffer),self.data_buffer)                    

            case 2: # temperature
                self.containers[self.state].sample()
                self.set_up_plot()
                #pltx.plot(self.data_buffer)
                pltx.ylabel("x: time(s)",2)
                pltx.ylabel("y: temperature C°")
                pltx.plot(prepare_time_data(self.time_buffer),self.data_buffer)
            case 3: # distance
                self.containers[self.state].sample()
                self.set_up_plot()
                pltx.ylabel("x: time(s)",2)
                pltx.ylabel("y: distance m")
                pltx.plot(prepare_time_data(self.time_buffer),self.data_buffer)
                
            case 4: # camera
                if self.containers[self.state].check_for_jobs():
                    self.containers[self.state].sample()
                    self.set_up_plot()
                    pltx.image_plot(create_access_path(self.containers[self.state].name,self.containers[self.state].last_job,"jpg"))
            case _:
                pass

        pltx.show()

    def set_up_plot(self):
        pltx.clf()
        pltx.title("Data")
        pltx.subplots(1,2)      
        self.set_state_labels()
        pltx.subplot(1,1)

    def set_state_labels(self):
        pltx.subplot(1,2).plot_size(pltx.tw() // 4, None)
        pltx.title("Sensors")
        temp = self.labels.copy()
        temp[self.state] = f"> {temp[self.state]}"
        [pltx.text(temp[i], x=1,y=-i,alignment="center",color="green",style="italic") for i in range(len(temp))]
        pltx.xticks([])
        pltx.yticks([])

    def on_shutdown(self):
        # empty data queue
        [con.on_shutdown() for con in self.containers]
        # this function only gets called, when shutting down, do for example an interrupt
        # so catching anything is reasonable, due to trying to free resources
        for con in self.containers:
            try:
                con.close()
            except:
                pass

    def passive_sample(self):
        #TODO figure out if this belongs here
        # implement passive sampling
        # sampling data
        [self.containers[i].sample() for i in self.passive_containers if i != self.state]
