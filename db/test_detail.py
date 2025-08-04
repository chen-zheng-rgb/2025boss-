import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from time import sleep



salary_xpath='//*[@id="main"]/div[1]/div/div/div[1]/div[2]'
href="https://www.zhipin.com/job_detail/76d4bbd8cd649f6e03B63Ny-GFZU.html"

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
service=webdriver.edge.service.Service(r"C:\Program Files\msedgedriver.exe")
browser = webdriver.Edge(service=service)
browser.get(href)
sleep(10)
text=browser.find_element(By.XPATH,salary_xpath).text
print(text)