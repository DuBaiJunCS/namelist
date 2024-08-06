import sys

from PyQt5.QtWidgets import QApplication

from jsoneditonly import JsonEditor

app = QApplication(sys.argv)
keys = ["更新时间","main","url"]
file_name = "update.json"

editor = JsonEditor(keys,file_name)
editor.show()
sys.exit(app.exec_())