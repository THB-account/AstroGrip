from model.model import on_start_up, action_loop, isr_state_transition, isr_state_action
from model.model import on_shutdown

import signal

# just add this to be sure, for shutdownbehavior on KeyboardInterrupt
signal.signal(signal.SIGINT, on_shutdown)



on_start_up()
try:
    while no_escape:
        action_loop()

finally:
    # do some cleaning up, after for example an KeyboardInterrupt came
    on_shutdown()
