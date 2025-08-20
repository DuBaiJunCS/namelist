import sys

from PyQt5.QtWidgets import QApplication

from jsoneditonly import JsonEditor

app = QApplication(sys.argv)
keys = ["key","value","mark"]
file_name = "config.json"

editor = JsonEditor(keys,file_name)
editor.show()
sys.exit(app.exec_())