import plotext as pltx
from collections import deque
from time import time

ar = deque(maxlen=5)
def f(ar):
    t = time()
    return [x-t for x in ar]

for i in range(5):
    ar.append(i)

pltx.clf()
pltx.title("your doom")
pltx.scatter(f(ar),range(5))

pltx.show()