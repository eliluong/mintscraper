# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 11:57:10 2021

@author: eliluong
"""

import time
import requests
import json
import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random
import datetime
import calendar
from dateutil.relativedelta import relativedelta

def test(v_driver):
    # scrapeCSVTable(v_driver)
    # navigateMonth(v_driver)
    primaryLoop(v_driver)

# scrapes the tabulated data and returns as comma-delimited array
def scrapeCSVTable(v_driver):
    # expand it first if necessary
    try:
        expand_button = v_driver.find_element_by_id('show-more-less')
        if expand_button.get_attribute('innerHTML') == 'Show more':
            v_driver.execute_script("arguments[0].scrollIntoView();", expand_button)
            expand_button.click()
            print('clicked expand button')
    except Exception as e:
        print('no need to expand')
        print(e)
    
    haystack = v_driver.find_element_by_id('portfolio-entries')
    
    # get the months
    haystack_months = haystack.find_elements_by_xpath('//th[@title]')
    # for i in haystack_months:
    #     print(i.get_attribute('innerHTML'))
    
    # get values
    haystack_values = haystack.find_elements_by_xpath('//th[@title]/following::td[1]')
    # for i in haystack_values:
    #     print(i.get_attribute('innerHTML'))
        
    # construct returnArray
    returnArray = []
    for count, item in enumerate(haystack_months):
        try:
            returnArray.append(item.get_attribute('innerHTML') + ',' + haystack_values[count].get_attribute('innerHTML').replace('$','').replace(',',''))
        except Exception as e:
            print(e)
    
    print(returnArray)
    return returnArray

def primaryLoop(v_driver):
    arrayData = []
    
    # generate list of dates to extract data from
    dates = generateDates('1/2008', '12/2010')
    
    # iterate through each month of data, followed by data extraction,
    # and append into an array
    for index, item in enumerate(dates):
        print(item)
        startDate = item[0].strftime("%m/%d/%Y")
        endDate = item[1].strftime("%m/%d/%Y")
        
        navigateMonth(v_driver, startDate, endDate)
        time.sleep(2)
        
        for i in scrapeCSVTable(v_driver):
            arrayData.append(i)
    
    for i in arrayData:
        print(i)
        
    return 0

# navigates to Custom start/end date range
def navigateMonth(v_driver, v_start, v_end):   
    # navigate to date-menu
    menu = v_driver.find_element_by_xpath("//div[@id='date-menu']//div[@id='trends-datedropdown']")
    action = ActionChains(v_driver)
    action.move_to_element(menu).perform()
    
    # navigate to Custom
    menu = v_driver.find_element_by_xpath("//div[@id='trends-datedropdown']//ul[@class='listmenu']/li[contains(text(),'Custom')]")
    action.move_to_element(menu).perform()
    menu.click()
    
    # enter input
    dateStart = v_driver.find_element_by_xpath("//div[@id='pop-trends-calendar']//input[@id='trend-popup-start-input']")
    action.move_to_element(dateStart).perform()
    dateStart.click()
    dateStart.send_keys(Keys.CONTROL, 'a')
    dateStart.send_keys(v_start)
    
    dateEnd = v_driver.find_element_by_xpath("//div[@id='pop-trends-calendar']//input[@id='trend-popup-end-input']")
    action.move_to_element(dateEnd).perform()
    dateEnd.click()
    dateEnd.send_keys(Keys.CONTROL, 'a')
    dateEnd.send_keys(v_end)
    
    # click OK button
    ok_button = v_driver.find_element_by_id('trend-popup-ok')
    ok_button.click()

# generate start and end dates for range of months within a year
# requires input format of month/year (eg 1/2008)
def generateDates(v_start, v_end):
    month_start, year_start = v_start.split('/')
    month_end, year_end = v_end.split('/')
    
    dateArray = []
    
    # determine number of months total to iterate through
    t_start = datetime.datetime(year_start, month_start, 1)
    t_end = datetime.datetime(year_end, month_end, 1)
    total_months = (t_end.year - t_start.year) * 12 + t_end.month - t_start.month
    
    # iterate through each month to generate start/end dates
    # uses relativedelta to interate through each month
    for i in range(total_months + 1):
        start_date = t_start + relativedelta(months = i)
        last_day = start_date.replace(day = calendar.monthrange(start_date.year, start_date.month)[1])
        
        dateArray.append([start_date, last_day])
    
    return dateArray
