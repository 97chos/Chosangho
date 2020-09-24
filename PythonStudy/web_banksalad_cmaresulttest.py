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
#sheet index 값은 엑셀 파일 시트 잘 확인해서 필요시 변경해주세요!!
sheet_tc = wb.sheet_by_name("CMA Result TestCase") #CMA Result TestCase

total = 10
sum_pass = 0
sum_fail = 0
sum_nt = 0

lst_signup = ['', '', '', '']
lst_func = ['', '', '', '', '', '', '']
lst_ben = ['', '', '', '', '', '', '']

def check():

    global sum_nt

    # TC sheet에 일치하는 가입방법을 체크
    for x in range(1, len(lst_signup)):
        lst_signup[x] = str(sheet_tc.cell(i, x).value)
        if bool(lst_signup[x]):
            try:
                driver.find_element(By.CSS_SELECTOR, ":nth-child(2) > ul > :nth-child(" + str(x) + ") > div").click()
                sleep(1)

            except NoSuchElementException:
                print("N/T - 가입방법 요소를 찾지 못했습니다.")
                sum_nt += 1
                return False

    # TC sheet에 일치하는 통장기능을 체크
    for x in range(1, len(lst_func)):
        lst_func[x] = str(sheet_tc.cell(i, x + 3).value)
        if bool(lst_func[x]):
            try:
                driver.find_element(By.CSS_SELECTOR, ".listWrap_119TX > :nth-child(2) > ul > li > ul > :nth-child(" + str(x) + ") > div").click()
                sleep(1)

            except NoSuchElementException:
                print("N/T - 통장기능 요소를 찾지 못했습니다.")
                sum_nt += 1
                return False

    # TC sheet에 일치하는 수수료 혜택을 체크
    for x in range(1, len(lst_ben)):
        lst_ben[x] = str(sheet_tc.cell(i, x + 9).value)
        if bool(lst_ben[x]):
            try:
                driver.find_element(By.CSS_SELECTOR, ".listWrap_119TX > :nth-child(3) > ul > li > ul > :nth-child(" + str(x) + ") > div").click()
                sleep(1)

            except NoSuchElementException:
                print("N/T - 수수료 혜택 요소를 찾지 못했습니다.")
                sum_nt += 1
                return False

            sleep(1)

    return True

# 한 페이지에서 로드할 수 있는 상품 모두 로드
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

# 체크한 가입 방법이 상위 3개의 상품 element에 정상적으로 노출되지 않으면 False를 반환
def confirm_signup(elements):

    global sum_fail

    if bool(lst_signup[1]) and not bool(lst_signup[2]) and not bool(lst_signup[3]):

        num = len(elements)

        if num > 3:
            num = 3

        for x in range(0, num):
            if "비대면\n가입" not in elements[x].text:
                print("\x1b[1;31mFail\x1b[1;m - 비대면 가입에대한 메시지가 노출되지 않습니다.")
                sum_fail += 1
                return False

    return True

# 체크한 통장기능이 상위 3개의 상품 element에 정상적으로 노출되지 않으면 False를 반환
def confirm_func(elements):

    global sum_fail

    sheet_func = wb.sheet_by_name("통장기능 index")

    num = len(elements)

    if num > 3:
        num = 3

    for x in range(0, num):

        for y in range(1, len(lst_func)):
            if bool(lst_func[y]):
                if str(sheet_func.cell(y, 1).value) not in elements[x].text:
                    print("\x1b[1;31mFail\x1b[1;m - 선택한 통장기능에 해당하는 상품이 정상적으로 노출되지 않습니다.")
                    sum_fail += 1
                    return False

    return True

# 체크한 수수료 혜택이 상위 3개의 상품 element에 정상적으로 노출되지 않으면 False를 반환
def confirm_ben(elements):

    global sum_fail

    sheet_ben = wb.sheet_by_name("수수료 혜택 index")

    num = len(elements)

    if num > 3:
        num = 3

    for x in range(0, num):
        for y in range(1, len(lst_ben)):
            if bool(lst_ben[y]):
                if str(sheet_ben.cell(y, 1).value) not in elements[x].text:
                    print("\x1b[1;31mFail\x1b[1;m - 선택한 수수료 혜택에 해당하는 상품이 정상적으로 노출되지 않습니다.")
                    sum_fail += 1
                    return False

    return True

# cma RP, MMW, 종금형 선택시 필터링 정상적으로 동작하는지 확인, 상세화면에서 각 상품 종류가 아닌 다른 종류가 노출되면 False 반환
def cma_kind():

    global sum_fail, sum_nt

    sheet_kind = wb.sheet_by_name("통장 종류 idx")

    try:
        for x in range (1, 4):

            kind_select = driver.find_element(By.CSS_SELECTOR, ".listWrap_119TX > :nth-child(1) > ul > :nth-child(4) > div")

            kind_select.click()
            driver.find_element(By.CSS_SELECTOR, ".listWrap_119TX > :nth-child(1) > ul > :nth-child(4) > div > ul > :nth-child(" + str(x + 1) + ")").click()

            sleep(2)

            invest_detail = driver.find_elements(By.CLASS_NAME, "link_gW3ms")

            if len(invest_detail) == 0:
                continue

            invest_detail[0].click()

            sleep(2)

            invest_kind = driver.find_element(By.CSS_SELECTOR, "tbody > tr > :nth-child(1)").text

            if invest_kind != str(sheet_kind.cell(x, 1).value):
                print("\x1b[1;31mFail\x1b[1;m - 선택한 통장종류에 해당하는 상품이 정상적으로 노출되지 않습니다.")
                sum_fail += 1
                return False

            driver.find_element(By.LINK_TEXT, "결과 리스트로").click()

            wait = 0

            while True:
                # 20초 기다렸는데도 load되지 않았을때, timeout처리
                if wait > 20:
                    screenshot()
                    print("\x1b[1;31mFail\x1b[1;m - 상품 로드 timeout")
                    sum_fail += 1
                    return False

                if len(driver.find_elements(By.CLASS_NAME, "cardWrap_3dP8_")) > 0:
                    break

        # 통장 종류 필터 적용 전으로 되돌리기
        driver.find_element(By.CSS_SELECTOR, ".listWrap_119TX > :nth-child(1) > ul > :nth-child(4) > div").click()
        driver.find_element(By.CSS_SELECTOR,".listWrap_119TX > :nth-child(1) > ul > :nth-child(4) > div > ul > :nth-child(1)").click()

    except NoSuchElementException:
        print("N/T - 통장종류 관련 요소를 찾지 못함")
        sum_nt += 1
        return False

    sleep(2)

    return True

# 정렬 필터 적용 했을 때 상품 비교
def confirm_filter(n, m):

    global sum_fail, sum_nt

    if n <= 1:
        return True

    try:
        for x in range(1, n):

            driver.find_element(By.CSS_SELECTOR, ".cardsContainer_2d0E9 > :nth-child(" + str(x) + ")").location_once_scrolled_into_view
            interest1 = driver.find_element(By.CSS_SELECTOR, ".cardsContainer_2d0E9 > :nth-child(" + str(x) + ") > .body_3UwsQ > dl > :nth-child(2) > strong > :nth-child(" + str(m + 1) + ")").text\
                .replace("원", "").replace(",", "").replace("적용받은 금리", "").replace("최대금리", "").replace("%","").replace(" ", "")
            interest2 = driver.find_element(By.CSS_SELECTOR, ".cardsContainer_2d0E9 > :nth-child(" + str(x + 1) + ") > .body_3UwsQ > dl > :nth-child(2) > strong > :nth-child(" + str(m + 1) + ")").text\
                .replace("원", "").replace(",", "").replace("적용받은 금리", "").replace("최대금리", "").replace("%","").replace(" ","")

            if float(interest1) < float(interest2):
                screenshot()
                if m == 1:
                    print("\x1b[1;31mFail\x1b[1;m - 연 이자 높은 순 필터가 정상적으로 동작하지 않습니다.")
                elif m == 2:
                    print("\x1b[1;31mFail\x1b[1;m - 금리 높은 순 필터가 정상적으로 동작하지 않습니다.")
                elif m == 3:
                    print("\x1b[1;31mFail\x1b[1;m - 최대금리 순 필터가 정상적으로 동작하지 않습니다.")
                print(interest1, interest2)
                sum_fail += 1
                return False

    except NoSuchElementException:
        print("N/T - 연 이자 금액을 찾지 못함")
        sum_nt += 1
        return False

    return True

def screenshot():

    file_dir = "screenshot/cmaresulttest/"

    if i < 10:
        screenshot_name = "cmaresulttest00" + str(i) + "_fail_" + datetime.today().strftime("%Y%m%d%H%M") + ".png"
    else:
        screenshot_name = "cmaresulttest0" + str(i) + "_fail_" + datetime.today().strftime("%Y%m%d%H%M") + ".png"

    driver.save_screenshot(file_dir + screenshot_name)

# main 함수 시작

#백그라운드 옵션
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("window-size=1920x1080")
chrome_options.add_argument("headless")

print("------------------------테스트 시작------------------------")

start = time.time()

for i in range(1, total + 1):

    # 크롬드라이버를 백그라운드로 돌리고 싶을 때(또는 다른 옵션을 추가하고 싶을 때), 크롬드라이버 디렉토리 뒤에 옵션 추가
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)

    if i < 10:
        print("cmaresulttest00" + str(i) + " Running...")
    else:
        print("cmaresulttest0" + str(i) + " Running...")

    driver.get("https://banksalad.com/cma/questions")

    sleep(2)

    try:
        driver.find_element(By.LINK_TEXT, "결과보기").click()
    except NoSuchElementException:
        print("N/T - 결과보기 버튼을 찾지못함")
        sum_nt += 1
        driver.quit()
        continue

    # 상품 load
    if not load_invest():
        driver.quit()
        continue

    # 가입방법 > 비대면 가입은 디폴트로 체크되어있기때문에 초기에 체크 해제
    try:
        driver.find_element(By.CSS_SELECTOR, ":nth-child(2) > ul > :nth-child(1) > div > input").location_once_scrolled_into_view
        driver.find_element(By.CSS_SELECTOR, ":nth-child(2) > ul > :nth-child(1) > div > input").click()
    except NoSuchElementException:
        print("N/T - 가입방법 체크박스를 찾지못함")
        sum_nt += 1
        driver.quit()
        continue

    # TC에 해당하는 값 체크
    if not check():
        driver.quit()
        continue

    # 값 선택후, 노출되는 상품들 div -> 노출되는 상품이 없을 때, Fail 처리 (확인이 필요한 사항이기 때문에, 이전에는 노출되는 상품이 있었음)
    invest_div = driver.find_elements(By.CLASS_NAME, "cardWrap_3dP8_")

    if len(invest_div) == 0:
        print("N/T - 노출되는 상품이 없습니다.")
        sum_nt += 1
        driver.quit()
        continue

    invest_div[0].location_once_scrolled_into_view

    # 비대면 가입만 선택한 경우, '비대면 가입' 메세지 노출되는지 않는 상품이 있을 때 Fail 처리
    if not confirm_signup(invest_div):
        screenshot()
        driver.quit()
        continue

    # 선택한 통장기능에 맞지 않는 상품이 노출되는 경우 Fail 처리
    if not confirm_func(invest_div):
        screenshot()
        driver.quit()
        continue

    # 선택한 수수료 혜택에 맞지 않는 상품이 노출되는 경우 Fail 처리
    if not confirm_ben(invest_div):
        screenshot()
        driver.quit()
        continue

    # 선택한 통장 종류에 맞지 않는 상품이 노출되는 경우 Fail 처리 & 함수 마지막에 통장종류를 전체로 바꿔줌
    if not cma_kind():
        screenshot()
        driver.quit()
        continue

    # 상품 load
    if not load_invest():
        driver.quit()
        continue

    # 연 이자 높은 순 필터 적용
    try:
        driver.find_element(By.CSS_SELECTOR, ".headSort_1LuVw").location_once_scrolled_into_view
        driver.find_element(By.CSS_SELECTOR, ".headSort_1LuVw").click()
        driver.find_element(By.CSS_SELECTOR, ".headSort_1LuVw > div > ul > :nth-child(1)").click()
    except NoSuchElementException:
        print("N/T - 연 이자 높은 순 필터 관련 요소를 찾지못함")
        sum_nt += 1
        driver.quit()

    # 상품 load
    if not load_invest():
        driver.quit()
        continue

    invest_div = driver.find_elements(By.CLASS_NAME, "cardWrap_3dP8_")

    if not confirm_filter(len(invest_div), 1):
        driver.quit()
        continue

    # 금리 높은 순 필터 적용
    try:
        driver.find_element(By.CSS_SELECTOR, ".headSort_1LuVw").location_once_scrolled_into_view
        driver.find_element(By.CSS_SELECTOR, ".headSort_1LuVw").click()
        driver.find_element(By.CSS_SELECTOR, ".headSort_1LuVw > div > ul > :nth-child(2)").click()
    except NoSuchElementException:
        print("N/T - 금리 높은 순 필터 관련 요소를 찾지못함")
        sum_nt += 1
        driver.quit()

    # 상품 load
    if not load_invest():
        driver.quit()
        continue

    invest_div = driver.find_elements(By.CLASS_NAME, "cardWrap_3dP8_")

    if not confirm_filter(len(invest_div), 2):
        driver.quit()
        continue

    # 금리 높은 순 필터 적용
    try:
        driver.find_element(By.CSS_SELECTOR, ".headSort_1LuVw").location_once_scrolled_into_view
        driver.find_element(By.CSS_SELECTOR, ".headSort_1LuVw").click()
        driver.find_element(By.CSS_SELECTOR, ".headSort_1LuVw > div > ul > :nth-child(3)").click()
    except NoSuchElementException:
        print("N/T - 최대금리 순 필터 관련 요소를 찾지못함")
        sum_nt += 1
        driver.quit()

    # 상품 load
    if not load_invest():
        driver.quit()
        continue

    invest_div = driver.find_elements(By.CLASS_NAME, "cardWrap_3dP8_")

    if not confirm_filter(len(invest_div), 3):
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