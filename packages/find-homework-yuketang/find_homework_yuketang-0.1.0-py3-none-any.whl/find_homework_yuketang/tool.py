from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import requests
import json
import os
from datetime import datetime
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "university-id": "0",
    "uv-id": "0",
    "xt-agent": "web",
    "xtbz": "ykt"
}

# 获取网页cookies
def getCookies():
    url = 'https://www.yuketang.cn/web'
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    init_url = driver.current_url
    try:
        print("等待用户扫描二维码")
        WebDriverWait(driver, 30).until(
            lambda driver: driver.current_url != init_url
        )
        cookies = driver.get_cookies()
        driver.quit()
    except TimeoutException:
        print("登录失败")
        driver.quit()
        exit(1)
    finally:
        print("成功获取cookies")
        return cookies

# 获得课程列表
def getClasses(cookies):
    url = 'https://www.yuketang.cn/v2/api/web/courses/list?identity=2'
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        try:
            json_data = response.json()
            if json_data['errmsg'] == "Success":
                return json_data['data']['list']
            else:
                print("获取JSON文件失败")
                exit(1)
        except ValueError:
            print("非有效JSON格式")
            exit(1)
    else:
        print(f'错误 {response.status_code}: {response.content}')
        exit(1)

# 获取本地课程
def getLocalChoseClass():
    if os.path.exists('./choosed_class.json'):
        print("加载本地已选择课程")
        with open('./choosed_class.json', 'r', encoding='utf-8') as file:
            return json.load(file)["data"]
    else:
        print("本地没有已选择课程")
        return None

# 读入本地课程
def writeLocalChoseClass(class_list):
    with open('./choosed_class.json', 'w', encoding='utf-8') as file:
        json.dump({
            "data": class_list
        }, file, ensure_ascii=False, indent=4)
    print('成功保存')
    
# 获取当前课程表的作业
def queryClassListWork(class_list, cookies):
    homework = []
    for _class in class_list:
        url = f'https://www.yuketang.cn/v2/api/web/logs/learn/{_class['classroom_id']}?actype=-1&page=0&offset=20&sort=-1'
        response = requests.get(url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            json_data = response.json()
            if json_data['errmsg'] == "Success":
                logs = json_data['data']['activities']
                for log in logs:
                    if 'deadline' in log and log['status'] == 1:
                        homework.append({ **log, 'name': _class['name'] })
            else:
                print("无法获取JSON文件")
        else:
            print(f'错误 {response.status_code}: {response.content}')
    homework.sort(key=lambda log: log['deadline'])
    for indice, item in enumerate(homework, 1):
        print(f'{indice}.课程名：{item['name']}\n作业名：{item['title']}\n截止日期：{datetime.fromtimestamp(int(item['deadline']) / 1000).strftime('%Y-%m-%d %H:%M:%S')}\n')