# Author: Lasith Manujitha
# Github: @z1nc0r3
# Description: A flow launcher plugin to find unicode characters
# Date: 2024-02-11

import sys, os
import sqlite3
from pathlib import Path

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, "lib"))
sys.path.append(os.path.join(parent_folder_path, "plugin"))

from flowlauncher import FlowLauncher
from rapidfuzz import process
import pyperclip


class Unicoder(FlowLauncher):
    DB_PATH = Path(__file__).parent / "assets" / "unicode_characters.db"

    @staticmethod
    def fuzzy_search(query):
        with sqlite3.connect(Unicoder.DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute(
                "SELECT * FROM characters WHERE name LIKE ? LIMIT ?",
                ("%" + query + "%", 40),
            )
            return c.fetchall()

    def query(self, query):
        output = []

        if not query:
            output.append(
                {
                    "Title": "Enter a query to search unicode characters",
                    "IcoPath": "Images/icon.png",
                }
            )
            return output

        results = self.fuzzy_search(query)

        for i in results:
            output.append(
                {
                    "Title": f"{i[0] + ' ⎯  ' + i[1]}",
                    "SubTitle": f"{i[3] + ' (' + str(i[4]) + ')'}",
                    "IcoPath": "Images/copy.png",
                    "JsonRPCAction": {"method": "copy", "parameters": [i[0]]},
                }
            )

        return output

    @staticmethod
    def copy(unicode):
        pyperclip.copy(unicode)


if __name__ == "__main__":
    Unicoder()
