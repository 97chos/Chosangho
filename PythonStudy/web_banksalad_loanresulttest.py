# -*- coding: utf-8 -*-
from imp import reload
from time import sleep
import xlrd
from beautifultable import BeautifulTable
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
import sys
from selenium.webdriver.common.by import By
import datetime
import time

from selenium.webdriver.support.wait import WebDriverWait

reload(sys)
sys.setdefaultencoding("utf-8")

wb = xlrd.open_workbook('/Users/hwangchaeeun/Desktop/Test_Data.xlsx')
sheet_loanresulttc = wb.sheet_by_name("대출 Result TestCase")

sum_pass = 0
sum_fail = 0
total = 0
sum_nt = 0

lst_financial = ['', '', '', '', '', '']  # 금융사
lst_prepayment = ['', '', '', '']  # 중도상환수수료
lst_interest_rate_method = ['', '', '']  # 금리방법
lst_repayment_method = ['', '', '', '']  # 상환방법
lst_primerate = ['', '', '', '', '', '', '', '', '']  # 우대금리

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")


def loan_select():
    global sum_nt
    try:
        # 희망 대출금액
        driver.find_element(By.CSS_SELECTOR,
                            ":nth-child(2) > :nth-child(1) > ul > :nth-child(7) > button").click()
        # 신용등급 선택
        driver.find_element(By.CSS_SELECTOR, "label > span").click()
        driver.find_element(By.CSS_SELECTOR,
                            "ul > :nth-child(1) > span").click()
        # 직업 선택
        driver.find_element(By.CSS_SELECTOR, ":nth-child(6) > div > button").click()
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".list_2C8C4 > li:nth-child(5) > label").click()
        driver.find_element(By.CSS_SELECTOR, ".accept_3yeys").click()
        # 연소득 선택
        driver.find_element(By.CSS_SELECTOR, ".preset_guXx3 > li:nth-child(7)").click()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 대출 입력화면의 버튼을 찾지 못했습니다.")
        return False
    return True


def check_reset():
    global sum_nt
    try:
        # 결과페이지 체크 초기화
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, ":nth-child(4) > ul > :nth-child(1) > div").click()
        driver.find_element(By.CSS_SELECTOR, ":nth-child(4) > ul > :nth-child(2) > div").click()
        driver.find_element(By.CSS_SELECTOR, ":nth-child(4) > ul > :nth-child(3) > div").click()
        driver.find_element(By.CSS_SELECTOR, ":nth-child(4) > ul > :nth-child(4) > div").click()
        driver.find_element(By.CSS_SELECTOR, ":nth-child(4) > ul > :nth-child(5) > div").click()
        driver.find_element(By.CSS_SELECTOR, ":nth-child(8) > ul > :nth-child(1) > div").click()
        driver.find_element(By.CSS_SELECTOR, ":nth-child(8) > ul > :nth-child(2) > div").click()
        driver.find_element(By.CSS_SELECTOR, ":nth-child(10) > ul > :nth-child(1) > div").click()
        driver.find_element(By.CSS_SELECTOR, ":nth-child(10) > ul > :nth-child(2) > div").click()
        driver.find_element(By.CSS_SELECTOR, ":nth-child(10) > ul > :nth-child(3) > div").click()

    except NoSuchElementException:
        sum_nt += 1
        screenshot(i, driver)
        print("NT - 대출 결과화면 초기화 시 버튼을 찾지 못했습니다.")
        return False

    return True


def check_financialco(x, web_driver):
    global sum_nt

    try:
        # 금융사 선택(결과페이지로 랜딩 후 금융사 항목이 모두 체크되어있어 엑셀에는 반대로 표기했습니다.)
        for y in range(1, len(lst_financial)):
            lst_financial[y] = str(sheet_loanresulttc.cell(x, y).value)
            if bool(lst_financial[y]):
                web_driver.find_element(By.CSS_SELECTOR, ":nth-child(4) > ul > :nth-child(" + str(y) + ") > div").click()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 금융사 선택 버튼을 찾지 못했습니다.")
        return False

    return True


def check_prepayment(x, web_driver):
    global sum_nt

    try:
        # 중도상환수수료 선택
        for y in range(1, len(lst_prepayment)):
            lst_prepayment[y] = str(sheet_loanresulttc.cell(x, y + 5).value)
            if bool(lst_prepayment[y]):
                web_driver.find_element(By.CSS_SELECTOR, ":nth-child(6) > ul > :nth-child(" + str(y) + ") > div").click()
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 중도상환수수료 선택 버튼을 찾지 못했습니다.")
        return False

    return True


def check_rate_method(x, web_driver):
    global sum_nt

    try:
        # 금리방식 선택
        for y in range(1, len(lst_interest_rate_method)):
            lst_interest_rate_method[y] = str(sheet_loanresulttc.cell(x, y + 8).value)
            if bool(lst_interest_rate_method[y]):
                web_driver.find_element(By.CSS_SELECTOR, ":nth-child(8) > ul > :nth-child(" + str(y) + ") > div").click()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 금리방식 선택 버튼을 찾지 못했습니다.")
        return False

    return True


def check_repayment_method(x, web_driver):
    global sum_nt

    try:
        # 상환방법 선택
        for y in range(1, len(lst_repayment_method)):
            lst_repayment_method[y] = str(sheet_loanresulttc.cell(x, y + 10).value)
            if bool(lst_repayment_method[y]):
                web_driver.find_element(By.CSS_SELECTOR,
                                        ":nth-child(10) > ul > :nth-child(" + str(y) + ") > div").click()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 상환방법 선택 버튼을 찾지 못했습니다.")
        return False

    return True


def check_primerate(x, web_driver):
    global sum_nt

    try:
        # 우대금리 선택
        for y in range(1, len(lst_primerate)):
            lst_primerate[y] = str(sheet_loanresulttc.cell(x, y + 10).value)
            if bool(lst_primerate[y]):
                web_driver.find_element(By.CSS_SELECTOR, ":nth-child(2) > dl > dd > ul > :nth-child(" + str(y) + ") > div > label").click()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 우대금리 선택 버튼을 찾지 못했습니다.")
        return False

    return True


def screenshot(x, web_driver):
    file_dir = "/Users/hwangchaeeun/Desktop/"
    if x < 10:
        screenshot_name = "loanresulttest00" + str(x) + "_fail.png"
    else:
        screenshot_name = "loanresulttest0" + str(x) + "_fail.png"

    web_driver.save_screenshot(file_dir + screenshot_name)


# 결과 화면에 금리방식 노출 확인
def confirm_rate_method(i):
    global sum_nt, sum_fail
    try:
        sheet_ratemethod = wb.sheet_by_name("금리방식")

        num = len(i)

        if num > 3:
            for x in range(1, 3):
                for y in range(1, len(lst_interest_rate_method)):
                    if bool(lst_interest_rate_method[y]):
                        if str(sheet_ratemethod.cell(y, 1).value) not in i[x].text:
                            sum_fail += 1
                            print(
                                "\x1b[1;31mFail\x1b[1;m - 선택한 금리방식이 결과에 노출되지 않습니다.")  # Fail 빨간색 글씨
                            screenshot(i, driver)
                            return False
        else:
            for x in range(1, num):
                for y in range(1, len(lst_interest_rate_method)):
                    if bool(lst_interest_rate_method[y]):
                        if str(sheet_ratemethod.cell(y, 1).value) not in i[x].text:
                            sum_fail += 1
                            print(
                                "\x1b[1;31mFail\x1b[1;m - 선택한 금리방식이 결과에 노출되지 않습니다.")  # Fail 빨간색 글씨
                            screenshot(i, driver)
                            return False

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 결과페이지에 노출되는 금리방식 항목을 찾지 못했습니다.")
        return False

    return True


# 결과 화면에 상환방법 노출 확인
def confirm_repayment_method(i):
    global sum_nt, sum_fail
    sheet_repayment_method = wb.sheet_by_name("상환방법")

    num = len(i)

    try:
        if num > 3:
            for x in range(1, 3):
                for y in range(1, len(lst_repayment_method)):
                    if bool(lst_repayment_method[y]):
                        if str(sheet_repayment_method.cell(y, 1).value) not in i[x].text:
                            sum_fail += 1
                            print(
                                "\x1b[1;31mFail\x1b[1;m - 선택한 상환방법이 결과에 노출되지 않습니다.")  # Fail 빨간색 글씨
                            screenshot(i, driver)
                            return False

        else:
            for x in range(1, num):
                for y in range(1, len(lst_repayment_method)):
                    if bool(lst_repayment_method[y]):
                        if str(sheet_repayment_method.cell(y, 1).value) not in i[x].text:
                            sum_fail += 1
                            print(
                                "\x1b[1;31mFail\x1b[1;m - 선택하지 않은 상환방법이 결과에 노출됩니다.")  # Fail 빨간색 글씨
                            screenshot(i, driver)
                            return False

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 결과페이지에 노출되는 상환방법 항목을 찾지 못했습니다.")
        return False

    return True


# 결과 화면에 중도상환수수료 노출 확인
def confirm_prepayment(elements):
    global sum_fail, sum_nt
    sheet_prepayment = wb.sheet_by_name("추가선택항목")

    num = len(elements)

    if num > 3:
        for x in range(1, 3):
            for y in range(1, len(lst_prepayment)):
                if bool(lst_prepayment[y]):
                    if str(sheet_prepayment.cell(y, 1).value) not in elements[x].text:
                        sum_fail += 1
                        print(
                            "\x1b[1;31mFail\x1b[1;m - 선택한 중도상환수수료가 결과에 노출되지 않습니다.")  # Fail 빨간색 글씨
                        screenshot(i, driver)
                        return False

    else:
        for x in range(1, num):
            for y in range(1, len(lst_prepayment)):
                if bool(lst_prepayment[y]):
                    if str(sheet_prepayment.cell(y, 1).value) not in elements[x].text:
                        sum_fail += 1
                        print(
                            "\x1b[1;31mFail\x1b[1;m - 중도상환수수료를 선택하지 않았으나 결과에 노출됩니다.")  # Fail 빨간색 글씨
                        screenshot(i, driver)
                        return False

    return True


start = time.time()

print("------------------------TEST START------------------------")

for i in range(1, 33):
    total += 1

    if i < 10:
        print("loanresulttest00" + str(i) + " Running...")
    else:
        print("loanresulttest0" + str(i) + " Running...")

    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.get('https://banksalad.com/credit-loans/questions')

    if not loan_select():
        driver.quit()
        continue

    sleep(1)

    loan_result = driver.find_element(By.CSS_SELECTOR,
                                      ".questions_3ScUv > li:nth-child(1) > .value_3k1fw").text.replace(",", "")
    loan_result = loan_result.replace("만원", "")
    loan_expect = driver.find_element(By.CSS_SELECTOR,
                                      "div.preview_Qee0B > div.foot_2aDGD > section > span.resultValue_rynW5 > span").text.replace(",", "").replace("예상 대출한도 ", "").replace("만원", "")

    try:
        alert = driver.find_element(By.LINK_TEXT, "결과보기").click()
        sleep(1)

    except NoSuchElementException:
        print("N/T - \'결과보기\' 버튼을 찾지 못했습니다.")
        sum_nt += 1
        driver.quit()
        continue

    # 희망 대출금액이 예상 한도보다 낮은 경우 노출되는 alert 처리
    if int(loan_result) > int(loan_expect):

        try:
            alert_switch = driver.switch_to.alert
            alert_text = alert_switch.text.replace(",", "")  # alert에 노출되는 문구
            # print("alert text : " + alert_text)
            alert_switch.accept()
            sleep(1)

        except NoSuchElementException:
            print("N/T - \'alert\' 항목을 찾지 못했습니다.")
            sum_nt += 1
            driver.quit()
            continue

        if not check_reset():
            driver.quit()
            continue

    else:
        # 희망 대출금액이 예상한도보다 높은 경우 동작
        if not check_reset():
            driver.quit()
            continue

    check_financialco(i, driver)
    check_prepayment(i, driver)
    check_rate_method(i, driver)
    check_repayment_method(i, driver)
    check_primerate(i, driver)

    sleep(2)
    loan_div = driver.find_elements(By.CLASS_NAME, "resultItem_2jgVP")
    if len(loan_div) == 0:
        screenshot(i, driver)
        sum_nt += 1
        print("NT - 상품이 노출되지 않습니다.")
        driver.quit()
        continue

    loan_div[0].location_once_scrolled_into_view

    if not confirm_rate_method(loan_div):
        driver.quit()
        continue

    if not confirm_repayment_method(loan_div):
        driver.quit()
        continue

    if not confirm_prepayment(loan_div):
        driver.quit()
        continue

    sleep(1)

    sum_pass += 1

    print("\x1b[1;34mPass\x1b[1;m")

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
