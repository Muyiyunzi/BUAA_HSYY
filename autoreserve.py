from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException as TE
from selenium.common.exceptions import ElementClickInterceptedException as ECIE
import yaml
from school_trans import school_trans

# 基本信息

url = "https://jinshuju.net/f/GjvEPd" # 每次使用只需修改新的网址

conf_file = open('configs.yaml', 'rb')
configs = yaml.load(conf_file, Loader=yaml.Loader)

driver = webdriver.Chrome(r"chromedriver")
# driver下载地址 https://chromedriver.storage.googleapis.com/index.html
driver.maximize_window()

def explicit_find(method, value, driver=driver):
    # locator = (method, value)
    try:
        WebDriverWait(driver, 30, 0.5).until(EC.presence_of_element_located((method, value)))
        return driver.find_element(method, value)
    except TE:
        return 0


def explicit_click(method, value, driver=driver):
    ele = explicit_find(method, value)
    WebDriverWait(driver, 10, 0.5).until(EC.element_to_be_clickable(ele))
    try:
        ele.click()
    except ECIE:
        driver.execute_script("arguments[0].click();", ele)


if __name__ == '__main__':
    driver.get(url)
    # 选择学院
    explicit_click('css selector', '#root > div > form > div.published-form__body > div.ant-row.fields > div:nth-child(2) > div > div > div.ant-col.ant-form-item-control')
    explicit_click('css selector', '#react-select-2-option-%d' % school_trans(configs['school']))

    # 输入姓名、学号、联系方式
    explicit_find('css selector', '#root > div > form > div.published-form__body > div.ant-row.fields > div:nth-child(4) > div > div > div.ant-col.ant-form-item-control > div.ant-form-item-control-input > div > span > span > input').send_keys(configs['name'])
    explicit_find('css selector', '#root > div > form > div.published-form__body > div.ant-row.fields > div:nth-child(6) > div > div > div.ant-col.ant-form-item-control > div.ant-form-item-control-input > div > span > input').send_keys(configs['schoolid'])
    explicit_find('css selector', '#root > div > form > div.published-form__body > div.ant-row.fields > div:nth-child(8) > div > div > div.ant-col.ant-form-item-control > div.ant-form-item-control-input > div > span > div > span > input').send_keys(configs['mobile'])

    # 选择校区（与地点）
    if configs['campus'] == 0:
        explicit_click('css selector', '#root > div > form > div.published-form__body > div.ant-row.fields > div:nth-child(10) > div > div > div.ant-col.ant-form-item-control > div.ant-form-item-control-input > div > span > div > div:nth-child(1) > div > div > label > span.ant-radio')

        # root > div > form > div.published-form__body > div.ant-row.fields > div:nth-child(10) > div > div > div.ant-col.ant-form-item-control > div.ant-form-item-control-input > div > span > div > div:nth-child(1) > div > div > label > span.ant-radio

        explicit_click('css selector', '#root > div > form > div.published-form__body > div.ant-row.fields > div:nth-child(12) > div > div > div.ant-col.ant-form-item-control > div.ant-form-item-control-input > div > span > div > div > div > div > label > span.ant-radio')
    else:
        explicit_click('css selector', '#root > div > form > div.published-form__body > div.ant-row.fields > div:nth-child(10) > div > div > div.ant-col.ant-form-item-control > div.ant-form-item-control-input > div > span > div > div:nth-child(2) > div > div > label > span.ant-radio')

    # 选择一个空时间段，默认正序检索
    for i in range(1, 25):
        ele = explicit_find('css selector', '#root > div > form > div.published-form__body > div.ant-row.fields > div:nth-child(14) > div > div > div.ant-col.ant-form-item-control > div.ant-form-item-control-input > div > span > div > div:nth-child(%d) > div > div > label' % i)
        if "已满" in ele.get_property('textContent'):
            continue
        else:
            explicit_click('css selector', '#root > div > form > div.published-form__body > div.ant-row.fields > div:nth-child(14) > div > div > div.ant-col.ant-form-item-control > div.ant-form-item-control-input > div > span > div > div:nth-child(%d) > div > div > label > span.ant-radio' % i)
            break
    else:
        print("预约时间全满，请联系辅导员！")
        driver.quit()
        exit()

    print("选择完毕，准备提交……")

    # 提交。可以注释掉本句话选择手动提交
    explicit_click('css selector', '#root > div > form > div.published-form__footer > div > button')

    driver.quit()
    exit()