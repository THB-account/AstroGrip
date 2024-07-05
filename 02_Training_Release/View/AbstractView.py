class AbstractView:
    def __init__(self):
        pass

    # aka plot button
    def isr_state_transition(self):
        raise NotImplementedError()
    
    # aka SOP button
    def isr_state_action(self):
        raise NotImplementedError()

    def animate(self):
        raise NotImplementedError()
