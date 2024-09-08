import sys

from PyQt5.QtWidgets import QApplication

from jsoneditonly import JsonEditor

app = QApplication(sys.argv)
keys = ['机器码', '标志', '参数', '任务名', '最晚执行时间', "操作"]
file_name = "task.json"

editor = JsonEditor(keys,file_name)
editor.show()
sys.exit(app.exec_())

