import requests
import json  


def update_data(url, filename):
    # 添加请求头，模拟浏览器访问，避免被拒绝
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功（状态码200）
        data = response.json()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)  # ensure_ascii=False保证中文正常显示，indent=2格式化输出
        print(f"{filename}数据更新完成")
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误：{e}")
    except json.JSONDecodeError:
        print("JSON解析错误")
    except Exception as e:
        print(f"其他错误：{e}")

positiondata_url = "https://www.zhipin.com/wapi/zpCommon/data/position.json"
citydata_url = "https://www.zhipin.com/wapi/zpCommon/data/city.json"

# 调用更新数据函数
update_data(positiondata_url, 'position.json')
update_data(citydata_url, 'city.json')