from detail_url import get_job_detail_urls
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from time import sleep
import pandas as pd 
import json

num=15
positioncode=140101

urls = get_job_detail_urls(101010100, positioncode,num)
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
options.add_argument("--window-size=1366,768")  # 固定窗口大小（避免默认尺寸被识别）
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")

    
# 初始化浏览器并访问页面
service = webdriver.edge.service.Service(r"C:\Program Files\msedgedriver.exe")
browser = webdriver.Edge(service=service, options=options)


state_xpath='//*[@id="main"]/div[1]/div/div/div[1]/div[1]'
job_xpath='//*[@id="main"]/div[1]/div/div/div[1]/div[2]/h1'
salary_xpath='//*[@id="main"]/div[1]/div/div/div[1]/div[2]/span'
city_xpath='//*[@id="main"]/div[1]/div/div/div[1]/p/a'
brand_xpath='//*[@id="main"]/div[1]/div/div/div[1]/p/span[@class="brand-name"]'
experience_xpath='//*[@id="main"]/div[1]/div/div/div[1]/p/span[@class="text-desc text-experiece"]'
degree_xpath='//*[@id="main"]/div[1]/div/div/div[1]/p/span[@class="text-desc text-degree"]'
tag_xpath='//*[@id="main"]/div[1]/div/div/div[2]/div[2]'
description_xpath='//*[@id="main"]/div[3]/div/div[2]/div[1]/div[3]'
df = pd.DataFrame(columns=['state','job','salary','city','brand','experience','degree','tag','description'])

browser.get("https://www.zhipin.com")  # 关键：先加载网站，使 Cookie 生效



# 读取并通过浏览器实例添加 Cookie（使用 browser.add_cookie）
with open("boss_cookies.json", "r", encoding="utf-8") as f:
    cookies = json.load(f)
for cookie in cookies:
    # 解决可能的 domain 格式问题（部分网站需要去除域名前的点）
    if "domain" in cookie and cookie["domain"].startswith("."):
        cookie["domain"] = cookie["domain"][1:]  # 去除域名前的 "."
    browser.add_cookie(cookie)  # 正确：通过浏览器实例添加 Cookie

# 刷新页面使 Cookie 生效
browser.refresh()

sleep(3)  # 等待刷新完成

browser.execute_script("""
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    })
""")

for i in range(1,num+1):
    url=urls[i]
    browser.get(url)
    sleep(4)  # 等待页面加载
    #没找到跳过
    try:
        state=browser.find_element(By.XPATH,state_xpath).text
    except:
        state='无'
    job=browser.find_element(By.XPATH,job_xpath).text
    salary=browser.find_element(By.XPATH,salary_xpath).text
    city=browser.find_element(By.XPATH,city_xpath).text
    try:
        brand=browser.find_element(By.XPATH,brand_xpath).text
    except:
        brand='无'
    experience=browser.find_element(By.XPATH,experience_xpath).text
    degree=browser.find_element(By.XPATH,degree_xpath).text
    try:
        tag=browser.find_element(By.XPATH,tag_xpath).text
    except:
        tag='无'
    description=browser.find_element(By.XPATH,description_xpath).text
    #写入excel表格中
    df.loc[len(df)]=[state,job,salary,city,brand,experience,degree,tag,description]
    #程序结束前保存一次
df.to_excel(str(positioncode)+'zhipin.xlsx',index=False)
browser.quit()
