import csv
import timeit
import collections
import time


speed_test= True
if not speed_test:
    with open("data.csv",'w',newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(["col1","col2"])
        spamwriter.writerow([1,2])


    with open("data.csv","r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)
else:
    iterations = 10000
    MAX_LEN = 100
    d = collections.deque(maxlen=MAX_LEN)
    t = collections.deque(maxlen=MAX_LEN)
    for i in range(MAX_LEN):
        d.append(i)
        t.append(time.time())

    def f1():
        with open("data.csv",'w',newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            [spamwriter.writerow([meas,t]) for meas,t in zip(d,t)]


    def f2():
        with open("data.csv",'w',newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            spamwriter.writerows(zip(d,t))

    print("f1: ",timeit.timeit(f1,number=iterations))
    print("f2: ",timeit.timeit(f2,number=iterations))