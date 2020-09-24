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
import xlrd
from xlutils.copy import copy
from datetime import datetime
import time
from selenium.common.exceptions import NoSuchElementException
from beautifultable import BeautifulTable

wb = xlrd.open_workbook('Test_Data.xlsx')
# sheet name은 필요시, 엑셀 파일 시트 잘 확인해서 필요시 변경해주세요!!
sheet_tc = wb.sheet_by_name("CMA 금융사 TestCase") #CMA Result TestCase
sheet_fin1_idx = wb.sheet_by_name("CMA 증권사 index")
sheet_fin2_idx = wb.sheet_by_name("CMA 종금사 index")

total = 22
sum_pass = 0
sum_fail = 0
sum_nt = 0

fin_kind = 0
fin_idx = 0

# 한 페이지에서 로드할 수 있는 cma 상품 모두 로드
def load_invest():

    global sum_nt, sum_fail

    n = 37 # 총 상품 갯수

    for x in range(1, int(n / 10) + 1):

        wait = 0

        while True:

            # 20초 기다렸는데도 load되지 않았을때, timeout처리
            if wait > 20:
                screenshot()
                print("\x1b[1;31mFail\x1b[1;m - 결과 리스트 로드 timeout")
                sum_fail += 1
                return False

            elements = driver.find_elements(By.CLASS_NAME, "cardWrap_3dP8_")
            num = len(elements)

            if num > 0:
                break

            sleep(1)
            wait += 1

        elements[num - 1].location_once_scrolled_into_view

        sleep(2)

    return True

def select_fin():

    global fin_kind, fin_idx, sum_nt

    try:
        # 증권사/종금사 선택하기 버튼
        driver.find_element(By.CLASS_NAME, "popupButton_2i004").click()

        sleep(2)

        fin_kind = int(sheet_tc.cell(i, 1).value) # 증권사/종금사
        fin_idx = int(sheet_tc.cell(i, 2).value) # 증권사 idx / 종금사 idx

        if fin_kind == 1:
            fin_name = sheet_fin1_idx.cell(fin_idx, 1).value
        elif fin_kind == 2:
            fin_name = sheet_fin2_idx.cell(fin_idx, 1).value
        else:
            print("N/T - 증권사, 종금사 종류가 잘못입력됨")
            sum_nt += 1
            return False

        if fin_idx > 5:
            driver.find_element(By.CSS_SELECTOR, ".search_3T8DM > input").send_keys(fin_name)
            fin_checkbox = driver.find_element(By.CSS_SELECTOR, ".result_kF6qg > :nth-child(" + str(fin_kind) + ") > ul > :nth-child(1)")
        else:
            fin_checkbox = driver.find_element(By.CSS_SELECTOR, ".result_kF6qg > :nth-child(" + str(fin_kind) + ") > ul > :nth-child(" + str(fin_idx) + ")")

        fin_checkbox.click()

        sleep(1)

        driver.find_element(By.LINK_TEXT, "완료").click()

        sleep(2)

    except NoSuchElementException:
        print("N/T - 증권사/종금사 선택 요소를 찾지 못함")
        sum_nt += 1
        return False

    return True

def confirm_fin():

    global sum_nt, sum_fail

    if fin_kind == 1:
        fin_name = sheet_fin1_idx.cell(fin_idx, 1).value
    elif fin_kind == 2:
        fin_name = sheet_fin2_idx.cell(fin_idx, 1).value
    else:
        print("N/T - 증권사, 종금사 종류가 잘못입력됨")
        sum_nt += 1
        return False

    num = len(driver.find_elements(By.CLASS_NAME, "cardWrap_3dP8_"))

    if num == 0:
        print("N/T - " + fin_name + ": 노출되는 상품이 없습니다.")
        sum_nt += 1
        return False

    if num > 3:
        num = 3

    for x in range(0, num):

        try:
            driver.find_element(By.CSS_SELECTOR, ".cardsContainer_2d0E9 > :nth-child(" + str(x + 1) + ") > .body_3UwsQ > .buttonGroup_1CD2Q > :nth-child(1)").click()
        except NoSuchElementException:
            print("N/T - 상세보기 버튼을 찾지 못함")
            sum_nt += 1
            return False

        sleep(2)

        if fin_name not in driver.title:
            screenshot()
            print("\x1b[1;31mFail\x1b[1;m - 선택한 증권사/종금사와 일치하지 않는 상품입니다.")
            sum_fail += 1
            return False

        try:
            driver.find_element(By.LINK_TEXT, "결과 리스트로").click()
        except NoSuchElementException:
            print("N/T - 결과 리스트로 버튼을 찾지 못함")
            sum_nt += 1
            return False

        wait = 0

        while True:
            # 20초 기다렸는데도 load되지 않았을때, timeout처리
            if wait > 20:
                screenshot()
                print("\x1b[1;31mFail\x1b[1;m - 결과 리스트 로드 timeout")
                sum_fail += 1
                return False

            if len(driver.find_elements(By.CLASS_NAME, "cardWrap_3dP8_")) > 0:
                break

    return True

def screenshot():

    file_dir = "screenshot/cmafintest/"

    if i < 10:
        screenshot_name = "cmafintest00" + str(i) + "_fail_" + datetime.today().strftime("%Y%m%d%H%M") + ".png"
    else:
        screenshot_name = "cmafintest0" + str(i) + "_fail_" + datetime.today().strftime("%Y%m%d%H%M") + ".png"

    driver.save_screenshot(file_dir + screenshot_name)

#백그라운드 옵션
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("window-size=1920x1080")
chrome_options.add_argument("headless")

# main 함수 시작

print("------------------------테스트 시작------------------------")

start = time.time()

for i in range(1, total + 1):

    # 크롬드라이버를 백그라운드로 돌리고 싶을 때(또는 다른 옵션을 추가하고 싶을 때), 크롬드라이버 디렉토리 뒤에 옵션 추가
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')

    if i < 10:
        print("cmafintest00" + str(i) + " Running...")
    else:
        print("cmafintest0" + str(i) + " Running...")

    driver.get("https://banksalad.com/cma/questions")

    sleep(2)

    # 결과보기 버튼 load 못했을 때, N/T 처리
    try:
        driver.find_element(By.LINK_TEXT, "결과보기").click()
    except NoSuchElementException:
        print("N/T - 결과보기 버튼을 찾지못함")
        sum_nt += 1
        driver.quit()
        continue

    cma_wait = 0

    while True:

        # 20초 기다렸는데도 load되지 않았을때, timeout처리
        if cma_wait > 20:
            screenshot()
            print("\x1b[1;31mFail\x1b[1;m - 결과 리스트 로드 timeout")
            sum_fail += 1
            driver.quit()
            continue

        num = len(driver.find_elements(By.CLASS_NAME, "cardWrap_3dP8_"))

        if num > 0:
            break

        sleep(1)
        cma_wait += 1

    # 가입방법 - 비대면 가입, 콜센터, 영업점 모두 체크
    driver.find_element(By.CSS_SELECTOR, ".filterContainer_2A76Q > div > .listWrap_119TX > :nth-child(1) > ul > :nth-child(2) > div > ul > :nth-child(2) > div").click()
    driver.find_element(By.CSS_SELECTOR, ".filterContainer_2A76Q > div > .listWrap_119TX > :nth-child(1) > ul > :nth-child(2) > div > ul > :nth-child(3) > div").click()

    sleep(2)

    # 결과 페이지 내 투자 상품 모두 load
    if not load_invest():
        driver.quit()
        continue

    if not select_fin():
        driver.quit()
        continue

    if not confirm_fin():
        driver.quit()
        continue

    sum_pass += 1
    print("\x1b[1;34mPass\x1b[1;m")
    driver.quit()

table = BeautifulTable()

table.column_headers = ["Total", "Pass", "Fail", "N/T"]
table.append_row([total, sum_pass, sum_fail, sum_nt])

print("------------------------테스트 결과------------------------")
print("실행 날짜: " + datetime.today().strftime("%Y-%m-%d"))
print("총 실행시간: " + str(int(time.time() - start)) +  "s")
print("한 케이스당 평균 실행시간: " + str(int((time.time() - start)/total)) + "s")
print(table)

