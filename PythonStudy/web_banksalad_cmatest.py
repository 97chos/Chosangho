# -*- coding: utf-8 -*-

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
from urllib import parse

wb = xlrd.open_workbook('Test_Data.xlsx')
sheet_tc = wb.sheet_by_name("BEST CMA TestCase")  # BEST CMA TestCase

total = 49
sum_pass = 0
sum_fail = 0
sum_nt = 0

lst_perf = ['', '', '', '', '', '', '']
lst_func = ['', '', '', '', '']


def check():
    global sum_nt
    balance_idx = int(sheet_tc.cell(i, 1).value)

    try:
        # 평균 잔액 버튼 클릭
        driver.find_element(By.CSS_SELECTOR, "li:nth-child(" + str(balance_idx) + ") > button").click()
        sleep(1)

        # 실적 체크
        for x in range(1, len(lst_perf)):
            lst_perf[x] = str(sheet_tc.cell(i, x + 1).value)

            if bool(lst_perf[x]):
                driver.find_element(By.CSS_SELECTOR, ".item_3aRCD:nth-child(" + str(x + 1) + ") > label").click()
                # 실적 체크박스는 전체 체크도 있어서 +1 해줘야돼요!
                sleep(1)

        # 통장 기능 체크
        for x in range(1, len(lst_func)):
            lst_func[x] = str(sheet_tc.cell(i, x + 7).value)

            if bool(lst_func[x]):
                driver.find_element(By.CSS_SELECTOR, ".item_2l67q:nth-child(" + str(x) + ") > label").click()
                sleep(1)

    except NoSuchElementException:
        sum_nt += 1
        print("N/T - 입력 항목을 찾지못함")
        return False

    return True

# 한 페이지에서 로드할 수 있는 상품 모두 로드
def load_invest():

    global sum_fail, sum_nt
    wait = 0

    n = 37 #총 상품 갯수

    for x in range(1, int(n / 10) + 1):

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

        if num == x * 10:
            elements[x * 10 - 1].location_once_scrolled_into_view
            sleep(2)
        else:
            elements[num - 1].location_once_scrolled_into_view
            sleep(2)
            break

    return True

#결과 페이지에서 월 평균잔액과, 이자금액이 이전 화면과 동일한지 확인
def confirm_result():

    global sum_fail, sum_nt

    sheet_bal_idx = wb.sheet_by_name("평균 잔액 index")  # 잔액 index sheet
    sheet_func_idx = wb.sheet_by_name("통장기능 index") # 통장 기능 index sheet
    balance_idx = int(sheet_tc.cell(i, 1).value)
    balance = int(sheet_bal_idx.cell(balance_idx, 1).value)

    try:
        # 월 평균잔액이 보일때까지 scroll
        driver.find_element(By.CSS_SELECTOR, ".balanceContainer_3al0D > div > label > span").location_once_scrolled_into_view
        text_balance = driver.find_element(By.CSS_SELECTOR, ".balanceContainer_3al0D > div > label > span").text

        # 결과 페이지에 노출되는 월 평균잔액과 입력 페이지에서 선택한 월 평균잔액이 일치하는지 확인
        if balance != int(text_balance.replace(",", "")):
            sum_fail += 1
            print("\x1b[1;31mFail\x1b[1;m - cma 분석 결과 페이지 상단에 선택한 월 평균잔액이 정상적으로 노출되지 않습니다.")
            print("기대결과값: " + format(balance, ","))
            print("실제결과값: " + text_balance)
            screenshot()
            return False

    except NoSuchElementException:
        sum_nt += 1
        print("N/T - 분석 결과 페이지 상단 월 평균잔액을 찾지못함")
        return False

    try:
        # 결과 페이지 최 상단에 노출되는 상품의 연 이자 금액과 입력 페이지에 노출되는 예상 연 이자금액이 일치하는지 확인
        next_interest = driver.find_element(By.CSS_SELECTOR,".resultsContainer_24LR6 > :nth-child(4) > :nth-child(1) > :nth-child(2) > dl > dd > strong > span:nth-child(2)").text

        if format(interest, ",") != next_interest.replace("원", ""):
            screenshot()
            sum_fail += 1
            print("\x1b[1;31mFail\x1b[1;m - 입력 페이지에서 노출되던 예상 연 이자금액과 결과 페이지의 예상 연 이자금액이 일치하지 않음")
            print("기대결과값: " + format(interest, ",") + "원")
            print("실제결과값: " + next_interest + "원")
            return False

    except NoSuchElementException:
        sum_nt += 1
        print("N/T - 분석 결과 페이지의 예상 연 이자금액을 찾지못함")
        return False

    try:
        # 결과 페이지 통장 기능 체크박스에 체크된 항목이 입력 페이지에서 선택한 항목과 일치하는지 확인
        for x in range(1, len(lst_func)):

            checkbox = driver.find_element(By.CSS_SELECTOR, ".listWrap_119TX > :nth-child(2) > ul > li > ul > :nth-child(" + str(x) + ") > div > input")
            if bool(lst_func[x]) != checkbox.is_selected():
                screenshot()
                sum_fail += 1
                print("\x1b[1;31mFail\x1b[1;m - 입력 페이지에서 선택한 통장 기능이 결과 페이지로 정상적으로 전달되지 않음")
                return False

    except NoSuchElementException:
        sum_nt += 1
        print("N/T - 분석 결과 페이지의 통장기능 checkbox를 찾지못함")
        return False

    num = len(invest_div)

    if num > 3:
        num = 3

    for x in range(0, num):

        for y in range(1, len(lst_func)):
            if bool(lst_func[y]):
                if str(sheet_func_idx.cell(y, 1).value) not in invest_div[x].text:
                    screenshot()
                    print("\x1b[1;31mFail\x1b[1;m - 선택한 통장기능에 해당하는 상품이 정상적으로 노출되지 않습니다.")
                    sum_fail += 1
                    return False

    return True

# 결과 리스트에서 상위 5개의 상품 상세보기 클릭시, 정상적인 페이지로 이동하는지 확인
# 결과 리스트로 버튼 눌렀을 때, 결과 리스트 페이지로 잘 이동하는지 확인
def confirm_detail():

    global sum_fail, sum_nt

    num = len(driver.find_elements(By.CLASS_NAME, "cardWrap_3dP8_"))
    wait = 0

    if num > 5:
        num = 5

    for x in range (0, num):

        while True:

            if wait > 20:
                screenshot()
                print("\x1b[1;31mFail\x1b[1;m - 결과 리스트 로드 timeout")
                sum_fail += 1
                return False

            lst_invest = driver.find_elements(By.CLASS_NAME, "cardWrap_3dP8_")

            if len(lst_invest) > 0:
                break

            sleep(1)
            wait += 1

        invest_name1 = driver.find_elements(By.CLASS_NAME, "name_-Xnbq")[x].text
        invest_detail = driver.find_element(By.CSS_SELECTOR, ".cardsContainer_2d0E9 > :nth-child(" + str(x + 1) + ") > .body_3UwsQ > .buttonGroup_1CD2Q > :nth-child(1)")

        lst_invest[x].location_once_scrolled_into_view

        sleep(1)

        invest_detail.click()

        sleep(2)

        wait_detail = 0

        while True:

            if wait_detail > 20:
                screenshot()
                print("\x1b[1;31mFail\x1b[1;m - 상품 상세페이지 로드 Timeout")
                sum_fail += 1
                return False

            invest_name2 = driver.find_element(By.CSS_SELECTOR, ".headerInfo_FgKOA > h3").text

            if invest_name2 != "":
                break

            sleep(1)
            wait_detail += 1

        if invest_name1 != invest_name2:
            screenshot()
            sum_fail += 1
            print("\x1b[1;31mFail\x1b[1;m - 잘못된 상세페이지로 이동")
            print("기대결과값: " + invest_name1 + "의 상세페이지, 실제결과값: " + invest_name2 + "의 상세페이지")
            return False

        try:
            driver.find_element(By.LINK_TEXT, "결과 리스트로").click()
        except NoSuchElementException:
            sum_nt += 1
            print("N/T - 상품 상세보기 페이지 내 결과 리스트로 버튼을 찾지못함")
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

        if driver.current_url != "https://banksalad.com/cma/profits":
            screenshot()
            sum_fail += 1
            print("\x1b[1;31mFail\x1b[1;m - 결과 리스트로 버튼 클릭시 잘못된 url로 이동")
            print("기대결과값: https://banksalad.com/cma/profits")
            print("실제결과값: " + driver.current_url)
            return False

    return True


def screenshot():
    file_dir = "screenshot/cmatest/"

    if i < 10:
        screenshot_name = "cmatest00" + str(i) + "_fail_" + datetime.today().strftime("%Y%m%d%H%M") + ".png"
    else:
        screenshot_name = "cmatest0" + str(i) + "_fail_" + datetime.today().strftime("%Y%m%d%H%M") + ".png"

    driver.save_screenshot(file_dir + screenshot_name)


# main 함수 시작

print("------------------------테스트 시작------------------------")

start = time.time()

#백그라운드 옵션
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("window-size=1920x1080")
chrome_options.add_argument("headless")

for i in range(1, total + 1):

    # 크롬드라이버를 백그라운드로 돌리고 싶을 때(또는 다른 옵션을 추가하고 싶을 때), 크롬드라이버 디렉토리 뒤에 옵션 추가
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')

    if i < 10:
        print("cmatest00" + str(i) + " Running...")
    else:
        print("cmatest0" + str(i) + " Running...")

    driver.get("https://banksalad.com/cma/questions")

    sleep(2)

    if not check():
        driver.quit()
        continue

    interest = 0

    try:
        tmp_interest = driver.find_element(By.CSS_SELECTOR, ".result_tFmiI > :nth-child(2)").text.replace("원", "").replace(",", "")

        if tmp_interest == "":
            sum_nt += 1
            driver.quit()
            print("N/T - \'예상 연 이자금액\'을 찾지못함")
            continue

        else:
            interest = int(driver.find_element(By.CSS_SELECTOR, ".result_tFmiI > :nth-child(2)").text.replace("원", "").replace(",", ""))

    except NoSuchElementException:
        sum_nt += 1
        driver.quit()
        print("N/T - \'예상 연 이자금액\'을 찾지못함")
        continue

    try:
        driver.find_element(By.LINK_TEXT, "결과보기").click()
    except NoSuchElementException:
        print("N/T - \'결과보기\' 버튼을 찾지 못함")
        sum_nt += 1
        driver.quit()
        continue

    sleep(2)

    if not load_invest():
        driver.quit()
        continue

    # 노출되는 상품들 div
    invest_div = driver.find_elements(By.CSS_SELECTOR, ".cardWrap_3dP8_")

    if len(invest_div) == 0:
        screenshot()
        print("\x1b[1;31mFail\x1b[1;m - 상품이 노출되지 않습니다.")
        continue

    if not confirm_result():
        driver.quit()
        continue

    if not confirm_detail():
        driver.quit()
        continue

    sum_pass += 1

    print("\x1b[1;34mPass\x1b[1;m")  # Pass 파란색

    driver.quit()

table = BeautifulTable()

table.column_headers = ["Total", "Pass", "Fail", "N/T"]
table.append_row([total, sum_pass, sum_fail, sum_nt])

print("------------------------테스트 결과------------------------")
print("실행 날짜: " + datetime.today().strftime("%Y-%m-%d"))
print("총 실행시간: " + str(int(time.time() - start)) +  "s")
print("한 케이스당 평균 실행시간: " + str(int((time.time() - start)/total)) + "s")
print(table)