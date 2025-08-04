import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from time import sleep
import json

def get_job_detail_urls(citycode, positioncode,num):
    # 构建目标URL
    url = f"https://www.zhipin.com/web/geek/jobs?query=&city={citycode}&position={positioncode}"
    
    # 配置浏览器选项
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

# 打开BOSS直聘登录页
    browser.get("https://www.zhipin.com/user/login.html")
    print("请在30秒内手动完成登录...")
    sleep(30)  # 手动登录时间窗口   
    # 登录成功后保存Cookie到本地
    cookies = browser.get_cookies()
    with open("boss_cookies.json", "w", encoding="utf-8") as f:
        json.dump(cookies, f, ensure_ascii=False)
    # 关闭浏览器


    browser.get(url)
    # 刷新页面使Cookie生效
    browser.refresh()
    
    
    fullhref = {}
    sleep(20)  # 等待页面加载

    try:
    # 1. 定位左侧滚动容器
        scroll_container = browser.find_element(By.XPATH, '//*[@id="wrap"]/div[2]/div[3]/div/div/div[1]')
    
        for i in range(1, num+1):
        # 2. 先尝试获取当前页的元素（避免重复滚动）
            details_xpath = f'//*[@id="wrap"]/div[2]/div[3]/div/div/div[1]/ul/div[{i}]/div/li/div[1]/div/a'
            try:
                href = browser.find_element(By.XPATH, details_xpath).get_attribute('href')
                fullhref[i] = href
                print(href)
            except:
            # 3. 若元素未找到，滚动容器加载新内容
            # 滚动到容器底部（垂直滚动）
                browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scroll_container)
            # 若为水平滚动（左侧横向滚动），则使用：
            # browser.execute_script("arguments[0].scrollLeft = arguments[0].scrollWidth;", scroll_container)
            
            # 4. 增加等待时间（根据网页加载速度调整，建议3-5秒）
                sleep(3)
            # 重新获取元素
                href = browser.find_element(By.XPATH, details_xpath).get_attribute('href')
                fullhref[i] = href
                print(href)
        
            sleep(1)
        return fullhref  
    finally:
        browser.quit()
# 使用示例：
# urls = get_job_detail_urls(101010100, 100122,2)
# print("获取到的URL:", urls)
