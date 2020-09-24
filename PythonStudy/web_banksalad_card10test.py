# -*- coding: utf-8 -*-
from imp import reload
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from beautifultable import BeautifulTable
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import sys
from selenium.webdriver.common.by import By
from datetime import datetime
import datetime
import time
from selenium.webdriver.support.wait import WebDriverWait
reload(sys)
sys.setdefaultencoding("utf-8")
sum_pass = 0
sum_fail = 0
total = 0
sum_nt = 0


def screenshot(j, web_driver):
    file_dir = "/Users/hwangchaeeun/Desktop/"
    web_driver.save_screenshot(file_dir + screenshot_name)


def filter_check_credit():
    global sum_nt, sum_fail
    try:
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".container__tXwE.right_2TA44 > div > div > label").location_once_scrolled_into_view
        driver.find_element(By.CSS_SELECTOR, ".container__tXwE.right_2TA44 > div > div > label").click()
        sleep(1)
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 필터 버튼을 찾지 못했습니다.")
        return False

    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, ".container__tXwE.right_2TA44 > div > div > ul > li:nth-child(1) > button"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        sum_fail += 1
        screenshot(i, driver)
        print("\x1b[1;31mFail\x1b[1;m - 필터가 정상적으로 로드되지 않았습니다.")
        return False

    try:
        driver.find_element(By.CSS_SELECTOR, ".container__tXwE.right_2TA44 > div > div > ul > li:nth-child(1) > button").click()
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 필터 버튼을 선택하지 못했습니다.")
        return False
    return True


def filter_check():
    global sum_nt, sum_fail

    try:
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".container__tXwE.right_2TA44 > div > div > label").location_once_scrolled_into_view
        driver.find_element(By.CSS_SELECTOR, ".container__tXwE.right_2TA44 > div > div > label").click()
        sleep(1)
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 필터 버튼을 찾지 못했습니다.")
        return False

    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, ".container__tXwE.right_2TA44 > div > div > ul > li:nth-child(3) > button"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        sum_fail += 1
        screenshot(i, driver)
        print("\x1b[1;31mFail\x1b[1;m - 필터가 정상적으로 로드되지 않았습니다.")
        return False

    try:
        driver.find_element(By.CSS_SELECTOR, ".container__tXwE.right_2TA44 > div > div > ul > li:nth-child(3) > button").click()
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 필터 버튼을 선택하지 못했습니다.")
        return False
    return True


def title(i):
    global sum_fail, sum_nt
    try:
        driver.find_element(By.CSS_SELECTOR, ".cards_2AMVH > li:nth-child(" + str(i) + ") >  div > section > div.buttons_2Q2OW > a").location_once_scrolled_into_view
        card_name = driver.find_element(By.CSS_SELECTOR, ".wrap_1y4z9 > div:nth-child(2) > ul > li:nth-child(" + str(i) + ") > div > h4").text
        driver.find_element(By.CSS_SELECTOR, ".cards_2AMVH > li:nth-child(" + str(i) + ") >  div > section > div.buttons_2Q2OW > a").click()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - 페이지 이동 버튼을 찾지 못했습니다.")
        return False

    timeout = 20
    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, "#wrap > div > div:nth-child(1) > div.back_u8cSA > section.cover_s55z6 > div > h4"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        sum_fail += 1
        screenshot(i, driver)
        print("\x1b[1;31mFail\x1b[1;m - 카드 상세 페이지가 정상적으로 로드되지 않았습니다.")
        driver.back()
        return False
    try:
        title = driver.title.replace(" - ", "").replace(" 혜택 | 뱅크샐러드", "")
        if str(card_name) != str(title):
            sum_fail += 1
            screenshot(i, driver)
            print("\x1b[1;31mFail\x1b[1;m - 올바른 상세 페이지로 이동하지 않습니다.")
            print("카드 명 : " + card_name)
            print("페이지 title : " + title)
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 인기카드10 항목을 찾지 못했습니다.")
        return False
    return True


def main(i):
    global sum_nt, sum_fail

    try:
        driver.find_element(By.LINK_TEXT, "뱅크샐러드 메인으로").location_once_scrolled_into_view

        if i == 10:
            driver.find_element(By.LINK_TEXT, "뱅크샐러드 메인으로").click()
            if driver.current_url != "https://banksalad.com/":
                screenshot(i, driver)
                sum_fail += 1
                print("\x1b[1;31mFail\x1b[1;m - 뱅크샐러드 메인으로 버튼 클릭시 잘못된 url로 이동합니다.")
                print("기대결과값: https://banksalad.com/")
                print("실제결과값: " + driver.current_url)
                return False
            driver.back()

        driver.back()

    except NoSuchElementException:
        sum_nt += 1
        print("NT - \'뱅크샐러드 메인으로\' 버튼을 찾지 못했습니다.")
        return False
    return True


def page_load():
    global sum_fail
    timeout = 20
    try:
        element_present = EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".wrap_1y4z9 > div:nth-child(2) > ul > li:nth-child(1) > div > span"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        sum_fail += 1
        screenshot(y, driver)
        print("\x1b[1;31mFail\x1b[1;m - 페이지가 정상적으로 로드되지 않았습니다.")
        driver.refresh()
        return False
    return True


def card_type():
    global sum_fail, sum_nt
    try:
        driver.find_element(By.CSS_SELECTOR, ".wrap_1y4z9 > div:nth-child(2) > ul > li:nth-child(" + str(j) + ") > div > h4").location_once_scrolled_into_view
        card_type = driver.find_element(By.CSS_SELECTOR, ".wrap_1y4z9 > div:nth-child(2) > ul > li:nth-child(" + str(j) + ") > div > span").text
        if i == 1:
            if card_type != '신용':
                screenshot(j, driver)
                print("신용카드" + str(j) + "위 " + "\x1b[1;31mFail\x1b[1;m - 카드 종류가 일치하지 않습니다.")
                print("기대결과 : " + '신용')
                print("실제결과 : " + card_type)
                sum_fail += 1
                return False
        if i == 3:
            if card_type != '체크':
                screenshot(j, driver)
                print("체크카드" + str(j) + "위 " + "\x1b[1;31mFail\x1b[1;m - 카드 종류가 일치하지 않습니다.")
                print("기대결과 : " + '체크')
                print("실제결과 : " + card_type)
                sum_fail += 1
                return False
    except NoSuchElementException:
        sum_nt += 1
        print("NT - 인기카드10 항목을 찾지 못했습니다.")
        return False
    return True


driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.get('https://banksalad.com/cards/ranking')

start = time.time()
print("------------------------TEST START------------------------")
for i in range(1, 4):
    for j in range(1, 11):
        total += 1
        if not page_load():
            continue
        if i == 1:
            print("card10test00" + str(j) + "(credit) Running...")
            screenshot_name = "card10test00" + str(j) + "(credit)_fail.png"
        if i == 2:
            print("card10test0" + str(j+10) + "(check/credit) Running...")
            screenshot_name = "card10test00" + str(j+10) + "(check/credit)_fail.png"
        if i == 3:
            print("card10test0" + str(j+20) + "(check) Running...")
            screenshot_name = "card10test00" + str(j+20) + "(check)_fail.png"

        if i == 2:
            if not filter_check_credit():
                continue
            if not page_load():
                continue

        if i == 3:
            if not filter_check():
                continue
            if not page_load():
                continue

        if not card_type():
            continue

        if not title(j):
            continue

        if not main(j):
            continue

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
