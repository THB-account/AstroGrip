from View.AbstractView import AbstractView

class PlotScreenView:
    def __init__(self):
        pass

    def isr_state_transition(self):
        raise NotImplementedError()
    
    def isr_state_action(self):
        raise NotImplementedError()

    def animate(self)