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
from datetime import datetime
import datetime
import time

from selenium.webdriver.support.wait import WebDriverWait

reload(sys)
sys.setdefaultencoding("utf-8")

wb = xlrd.open_workbook('/Users/hwangchaeeun/Desktop/Test_Data.xlsx')
sheet_loantc = wb.sheet_by_name("BEST 대출 TestCase")

sum_pass = 0
sum_fail = 0
total = 0
sum_nt = 0

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")


def screenshot(x, web_driver):
    file_dir = "/Users/hwangchaeeun/Desktop/"
    if x < 10:
        screenshot_name = "loantest00" + str(x) + "_fail.png"
    else:
        screenshot_name = "loantest0" + str(x) + "_fail.png"
    web_driver.save_screenshot(file_dir + screenshot_name)


def loan_sum(mloan_idx, web_driver):
    global sum_nt, sum_fail
    sheet_mloan_idx = wb.sheet_by_name("대출금액 index")
    mloan = int(sheet_mloan_idx.cell(mloan_idx, 1).value)

    # 대출 금액 버튼 선택
    try:
        web_driver.find_element(By.CSS_SELECTOR, ":nth-child(2) > :nth-child(1) > ul > :nth-child(" + str(loan_idx) + ") > button").click()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 희망 대출 금액 선택 버튼을 찾지 못했습니다.")
        return False

    # 선택한 대출 금액이 입력창에 정상 노출되는지 확인
    try:
        input_loan = int(web_driver.find_element(By.CSS_SELECTOR, ".amount_3x6iq > .desktop_1HAhS > div > input").get_attribute('value'))
        loan_result = web_driver.find_element(By.CSS_SELECTOR, ".questions_3ScUv > li:nth-child(1) > .value_3k1fw").text.replace(",", "")
        loan_result = loan_result.replace("만원", "")
        if mloan != input_loan:
            sum_fail += 1
            print("\x1b[1;31mFail\x1b[1;m - 희망 대출 금액 버튼을 클릭했을 때, 입력창에 해당 금액이 정상적으로 노출되지 않습니다.")  # Fail 빨간색 글씨
            print("기대결과값: " + str(mloan) + ", 실제결과값: " + str(input_loan))
            screenshot(i, driver)
            return False
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 희망 대출 금액 선택 입력창을 찾지 못했습니다.")
        return False

    # 선택한 대출 금액이 입력항목에 정상 노출되는지 확인
    try:
        loan_result = web_driver.find_element(By.CSS_SELECTOR, ".questions_3ScUv > li:nth-child(1) > .value_3k1fw").text.replace(",", "")
        loan_result = loan_result.replace("만원", "")
        if int(mloan) != int(loan_result):
            sum_fail += 1
            print("\x1b[1;31mFail\x1b[1;m - 희망 대출 금액 버튼을 클릭했을 때, 입력 결과에 해당 금액이 정상적으로 노출되지 않습니다.")  # Fail 빨간색 글씨
            print("기대결과값: " + str(mloan) + ", 실제결과값: " + str(loan_result))
            screenshot(i, driver)
            return False
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 희망 대출 금액 버튼을 클릭했을 때, 입력 결과 항목을 찾지 못했습니다.")
        return False

    return True


def loan_credit(i, web_driver):
    global sum_nt, sum_fail
    sheet_creditlevel = int(sheet_loantc.cell(i, 2).value)

    # 신용등급 선택
    try:
        web_driver.find_element(By.CSS_SELECTOR, "label > span").click()
        web_driver.find_element(By.CSS_SELECTOR,
                                "ul > :nth-child(" + str(sheet_creditlevel) + ") > span").click()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 신용등급 선택창을 찾지 못했습니다.")
        return False

    # 신용등급 입력 결과 확인
    try:
        creditlevel = web_driver.find_element(By.CSS_SELECTOR, "label > span").text
        credit_result = web_driver.find_element(By.CSS_SELECTOR,
                                                ".questions_3ScUv > li:nth-child(2) > .value_3k1fw").text
        if str(credit_result) != str(creditlevel):
            sum_fail += 1
            print("\x1b[1;31mFail\x1b[1;m - 신용등급 선택 시, 입력 결과에 선택 사항이 정상적으로 노출되지 않습니다.")  # Fail 빨간색 글씨
            print("기대결과값: " + str(creditlevel) + ", 실제결과값: " + str(credit_result))
            screenshot(i, driver)
            return False
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 신용등급을 선택창과 입력 결과 항목을 찾지 못했습니다.")
        return False

    return True


def loan_job(i, web_driver):
    global sum_nt, sum_fail
    sheet_job = int(sheet_loantc.cell(i, 3).value)

    # 직업 선택
    try:
        web_driver.find_element(By.CSS_SELECTOR, ":nth-child(6) > div > button").click()
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 직업 선택 버튼을 선택하지 못했습니다.")
        return False

    # 직업 선택 팝업이 5초 안에 노출되지 않으면 fail
    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, ".list_2C8C4 > li:nth-child(1) > label"))
        WebDriverWait(driver, timeout).until(element_present)

    except TimeoutException:
        sum_fail += 1
        screenshot(i, driver)
        print("\x1b[1;31mFail\x1b[1;m - 직업 선택 팝업이 정상적으로 노출되지 않았습니다.")
        driver.quit()
        return False

    try:
        driver.find_element(By.CSS_SELECTOR, ".list_2C8C4 > li:nth-child(" + str(sheet_job) + ") > label").location_once_scrolled_into_view
        driver.find_element(By.CSS_SELECTOR, ".list_2C8C4 > li:nth-child(" + str(sheet_job) + ") > label").click()
        driver.find_element(By.CSS_SELECTOR, ".accept_3yeys").click()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 직업 선택 버튼을 찾지 못했습니다.")
        return False

    # 선택한 직업이 입력항목에 정상 노출되는지 확인
    try:
        job_name = web_driver.find_element(By.CSS_SELECTOR, ":nth-child(6) > div > button").text
        job_result = web_driver.find_element(By.CSS_SELECTOR, ".questions_3ScUv > li:nth-child(3) > .value_3k1fw").text
        if str(job_name) != str(job_result):
            print("\x1b[1;31mFail\x1b[1;m - 직업 선택 시, 입력 결과에 선택 사항이 정상적으로 노출되지 않습니다.")  # Fail 빨간색 글씨
            print("기대결과값: " + str(job_name) + ", 실제결과값: " + str(job_result))
            screenshot(i, driver)
            return False
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 직업을 선택했을 때, 입력 결과 항목을 찾지 못했습니다.")
        return False

    return True


def loan_income(i, web_driver):
    global sum_nt, sum_fail
    sheet_income_idx = wb.sheet_by_name("연소득 index")
    sheet_income = int(sheet_loantc.cell(i, 4).value)
    income = int(sheet_income_idx.cell(sheet_income, 1).value)

    # 연소득 선택
    try:
        web_driver.find_element(By.CSS_SELECTOR, ".preset_guXx3 > li:nth-child(" + str(sheet_income) + ")").click()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 연소득 선택 항목을 찾지 못했습니다.")
        return False

    # 선택한 연소득이 입력창에 정상 노출되는지 확인
    try:
        input_income = int(web_driver.find_element(By.CSS_SELECTOR,".amount_1_jHL > .desktop_1HAhS > div > input").get_attribute('value'))
        if income != input_income:
            print("\x1b[1;31mFail\x1b[1;m - 연소득 선택 시, 입력창에 선택 사항이 정상적으로 노출되지 않습니다.")  # Fail 빨간색 글씨
            print("기대결과값: " + str(income) + ", 실제결과값: " + str(input_income))
            screenshot(i, driver)
            return False
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 연소득을 선택했을 때, 입력창을 찾지 못했습니다.")
        return False
    # 선택한 연소득이 입력항목에 정상 노출되는지 확인
    try:
        income_result = web_driver.find_element(By.CSS_SELECTOR, ".questions_3ScUv > li:nth-child(4) > .value_3k1fw").text.replace(",", "")
        income_result = income_result.replace("만원", "")
        if income != int(income_result):
            print("\x1b[1;31mFail\x1b[1;m - 연소득 선택 시, 입력 결과에 선택 사항이 정상적으로 노출되지 않습니다.")  # Fail 빨간색 글씨
            print("기대결과값: " + str(income) + ", 실제결과값: " + str(income_result))
            screenshot(i, driver)
            return False
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 연소득을 선택했을 때, 입력 결과를 찾지 못했습니다.")
        return False

    return True


# 선택한 희망 대출금액이 상단 금액과 일치하는지 확인
def loan_sum2(i, web_driver):
    global sum_nt, sum_fail
    sheet_mloan_idx = wb.sheet_by_name("대출금액 index")
    sheet_mloan = int(sheet_loantc.cell(i, 1).value)
    try:
        mloan = int(sheet_mloan_idx.cell(sheet_mloan, 1).value)
        text_mloan = int(web_driver.find_element(By.CSS_SELECTOR, "#amount").get_attribute('value'))
        if mloan != text_mloan:
            print("\x1b[1;31mFail\x1b[1;m - 희망 대출금액이 결과 페이지 상단 금액과 일치하지 않습니다.")  # Fail 빨간색 글씨
            print("기대결과값: " + str(mloan) + ", 실제결과값: " + str(text_mloan))
            screenshot(i, driver)
            return False

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 결과 페이지 상단 금액을 찾지 못했습니다.")
        return False
    return True


# 예상한도가 결과페이지 상단에 노출되는 금액과 동일한지 확인
def expect_limit():
    global sum_nt
    try:
        loan_expect_result = driver.find_element(By.CSS_SELECTOR, ".calculatedInterest_2MmE7").text.replace(",", "").replace("예상한도 ", "").replace("만원", "")
        sleep(1)
        if loan_expect != loan_expect_result:
            print("\x1b[1;31mFail\x1b[1;m - 희망 대출금액이 결과 페이지 상단 금액과 일치하지 않습니다.")  # Fail 빨간색 글씨
            print("기대결과값: " + str(loan_expect) + ", 실제결과값: " + str(loan_expect_result))
            screenshot(i, driver)
            return False
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 결과페이지 첫 번째 상품의 예상한도를 찾지 못했습니다.")
        return False
    return True


# 결과 리스트 로드 timeout 시 fail처리
def load_loan():
    global sum_nt, sum_fail
    wait = 0
    for x in range(1, 4):
        while True:
            # 20번 기다렸는데도 load되지 않았을때, timeout처리
            if wait > 20:
                screenshot()
                print("\x1b[1;31mFail\x1b[1;m - 결과 리스트 로드 timeout")
                sum_fail += 1
                return False
            elements = driver.find_elements(By.CSS_SELECTOR, ".resultItem_2jgVP")
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


# 상품 상세페이지 확인
def confirm_detail():
    global sum_fail, sum_nt
    num = len(driver.find_elements(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol:nth-child(2) > li"))
    wait = 0
    if num > 2:
        num = 2
    for x in range(0, num):
        while True:
            if wait > 20:
                screenshot(i, driver)
                print("\x1b[1;31mFail\x1b[1;m - 결과 리스트 로드 timeout")
                sum_fail += 1
                return False
            lst_loan = driver.find_elements(By.CSS_SELECTOR, ".resultItem_2jgVP")

            if len(lst_loan) > 0:
                break

            sleep(1)
            wait += 1

        loan_name1 = driver.find_elements(By.CSS_SELECTOR, ".headerText_SOgCc > h1")[x].text.replace("고정금리", "").replace("변동금리", "")
        loan_detail = driver.find_element(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol > li:nth-child(" + str(x + 1) + ") > div > div.body_cYC3y > div > div.linkButtons_3eD-d > a.linkDetail_2YWx8.linkButton_3mX1p")
        lst_loan[x].location_once_scrolled_into_view
        sleep(1)
        loan_detail.click()

        # 상품 상세페이지 10초동안 로드되지 않은 경우 fail처리
        timeout = 10
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, ".head_25kNF > h1"))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            sum_fail += 1
            screenshot(i, driver)
            print("\x1b[1;31mFail\x1b[1;m - 상품 상세 페이지가 정상적으로 로드되지 않았습니다.")
            driver.quit()
            return False

        try:
            invest_name2 = driver.find_element(By.CSS_SELECTOR, ".head_25kNF > h1").text

            if loan_name1 != invest_name2:
                screenshot(i, driver)
                sum_fail += 1
                print("\x1b[1;31mFail\x1b[1;m - 잘못된 상세페이지로 이동")
                print("기대결과값: " + loan_name1 + "의 상세페이지, 실제결과값: " + invest_name2 + "의 상세페이지")
                return False

            driver.find_element(By.LINK_TEXT, "결과 리스트로").click()
            sleep(2)
            if driver.current_url != "https://banksalad.com/credit-loans/profits":
                screenshot(i, driver)
                sum_fail += 1
                print("\x1b[1;31mFail\x1b[1;m - 결과 리스트로 버튼 클릭시 잘못된 url로 이동")
                print("기대결과값: https://banksalad.com/credit-loans/profits")
                print("실제결과값: " + driver.current_url)
                return False

        except NoSuchElementException:
            sum_nt += 1
            print("N/T - 상품 상세보기 페이지 내 요소(상품명 또는 결과 리스트로 버튼)를 찾지못함")
            return False
    return True


# 금리 낮은 순 선택
def low_gumri(n):
    global sum_nt, sum_fail

    try:
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".desktop_1HAhS > ul > li:nth-child(3) > div").click()
        driver.find_element(By.CSS_SELECTOR,
                            ".desktop_1HAhS > ul > li:nth-child(3) > div > ul > li:nth-child(1) > button").click()

        for i in range(1, n):
            sleep(2)
            gumri1 = driver.find_element(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol > li:nth-child(" + str(i) + ") > div > div.body_cYC3y > div > div.info_19W26 > dl  dd.interestInfo_r017q > ul > li:nth-child(1) > div > strong").text.replace("평균 ", "").replace("%", "")
            gumri2 = driver.find_element(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol > li:nth-child(" + str(i + 1) + ") > div > div.body_cYC3y > div > div.info_19W26 > dl  dd.interestInfo_r017q > ul > li:nth-child(1) > div > strong").text.replace("평균 ", "").replace("%", "")
            if float(gumri1) > float(gumri2):
                print("\x1b[1;31mFail\x1b[1;m - 금리 낮은 순 필터가 정상적으로 동작하지 않습니다.")
                sum_fail += 1
                return False

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 금리 낮은 순 필터 관련 항목을 찾지 못했습니다.")
        return False
    return True


# 한도 높은 순 선택
def high_hando(n):
    global sum_fail, sum_nt

    try:
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".desktop_1HAhS > ul > li:nth-child(3) > div").click()
        driver.find_element(By.CSS_SELECTOR,
                            ".desktop_1HAhS > ul > li:nth-child(3) > div > ul > li:nth-child(2) > button").click()

        for i in range(1, n):
            sleep(2)
            hando1 = driver.find_element(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol > li:nth-child(" + str(i) + ") > div > div.body_cYC3y > div > div.info_19W26 > dl > dd.interestInfo_r017q > ul > li.calculatedInterestWrap_1QJa1 > span.calculatedInterest_2MmE7").text.replace("예상한도 ", "").replace(",", "").replace("만원", "")
            hando2 = driver.find_element(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol > li:nth-child(" + str(i + 1) + ") > div > div.body_cYC3y > div > div.info_19W26 > dl > dd.interestInfo_r017q > ul > li.calculatedInterestWrap_1QJa1 > span.calculatedInterest_2MmE7").text.replace("예상한도 ", "").replace(",", "").replace("만원", "")
            if int(hando1) < int(hando2):
                print("\x1b[1;31mFail\x1b[1;m - 한도 높은 순 필터가 정상적으로 동작하지 않습니다.")
                sum_fail += 1
                return False

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 한도 높은 순 필터 관련 항목을 찾지 못했습니다.")
        return False
    return True


# 최장 기간 순 선택
def long_date(n):
    global sum_nt, sum_fail

    try:
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".desktop_1HAhS > ul > li:nth-child(3) > div").click()
        driver.find_element(By.CSS_SELECTOR,
                            ".desktop_1HAhS > ul > li:nth-child(3) > div > ul > li:nth-child(3) > button").click()

        for i in range(1, n):
            sleep(2)
            date = driver.find_element(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol > li:nth-child(" + str(i) + ") > div > div.body_cYC3y > div > div.info_19W26 > dl > dd:nth-child(4) > ul > li > span").text
            date2 = driver.find_element(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol > li:nth-child(" + str(i + 1) + ") > div > div.body_cYC3y > div > div.info_19W26 > dl > dd:nth-child(4) > ul > li > span").text
            split1 = date.split('~', 2)
            split2 = split1[1].split('개월', 2)
            split3 = date2.split('~', 2)
            split4 = split3[1].split('개월', 2)
            if int(split2[0]) < int(split4[0]):
                print("\x1b[1;31mFail\x1b[1;m - 한도 높은 순 필터가 정상적으로 동작하지 않습니다.")
                sum_fail += 1
                return False

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 최장기간 순 필터 관련 항목을 찾지 못했습니다.")
        return False
    return True


start = time.time()
print("------------------------TEST START------------------------")
for i in range(1, 6):
    total += 1

    if i < 10:
        print("loantest00" + str(i) + " Running...")
    else:
        print("loantest0" + str(i) + " Running...")

    driver = webdriver.Chrome('/usr/local/bin/chromedriver')

    driver.get('https://banksalad.com/credit-loans/questions')

    loan_idx = int(sheet_loantc.cell(i, 1).value)

    if not loan_sum(loan_idx, driver):
        driver.quit()
        continue

    if not loan_credit(i, driver):
        driver.quit()
        continue

    if not loan_job(i, driver):
        driver.quit()
        continue

    if not loan_income(i, driver):
        driver.quit()
        continue

    sleep(1)

    # 희망 대출 금액, 예상 대출 한도
    creditlevel = driver.find_element(By.CSS_SELECTOR, ".questions_3ScUv > li:nth-child(2) > .value_3k1fw").text
    loan_result = driver.find_element(By.CSS_SELECTOR, ".questions_3ScUv > li:nth-child(1) > .value_3k1fw").text.replace(",", "")
    loan_result = loan_result.replace("만원", "")
    loan_expect = driver.find_element(By.CSS_SELECTOR, "div.preview_Qee0B > div.foot_2aDGD > section > span.resultValue_rynW5 > span").text.replace(",", "").replace("예상 대출한도 ", "").replace("만원", "")

    # 희망 대출금액이 예상 한도보다 낮은 경우 노출되는 alert 처리
    if int(loan_result) > int(loan_expect):
        try:
            alert = driver.find_element(By.LINK_TEXT, "결과보기").click()
            sleep(1)

        except NoSuchElementException:
            print("N/T - \'결과보기\' 버튼을 찾지 못했습니다.")
            sum_nt += 1
            driver.quit()
            continue

        try:
            alert_switch = driver.switch_to.alert
            alert_text = alert_switch.text.replace(",", "")  # alert에 노출되는 문구
            alert_switch.accept()
            sleep(1)
            text_mloan = int(driver.find_element(By.CSS_SELECTOR, "#amount").get_attribute('value'))  # 결과 페이지 상단 노출 금액

            # 결과 상단 희망금액이 alert 워딩에 포함되는지 확인
            if str(text_mloan) not in alert_text:
                sum_fail += 1
                print("\x1b[1;31mFail\x1b[1;m - 희망 대출금액이 결과 페이지 상단 금액과 일치하지 않습니다.")  # Fail 빨간색 글씨
                print("\x1b[1;31malert 워딩에\x1b[1;m " + str(alert_text) + "\x1b[1;31m결과 페이지 상단 금액\x1b[1;m " + str(text_mloan) + " 이 포함되지 않습니다.")
                screenshot(i, driver)
                continue

        except NoSuchElementException:
            print("N/T - \'결과페이지 상단 금액\' 항목을 찾지 못했습니다.")
            sum_nt += 1
            driver.quit()
            continue

    else:
        # 희망 대출금액이 예상한도보다 높은 경우 동작
        driver.find_element(By.LINK_TEXT, "결과보기").click()
        sleep(1)
        if not loan_sum2(i, driver):
            driver.quit()
            continue

    if not expect_limit():
        driver.quit()
        continue

    # 선택한 신용등급과 결과페이지 상단 신용등급 일치 여부 확인
    try:
        result_creditlevel = driver.find_element(By.CSS_SELECTOR, ".desktop_1HAhS > ul > li:nth-child(1) > div > ""label").text
        print(result_creditlevel)
        if creditlevel != result_creditlevel:
            sum_fail += 1
            print("\x1b[1;31mFail\x1b[1;m - 신용등급이 결과 페이지 상단과 일치하지 않습니다.")  # Fail 빨간색 글씨
            print("기대결과값: " + str(creditlevel) + ", 실제결과값: " + str(result_creditlevel))
            screenshot(i, driver)
            continue
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 결과페이지 상단 신용등급을 찾지 못했습니다.")
        driver.quit()
        continue

    if not load_loan():
        driver.quit()
        continue

    if not confirm_detail():
        driver.quit()
        continue

    loan_div = driver.find_elements(By.CSS_SELECTOR, ".resultWrap_1ZJb- > ol:nth-child(2) > li")
    if not low_gumri(len(loan_div)):
        driver.quit()

    if not high_hando(len(loan_div)):
        driver.quit()

    if not long_date(len(loan_div)):
        driver.quit()

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
