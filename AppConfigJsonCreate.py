import json
from dataclasses import dataclass, asdict
from typing import List

@dataclass
class AppConfig:
    packageName: str
    appName: str
    regexList: List[str]

# 创建实体对象
config1 = AppConfig(
    packageName="com.scrcu.ebap.mer",
    appName="惠支付商户版",
    regexList=[r"收款(\d+(?:\.\d+)?)元"]
)

config2 = AppConfig(
    packageName="com.example.app",
    appName="测试应用",
    regexList=[r"金额(\d+(?:\.\d+)?)元"]
)

# 放入列表，表示多个对象
configs = [config1]

# 转成 JSON 字符串，用于传输
json_str = json.dumps([asdict(c) for c in configs], ensure_ascii=False)

# 输出（网络传输时可以直接使用 json_str）
print(json_str)
