# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json

from src.core.performance_tracker import PerformanceTracker


# Press the green button in the gutter to run the script.
import time

from src.core.performance_tracker import PerformanceTracker
import pdb

if __name__ == '__main__':
    # pdb.set_trace()
    json_text = open('input_configuration.json', 'r')
    y = json.load(json_text)
    print(y)
    tracker = PerformanceTracker(y)
    while True:
        tracker.main()
        time.sleep(90)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
