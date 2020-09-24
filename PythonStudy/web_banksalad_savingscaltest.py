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
sheet_saving = wb.sheet_by_name("적금계산기")

sum_pass = 0
sum_fail = 0
total = 0
sum_nt = 0


driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.get('https://banksalad.com/savings/calculator')


def button1():
    global sum_nt, sum_fail, sum_pass
    try:
        driver.find_element(By.CSS_SELECTOR, "#wrap > div > div:nth-child(1) > div:nth-child(2) > div.bottom_1qFyD > div > a").click()

        tab = driver.window_handles[1]
        driver.switch_to.window(window_name=tab)

        if driver.current_url != "https://banksalad.com/deposits/calculator":
            sum_fail += 1
            print("\x1b[1;31mFail\x1b[1;m - 예금 계산기도 써보기 버튼 클릭시 잘못된 url로 이동합니다.")
            print("기대결과값: https://banksalad.com/deposits/calculator")
            print("실제결과값: " + driver.current_url)
            return False

        first_tab = driver.window_handles[0]
        driver.switch_to.window(window_name=first_tab)
        sum_pass += 1
        print("\x1b[1;34mPass\x1b[1;m")
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 예금계산기도 써보기 버튼을 찾지 못했습니다.")
    return True


def button2():
    global sum_fail, sum_nt, sum_pass
    try:
        driver.find_element(By.CSS_SELECTOR, "#wrap > div > div:nth-child(1) > div:nth-child(2) > div.bottom_1qFyD > a").click()

        tab = driver.window_handles[2]
        driver.switch_to.window(window_name=tab)

        if driver.current_url != "https://banksalad.com/savings/questions":
            sum_fail += 1
            print("\x1b[1;31mFail\x1b[1;m - 지금 추천받기 버튼 클릭시 잘못된 url로 이동합니다.")
            print("기대결과값: https://banksalad.com/savings/questions")
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


def input(i):
    global sum_nt, sum_fail
    # 입력 값 초기화
    try:
        input_month = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_2RDVa > div > div:nth-child(1) > div > div > input[type=text]")
        input_month.send_keys(' \b', ' \b', ' \b', ' \b', ' \b', ' \b', ' \b')
        input_period = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_2RDVa > div > div:nth-child(2) > div > div > input[type=text]")
        input_period.send_keys(Keys.BACK_SPACE, Keys.BACK_SPACE)
        input_interest = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_2RDVa > div > div:nth-child(3) > div > div.inputForm_30zap > div > input[type=text]")
        input_interest.send_keys(Keys.BACK_SPACE, Keys.BACK_SPACE, Keys.BACK_SPACE)

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 값을 초기화하기 위한 항목을 찾지 못했습니다.")
        return False

    # 값 입력
    try:
        month = int(sheet_saving.cell(i, 0).value)  # 월 납입금액 입력
        input_month.send_keys(month)

        period = int(sheet_saving.cell(i, 1).value)  # 가입기간 입력
        input_period.send_keys(period)

        interest = format(sheet_saving.cell(i, 2).value)  # 이자율 입력
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
        button = int(sheet_saving.cell(i, 3).value)
        driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_2RDVa > div > div:nth-child(3) > div > div.dropDownContainer_YrgkD > div > label").click()
        driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_2RDVa > div > div:nth-child(3) > div > div.dropDownContainer_YrgkD > div > ul > li:nth-child(" + str(button) + ") > button").click()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 단리/복리 선택 버튼을 찾지 못했습니다.")
        return False
    return True


def result_confirm():
    global sum_nt, sum_fail
    # 가입기간 * 납입금액과 결과의 원금이 일치하는지 확인
    try:
        period_input = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_2RDVa > div > div:nth-child(2) > div > div > input[type=text]").get_attribute("value")  # 가입기간
        month_input = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_2RDVa > div > div:nth-child(1) > div > div > input[type=text]").get_attribute("value").replace(",", "")  # 월 납입금액
        result_money = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_2RDVa > div > div.resultContainer_1foXe > div:nth-child(1) > div").text.replace(",", "").replace("원", "")  # 원금
        print(result_money, (int(month_input) * int(period_input)))
        if int(result_money) != int(month_input) * int(period_input):
            print("\x1b[1;31mFail\x1b[1;m - 원금이 일치하지 않습니다.")
            print("기대결과 : " + str(int(month_input) * int(period_input)))
            print("실제결과 : " + result_money)
            sum_fail += 1
            return False

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 원금 확인을 위한 항목을 찾지 못했습니다.")
        return False

    # 이자 + 납입액과 만기지급금액 일치여부 확인
    try:
        result_sum = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_2RDVa > div > div.option_blNaX.resultAmount_UmbNJ > div > div > input[type=text]").get_attribute("value").replace(",", "")  # 만기지급금액
        result_interest = driver.find_element(By.CSS_SELECTOR, ".calculatorWrap_2RDVa > div > div.resultContainer_1foXe > div:nth-child(2) > div").text.replace(",", "").replace("원", "")  # 이자
        print(result_sum, (int(result_interest) + int(result_money)))
        if int(result_sum) != (int(result_interest) + int(result_money)):
            print("\x1b[1;31mFail\x1b[1;m - 만기지급금액이 일치하지 않습니다.")
            print("기대결과 : " + str((int(result_interest) + int(result_money))))
            print("실제결과 : " + result_sum)
            sum_fail += 1
            return False

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 만기 지급금액 항목을 찾지 못했습니다.")
        return False
    return True


start = time.time()
print("------------------------TEST START------------------------")
for i in range(1, 31):
    if i < 10:
        print("savingcaltest00" + str(i) + " Running...")
    else:
        print("savingcaltest0" + str(i) + " Running...")

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

if not button1():
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
