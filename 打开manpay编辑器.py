import sys

from PyQt5.QtWidgets import QApplication

from jsoneditonly import JsonEditor

app = QApplication(sys.argv)
keys = ['配置名称',  '参数',  "操作"]
file_name = "wanpayconfig.json"

editor = JsonEditor(keys,file_name)
editor.show()
sys.exit(app.exec_())