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
            # running a fuzzy search with a limit of 30 results to avoid performance issues
            c.execute(
                "SELECT * FROM characters WHERE name LIKE ? LIMIT ?",
                ("%" + query + "%", 30),
            )
            return c.fetchall()

    def query(self, query):
        output = []

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

    def copy(self, unicode):
        # copy the unicode to the clipboard
        pyperclip.copy(unicode)

    # TODO: Add a method to directly inject the unicode to the active input field

if __name__ == "__main__":
    Unicoder()
