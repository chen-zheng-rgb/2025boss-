from selenium import webdriver
from selenium.webdriver.edge.service import Service

# 使用Service类和原始字符串路径
service = Service(r"C:\Program Files\msedgedriver.exe")  # 在路径前加r表示原始字符串
url="https://www.baidu.com"
driver = webdriver.Edge(service=service)
driver.get(url)