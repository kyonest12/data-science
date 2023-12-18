import os

import requests
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_tokenApi():
    token_api = ""
    driver = webdriver.Chrome()

    # Mở trang web
    driver.get("https://www.visualcrossing.com/")

    try:
        dismiss_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.btn.btn-sm.btn-primary.col-lg-3[data-bs-dismiss="modal"]'))
        )
        # Bấm vào phần tử đầu tiên tìm thấy
        dismiss_button.click()
    except Exception as e:
        print(f"Không tìm thấy phần tử: {e}")

    try:
        login_page_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[title="Sign in"]'))
        )
        login_page_element.click()
        # Điền tài khoản và mật khẩu
        email_input = driver.find_element(By.ID, "exampleInputEmail1")
        password_input = driver.find_element(By.ID, "exampleInputPassword1")

        email_input.send_keys("luongminh30092002@gmail.com")
        password_input.send_keys("123456")

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.modal-footer .btn.btn-primary'))
        )

        login_button.click()

        your_account_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[title="Your Account"]'))
        )
        your_account_link.click()

        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'mb-3.col-12.col-md-6.col-xl-4'))
        )

        # Lấy giá trị của class "fs-sm" của phần tử thứ 2
        if len(elements) > 1:
            token_api = elements[1].find_element(By.CLASS_NAME, 'fs-sm').text

            print(f"Giá trị token api: {token_api}")
        else:
            print("Không tìm thấy đủ số phần tử")

    except Exception as e:
        print(f"Không thể đăng nhập: {e}")

    logout_page_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[title="Sign out"]'))
    )
    logout_page_element.click()
    # Đóng trình duyệt

    driver.quit()
    return token_api


token = get_tokenApi()
end = datetime.now() - timedelta(days=1)
begin = datetime.now() - timedelta(days=1)
print(end.strftime("%Y-%m-%d"))
print(begin.strftime("%Y-%m-%d"))

import urllib.request
import urllib.error
import sys

import json



with open('data.json', 'r', encoding='utf-8') as file:
    data_j = json.load(file)

try:
    api = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/H%C3%A0%20N%E1%BB%99i%2C%20Gi%E1%BA%A3i%20Ph%C3%B3ng/{begin.strftime('%Y-%m-%d')}/{end.strftime('%Y-%m-%d')}?unitGroup=metric&key={token}&contentType=json"
    print(api)
    ResultBytes = urllib.request.urlopen(api)
    # Parse the results as JSON
    jsonData = json.load(ResultBytes)
    data_j.append(jsonData)

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data_j, file, indent=4, ensure_ascii=False)


except urllib.error.HTTPError as e:
    ErrorInfo = e.read().decode()
    print('Error code: ', e.code, ErrorInfo)
    sys.exit()


