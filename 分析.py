f= open(file="2024_08_26.txt",encoding="Utf-8",mode="r")
for i in f.readlines():
    context=i.strip()
    if "aLiveTask" in context:
        print(context)
# 08-26 09:02:20
