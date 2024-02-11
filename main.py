# Author: Lasith Manujitha
# Github: @z1nc0r3
# Description: A flow launcher plugin to find unicode characters
# Date: 2024-02-04

import sys, os
import json

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, "lib"))
sys.path.append(os.path.join(parent_folder_path, "plugin"))

from flowlauncher import FlowLauncher
import webbrowser
import requests
import pyperclip


class Shortener(FlowLauncher):

    def query(self, query):
        output = []

        with open("./assets/unicode_data.json", "r", encoding="utf-8") as f:
            unicode_data = json.load(f)
        
        

        output.append(
            {
                "Title": f"Found {(unicode_data[0])} unicode characters",
                "SubTitle": "Click to copy",
                "IcoPath": "Images/copy.png",
            }
        )

        """ output.append(
            {
                "Title": "Click to open in browser",
                "SubTitle": f"{tiny}",
                "IcoPath": "Images/open.png",
                "JsonRPCAction": {"method": "open_url", "parameters": [f"{tiny}"]},
            }
        ) """

        return output

    def copy(self, tiny):
        pyperclip.copy(tiny)

    def open_url(self, url):
        webbrowser.open(url)


if __name__ == "__main__":
    Shortener()
