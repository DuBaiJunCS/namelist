import json

def validate_and_print_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print("JSON is valid. Content:")
            print(json.dumps(data, indent=4, ensure_ascii=False))
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: The file is not valid JSON. Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# 示例用法
file_path = 'task.json'  # 替换为你的JSON文件路径
validate_and_print_json(file_path)
