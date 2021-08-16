# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json

from src.core.performance_tracker import PerformanceTracker


# Press the green button in the gutter to run the script.
import time

from src.core.performance_tracker import PerformanceTracker
import pdb
# from vepy_api import *

if __name__ == '__main__':
    # pdb.set_trace()
    json_text = open('input_configuration.json', 'r')
    y = json.load(json_text)
    print(y)
    tracker = PerformanceTracker(y)
    # while True:
    # Logic to stream
    # p1 = Packet()
    # start(phy=1, burst="Cont", packet=p1)
    # time.sleep(10)
    # start(phy=2, burst="Cont", packet=p1)
    # time.sleep(10)
    # stop(phy=1)
    # stop(phy=2)

    time.sleep(30)
    tracker.main()
    # time.sleep(30)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
