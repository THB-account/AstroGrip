import keyboard
from model.model import on_start_up, action_loop, isr_state_transition, isr_state_action
from model.model import on_shutdown





no_escape = True
def esc_key_action(keyboard_event):
    global no_escape
    no_escape=False
keyboard.on_release_key('esc',esc_key_action)

on_start_up()
try:
    while no_escape:
        action_loop()

finally:
    # do some cleaning up, after for example an KeyboardInterrupt came
    on_shutdown()