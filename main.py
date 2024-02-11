# Author: Lasith Manujitha
# Github: @z1nc0r3
# Description: A flow launcher plugin to find unicode characters
# Date: 2024-02-11

import sys, os
import json
import sqlite3

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, "lib"))
sys.path.append(os.path.join(parent_folder_path, "plugin"))

from flowlauncher import FlowLauncher
from rapidfuzz import process
import requests
import pyperclip


class Shortener(FlowLauncher):

    def query(self, query):
        output = []

        if query == "":
            output.append(
                {
                    "Title": "Enter a query to search unicode characters",
                    "SubTitle": "Enter a query to search unicode characters",
                    "IcoPath": "Images/icon.png",
                }
            )
            return output

        results = Shortener.fuzzy_search(query)

        for i in results:
            output.append(
                {
                    "Title": f"{i[0] + ' ⎯  ' + i[1]}",
                    "SubTitle": f"{i[3] + ' (' + str(i[4]) + ')'}",
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

    def fuzzy_search(query):
        conn = sqlite3.connect('./assets/unicode_characters.db')
        c = conn.cursor()
        c.execute("SELECT * FROM characters WHERE name LIKE ?", ('%' + query + '%',))
        results = c.fetchall()
        conn.close()
        return results

    def copy(self, tiny):
        pyperclip.copy(tiny)


if __name__ == "__main__":
    Shortener()
