# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json


class data :
    def __init__(self, designtype, designid, macs):
        self.designtype = designtype
        self.designid = designid
        self.macs = macs




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    json_text = open('data.json','r')
    y = json.load(json_text)
    print(y)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
