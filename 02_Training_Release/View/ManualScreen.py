from View.AbstractView import AbstractView
import plotext as pltx
from plotext import xticks,yticks,clf,show,text,tw,th
from textwrap import wrap
from itertools import chain

class ManualScreenView(AbstractView):
    def __init__(self, manual_text):

        # terminal width -2 because two characters are the sidebars
        # -4 as little spacing
        self.lines = wrap(manual_text,width=tw()-2-4,break_long_words=False,replace_whitespace=False)
        self.lines = list(chain.from_iterable(line.split('\n') for line in self.lines))
        # just for comparison
        self.num_lines = len(self.lines)
        # top and bottom line = 2
        # -1 from plotext that is not used
        # -2 at the bottom
        # limit
        self.display_text_num_lines = th() - 3 -2
        self.line_idx = 0
        self.step_size = 2
        self.__build_text()
        
        
    def __build_text(self):
        # build text everytime a change is made so it is not rebuild every animation frame
        self.display_text= '\n'.join(self.lines[self.line_idx: min(self.num_lines,self.line_idx + self.display_text_num_lines)])
        
    # aka SOP button
    def isr_state_action(self):
        # if already at maximum return to beginning
        # otherwise increment correspondingly while respecting bounds
        if self.line_idx == self.num_lines - self.display_text_num_lines:
            self.line_idx = 0
        elif self.line_idx <= self.num_lines - self.display_text_num_lines -  self.step_size:
            self.line_idx += self.step_size
        else: # if no adequate step size is possible set to limit
            self.line_idx = self.num_lines - self.display_text_num_lines
        
        self.__build_text()
        

    def animate(self):
        pltx.clf()
        pltx.text(self.display_text, x=0,y=0,alignment="left")
        # center text to top left corner
        pltx.xlim(0.,1.)
        pltx.ylim(0.,-1.)
        pltx.xticks([])
        pltx.yticks([])
        pltx.show()