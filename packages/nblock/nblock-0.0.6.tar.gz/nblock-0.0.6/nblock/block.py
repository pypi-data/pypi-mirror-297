import time
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


def check_block(driver:WebDriver):
    return True if '검색 서비스 이용이 제한되었습니다' in driver.page_source else False

def handle(driver:WebDriver, ip_change_flag:bool=False, chrome_options=None):
    # 반환값 - True : 검색 가능 / False : 검색 불가능(검색제한)
    result = False
    if check_block(driver):
        try:
            solve_btn = driver.find_element(By.CSS_SELECTOR,'a[class="btn active"]')
            solve_btn.click()
        except: pass
        time.sleep(2)

    if check_block(driver):
        if ip_change_flag:
            pre_url = driver.current_url
            driver.quit()
            for _ in range(5):
                if ip_change2():
                    if chrome_options is None: driver = load_driver()
                    else: driver = load_driver(chrome_options=chrome_options)
                    driver.get(pre_url)
                    if check_block(driver):
                        continue
                    else:
                        result = True
                        break
                else:
                    for _ in range(10):
                        print('IP 변경 실패 {} 초 후 재시도'.format(10-_-1), end='\r')
            else:
                result = False
        else:
            result = False
    else:
        result = True

    return driver, result