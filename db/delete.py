import json

def clean_item(item):
    """清理单个对象，只保留code、name和subLevelModelList字段"""
    # 保留需要的基础字段
    cleaned = {
        "code": item.get("code"),
        "name": item.get("name")
    }
    
    # 处理嵌套的子列表（如果存在）
    sub_list = item.get("subLevelModelList")
    if isinstance(sub_list, list):
        # 递归清理子列表中的每个元素
        cleaned["subLevelModelList"] = [clean_item(sub_item) for sub_item in sub_list]
    else:
        # 如果不是列表（如null），直接保留原始值
        cleaned["subLevelModelList"] = sub_list
    
    return cleaned

def clean_json_data(original_data):
    """清理整个JSON数据结构"""
    # 保留最外层的code和message
    result = {
        "code": original_data.get("code"),
        "message": original_data.get("message"),
        "zpData": []
    }
    
    # 处理zpData中的每个元素
    if isinstance(original_data.get("zpData"), list):
        result["zpData"] = [clean_item(item) for item in original_data["zpData"]]
    
    return result

文件路径='position.json'

# 示例用法
if __name__ == "__main__":
    # 假设原始数据为输入的JSON（这里使用用户提供的片段示例）
    original_json = open(文件路径, 'r', encoding='utf-8').read()
    
    # 解析原始JSON
    original_data = json.loads(original_json)
    
    # 清理数据
    cleaned_data = clean_json_data(original_data)
    
    # 保存清理后的JSON
    with open('cleaned_position.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
