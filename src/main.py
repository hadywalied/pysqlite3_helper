# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    json_text = open('data.json', 'r')
    y = json.load(json_text)
    print(y["objects_list"][0]["designid"])
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
