#-*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium import webdriver
from datetime import datetime
import time
from selenium.common.exceptions import NoSuchElementException
from beautifultable import BeautifulTable
import json
from selenium.webdriver.common.alert import Alert
from gspreadAPI import GC, TESTCASE_CARD_URL

doc = GC.open_by_url(TESTCASE_CARD_URL)
cardresulttest_tc = doc.worksheet('cardresulttest')

total = len(cardresulttest_tc.col_values(1)) - 1
sum_pass = 0
sum_fail = 0
sum_nt = 0

def tc_to_json():

    col = len(cardresulttest_tc.row_values(1)) - 1

    str_json = '{'

    for x in range(0, col + 1):

        if x != 0:
            str_json += ", "

        str_json += '"' + cardresulttest_tc.row_values(1)[x] + '": "' + cardresulttest_tc.row_values(i + 1)[x] + '"'

    str_json += "}"

    return json.loads(str_json)

def load_result():

    wait = 0

    while True:

        if wait > 20:
            return False

        elements = driver.find_elements(By.CLASS_NAME, "head_32_Bt")
        num = len(elements)

        if num > 0:
            break

        sleep(1)
        wait += 1

    return True

def select():

    global sum_nt

    try:
        card_all = driver.find_elements(By.CLASS_NAME, "all_1idVF")[0]
        card_all.click()

        sleep(1)

        temp = tc_json["카드 종류"].split(", ")
        card_checkbox = driver.find_elements(By.CSS_SELECTOR, ".filter_mgC68 > div > :nth-child(1) > :nth-child(2) > li")
        for x in range(0, len(temp)):
            print(temp[x])
            for y in range(0, len(card_checkbox)):
                if card_checkbox[y].text == temp[x]:
                    card_checkbox[y].click()
                    break

    except NoSuchElementException:
        sum_nt += 1
        print("N/T - 카드 종류 항목을 찾지못함")
        return False

    if not load_result():
        sum_nt += 1
        print("N/T - 카드 종류 선택 후 결과리스트 로드되지 않음")
        return False

    try:
        driver.find_element(By.XPATH, "//label[contains(text(), '" + tc_json["혜택 종류"] + "')]").click()
    except NoSuchElementException:
        sum_nt += 1
        print("N/T - 혜택 종류 항목을 찾지못함")
        return False

    if not load_result():
        sum_nt += 1
        print("N/T - 혜택 종류 선택 후 결과리스트 로드되지 않음")
        return False

    try:

        if tc_json["연회비이벤트"] == "TRUE":
            driver.find_element(By.XPATH, "//label[@for='promotion-annual_cost']").click()

            if not load_result():
                sum_nt += 1
                print("N/T - 연회비 이벤트 여부 선택 후 결과리스트 로드되지 않음")
                return False

    except NoSuchElementException:
        sum_nt += 1
        print("N/T - 연회비 이벤트 체크박스를 찾지못함")
        return False

    return True

# fail 당시의 화면을 캡쳐하여 screenshot/cardresulttest 폴더에 저장
def screenshot():

    file_dir = "screenshot/cardresulttest/"

    if i < 10:
            screenshot_name = "cardresulttest00" + str(i) + "_fail_" + datetime.today().strftime("%Y%m%d%H%M") + ".png"
    else:
        screenshot_name = "cardresulttest0" + str(i) + "_fail_" + datetime.today().strftime("%Y%m%d%H%M") + ".png"

    driver.save_screenshot(file_dir + screenshot_name)

print("------------------------테스트 시작------------------------")

start = time.time()

#백그라운드 옵션
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("window-size=1920x1080")
chrome_options.add_argument("headless")

for i in range(1, total + 1):

    driver = webdriver.Chrome('/Users/97chos/Downloads/web_automation-master/chromedriver')

    if i < 10:
        print("cardtest00" + str(i) + " Running...")
    else:
        print("cardtest0" + str(i) + " Running...")

    driver.get("https://banksalad.com/cards/questions")

    sleep(1)

    try:
        driver.find_element(By.XPATH, "//label[contains(text(), '신용')]").click()
        driver.find_element(By.XPATH, "//label[contains(text(), '체크')]").click()
        driver.find_element(By.XPATH, "//label[contains(text(), '하이브리드')]").click()
        driver.find_element(By.XPATH, "//label[contains(text(), '할인/적립')]").click()
        driver.find_element(By.XPATH,  "//button[@class='tag_1jHZn' and contains(text(), '100만')]").click()
    except NoSuchElementException:
        sum_nt += 1
        print("N/T - 카드종류, 혜택종류, 사용금액을 입력 칸을 찾지 못함")
        continue

    sleep(1)

    try:
        driver.find_element(By.LINK_TEXT, "결과보기").click()
    except NoSuchElementException:
        sum_nt += 1
        print("N/T - '결과보기'를 찾지못함")
        continue

    Alert(driver).accept()

    if not load_result():
        sum_nt += 1
        print("N/T - 결과 리스트 로드되지 않음")
        driver.quit()
        continue

    tc_json = tc_to_json()

    if not select():
        driver.quit()
        continue
