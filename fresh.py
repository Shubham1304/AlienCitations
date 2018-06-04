import os , sys
from selenium  import webdriver
from selenium.webdriver.common.keys import Keys
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import errno

def start():
    print("Enter the name of the author you want to search:")
    search=input()
    url="https://scholar.google.co.in/citations?view_op=search_authors&mauthors=" + search

    browser = webdriver.Firefox()
    browser.get(url)
    elem = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gsc_sa_ccl"]/div/div/h3/a/span')))
    source = browser.page_source
    button = browser.find_element_by_css_selector('#gsc_sa_ccl > div > div > h3 > a > span')
    button.click()
    element = WebDriverWait(browser,30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#gsc_a_b > tr:nth-child(1) > td.gsc_a_t > a')))
    source1=browser.page_source
    soup = BeautifulSoup(source1,'html.parser')
    button2 = browser.find_element_by_css_selector('tr.gsc_a_tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)')
    button2.click()
    source2=browser.page_source
    soup = BeautifulSoup(source2,'html.parser')
    make_directory()
    scrape_data(soup)
    i=10
    while True:
        try:
            next_url=make_url(i)
            i+=10
            browser.get(next_url)
        except:
            break


def make_url(num):
    text=browser.current_url()
    text1,text2=text.split('?')
    text3,text4=text2.split("&",1)
    next_url=text1+"?"+"start="+str(num)+"&"+text4
    return next_url

def scrape_data(soup):
    str1=[]
    #str1.append('{\"citations\":[')
    file=open('/home/shubham/directory2/data5.json',"a")
    str2=[]
    ele=[]
    for ele in soup.find_all("div",{"class":"gs_ri"}):  #for the whole class
        #for ele1 in ele.find_all("h3",{'class':"gs_rt"}):
        #    for a1 in ele1.find_all('a'):
        #        str1.append(a1.text)
        for ele2 in ele.find_all("div",{'class':'gs_a'}):
            for a2 in ele2.find_all('a'):
                str1.append(a2.text)
    #str1.append(']}')
    var = ' '.join(str1)
    file.write(var)
    file.close()



def make_directory():
    path = "/home/shubham/Desktop/directory2"
    os.makedirs(path, exist_ok=True)
    print ("Path is created")
