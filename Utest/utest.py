# /usr/env python
#_*_coding:utf-8_*_


import selenium
from selenium import webdriver
import time
import pymysql
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
# from pyvirtualdisplay import Display


import requests

# display = Display(visible=0, size=(800, 600))
# display.start()

driver = webdriver.Firefox()

#driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.HTMLUNIT)

def loginUtest():

    driver.get("http://utest.qq.com/")

    time.sleep(3)
    driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/a").click()

    time.sleep(3)

    driver.switch_to.frame("login_frame")
    driver.find_element_by_xpath("//*[@id=\"img_out_244026510\"]").click()

    #driver.switch_to.frame()
    driver.switch_to.default_content()
    # #driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[3]/div[1]/a").click()
    # mobileUrl = "http://remote.utest.qq.com/deviceSearch?type=remote&searchName=MI-ONE%20Plus"
    # driver.get(mobileUrl)
    #
    # time.sleep(5)
    # timeText = driver.find_element_by_xpath("/html/body/div[6]/div[6]/div/dl/dd[4]").text.split("： ")
    #
    # print(timeText[1])

    return driver

def getMobileInfo(webdriver,model):

    model = model
    mobileUrl = "http://remote.utest.qq.com/deviceSearch?type=remote&searchName="+model
    driver.get(mobileUrl)

    time.sleep(2)
    timeText = driver.find_element_by_xpath("/html/body/div[6]/div[6]/div[1]/dl/dd[4]").text.split("： ")
    versionText = driver.find_element_by_xpath("/html/body/div[6]/div[6]/div/dl/dd[2]").text.split("： ")
    name = driver.find_element_by_xpath("/html/body/div[6]/div[6]/div/dl/dt[1]").text

    topValue = None
    print(timeText[1] +"****"+versionText[1] +"****"+name)
    # top排行只有部分手机有，所以这里需要做区分
    if timeText[1].isdigit():
        topValue = driver.find_element_by_xpath("/html/body/div[6]/div[6]/div[1]/dl/dd[4]").text.split("： ")
        timeText = driver.find_element_by_xpath("/html/body/div[6]/div[6]/div/dl/dd[5]").text.split("： ")
        sql = "update utest_mobile_model set name = '%s',time = '%s',version = '%s',top ='%s' where model ='%s'" % (
            name, timeText[1], versionText[1], topValue[1], model)
    else:
        sql = "update utest_mobile_model set name = '%s',time = '%s',version = '%s'where model ='%s'" % (
        name, timeText[1], versionText[1], model)

    print(sql)
    executeSql(sql,2)

def getModelId(webdriver):

    getModelSql = "SELECT model FROM utest_mobile_model"
    model = executeSql(getModelSql, 1)

    for index in range(model.__len__()):
        print(model[index][0])
        #getMobileInfo(driver, model[index][0])
        try:
            getMobileInfo(driver, model[index][0])
        except Exception as e:
            print(e)
            continue



def executeSql(sql,model):
    conn = pymysql.connect(host='192.168.3.193', user='root', passwd='cyhc2017', db='mobile', charset='utf8')
    cur = conn.cursor()
    result = cur.execute(sql)
    conn.commit()

    if model ==1:
        return cur.fetchall()

    conn.close()
    return result


if __name__ == "__main__":

    driver = loginUtest()

    getModelId(driver)
    driver.close()


