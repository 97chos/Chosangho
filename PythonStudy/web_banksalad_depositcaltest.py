# -*- coding: utf-8 -*-
from imp import reload
import xlrd
from beautifultable import BeautifulTable
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import sys
from selenium.webdriver.common.by import By
import datetime
import time

from selenium.webdriver.common.keys import Keys

reload(sys)
sys.setdefaultencoding("utf-8")

wb = xlrd.open_workbook('/Users/hwangchaeeun/Desktop/Test_Data.xlsx')
sheet_deposit = wb.sheet_by_name("예금계산기")

sum_pass = 0
sum_fail = 0
total = 0
sum_nt = 0


driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.get('https://banksalad.com/deposits/calculator')


def input(i):
    global sum_nt, sum_fail
    # 입력 값 초기화
    try:
        input_money = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div:nth-child(1) > div > div > input[type=text]")
        input_money.send_keys(' \b', ' \b', ' \b', ' \b', ' \b', ' \b', ' \b', ' \b', ' \b')
        input_period = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div:nth-child(2) > div > div > input[type=text]")
        input_period.send_keys(Keys.BACK_SPACE, Keys.BACK_SPACE)
        input_interest = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div:nth-child(3) > div > div.inputForm_LqSYE > div > input[type=text]")
        input_interest.send_keys(Keys.BACK_SPACE, Keys.BACK_SPACE, Keys.BACK_SPACE)

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 값을 초기화하기 위한 항목을 찾지 못했습니다.")
        return False

    # 값 입력
    try:
        month = int(sheet_deposit.cell(i, 2).value)  # 예치금 입력
        input_money.send_keys(month)

        period = int(sheet_deposit.cell(i, 1).value)  # 가입기간 입력
        input_period.send_keys(period)

        interest = format(sheet_deposit.cell(i, 3).value)  # 이자율 입력
        input_interest.send_keys(interest)

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 값을 입력하기 위한 항목을 찾지 못했습니다.")
        return False
    return True


def drop_select():
    global sum_nt
    # 단리/복리 버튼 선택
    try:
        button = int(sheet_deposit.cell(i, 4).value)
        driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div:nth-child(3) > div > div.dropDownContainer_3NNNi > div > label").click()
        driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div:nth-child(3) > div > div.dropDownContainer_3NNNi > div > ul > li:nth-child(" + str(button) + ") > button").click()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 단리/복리 선택 버튼을 찾지 못했습니다.")
        return False
    return True


def result_confirm():
    # 원금 및 만기지급금액 일치 여부 확인
    global sum_fail, sum_nt
    try:
        money_input = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div:nth-child(1) > div > div > input[type=text]").get_attribute("value").replace(",", "")  # 예치금 입력 값
        money_result = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div.resultContainer_1uMhk > div:nth-child(1) > div").text.replace(",", "").replace("원", "")  # 원금 입력 값
        sum_result = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div.option_VmIHA.resultAmount_3pRs4 > div > div > input[type=text]").get_attribute("value").replace(",", "")  # 만기 지급금액 값
        interest_result = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_Fqfwi > div > div.resultContainer_1uMhk > div:nth-child(2) > div").text.replace(",", "").replace("원", "")  # 하단 이자 값

        # 예치금액 입력값과 하단 원금 일치여부 확인
        if money_result != money_input:
            print("\x1b[1;31mFail\x1b[1;m - 원금이 일치하지 않습니다.")
            print("기대결과 : " + money_result)
            print("실제결과 : " + money_input)
            sum_fail += 1
            return False

        # 만기금액 결과와 원금 + 이자 일치여부 확인
        if int(sum_result) != (int(money_result) + int(interest_result)):
            print("\x1b[1;31mFail\x1b[1;m - 만기지급금액이 일치하지 않습니다.")
            print("기대결과 : " + sum_result)
            print("실제결과 : " + str(int(money_result + interest_result)))
            sum_fail += 1
            return False

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 원금 확인을 위한 항목을 찾지 못했습니다.")
        return False
    return True


def button():
    # 적금계산기도 써보기 버튼 선택
    global sum_nt, sum_fail, sum_pass
    try:
        driver.find_element(By.CSS_SELECTOR,
                            "#wrap > div > div:nth-child(1) > div:nth-child(2) > div.bottom_3nZP1 > div > a").click()

        tab = driver.window_handles[1]
        driver.switch_to.window(window_name=tab)

        if driver.current_url != "https://banksalad.com/savings/calculator":
            sum_fail += 1
            print("\x1b[1;31mFail\x1b[1;m - 적금 계산기도 써보기 버튼 클릭시 잘못된 url로 이동합니다.")
            print("기대결과값: https://banksalad.com/savings/calculator")
            print("실제결과값: " + driver.current_url)
            return False

        first_tab = driver.window_handles[0]
        driver.switch_to.window(window_name=first_tab)
        sum_pass += 1
        print("\x1b[1;34mPass\x1b[1;m")

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 적금계산기도 써보기 버튼을 찾지 못했습니다.")
    return True


def button2():
    # 지금 추천받기 버튼 선택
    global sum_fail, sum_nt, sum_pass
    try:
        driver.find_element(By.CSS_SELECTOR,
                            "#wrap > div > div:nth-child(1) > div:nth-child(2) > div.bottom_3nZP1 > a").click()

        tab = driver.window_handles[2]
        driver.switch_to.window(window_name=tab)

        if driver.current_url != "https://banksalad.com/deposits/questions":
            sum_fail += 1
            print("\x1b[1;31mFail\x1b[1;m - 지금 추천받기 버튼 클릭시 잘못된 url로 이동합니다.")
            print("기대결과값: https://banksalad.com/deposits/questions")
            print("실제결과값: " + driver.current_url)
            return False

        first_tab1 = driver.window_handles[0]
        driver.switch_to.window(window_name=first_tab1)
        sum_pass += 1
        print("\x1b[1;34mPass\x1b[1;m")

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 지금 추천받기 버튼을 찾지 못했습니다.")
    return True


start = time.time()
print("------------------------TEST START------------------------")
for i in range(1, 22):
    if i < 10:
        print("depositcaltest00" + str(i) + " Running...")
    else:
        print("depositcaltest0" + str(i) + " Running...")

    if not input(i):
        driver.quit()
        continue

    if not drop_select():
        driver.quit()
        continue

    if not result_confirm():
        driver.quit()
        continue

    sum_pass += 1
    print("\x1b[1;34mPass\x1b[1;m")

if not button():
    driver.quit()

if not button2():
    driver.quit()

driver.quit()

table = BeautifulTable()
table.column_headers = ["Total", "Pass", "Fail", "N/T"]
table.append_row([total, sum_pass, sum_fail, sum_nt])

print("------------------------TEST RESULT------------------------")
sec = time.time() - start
times = str(datetime.timedelta(seconds=sec)).split(".")
times = times[0]
now = time.localtime()
date = "Today %04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
print(date)
print("Running Time " + times)
print(table)
