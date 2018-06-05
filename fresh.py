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
browser = webdriver.Firefox()
str1=[]
def start():
    #print("Enter the name of the author you want to search:")
    #search=sys.argv[1]
    url=sys.argv[1]
    print(url)
    browser.get(url)
    elem = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gsc_sa_ccl"]/div/div/h3/a/span')))
    source = browser.page_source
    button = browser.find_element_by_css_selector('#gsc_sa_ccl > div > div > h3 > a > span')
    button.click()
    element = WebDriverWait(browser,30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#gsc_a_b > tr:nth-child(1) > td.gsc_a_t > a')))
    source1=browser.page_source
    soup = BeautifulSoup(source1,'html.parser')
    dashboard_url=browser.current_url
    css_1="tr.gsc_a_tr:nth-child("
    css_2=") > td:nth-child(2)"
    j=1
    make_directory()
    str1.append('[')
    while True:
        try:
        #if(browser.find_element_by_css_selector(css_1+str(j)+css_2)):
            button2 = browser.find_element_by_css_selector(css_1+str(j)+css_2)
            button2.click()
            source2=browser.page_source
            soup = BeautifulSoup(source2,'html.parser')

            scrape_data(soup)
            i=10

            while True:
                if not soup.find("div",{'class':'gs_a'}):
                    break
                else:
                    next_url=make_url(i)
                    i+=10
                    print(next_url)
                    browser.get(next_url)
                    source3=browser.page_source
                    soup = BeautifulSoup(source3,'html.parser')
                    scrape_data(soup)
            j+=1
            browser.get(dashboard_url)
        except:
            break
    str1.append(']')


def make_url(num):
    text=browser.current_url
    text1,text2=text.split('?')
    text3,text4=text2.split("&",1)
    next_url=text1+"?"+"start="+str(num)+"&"+text4
    return next_url

def scrape_data(soup):
    name1,name2,name3=sys.argv[1].split('=')
    print(name3)
    file=open('./directory1/'+name3+'.json',"a")
    str2=[]
    ele=[]
    for ele in soup.find_all("div",{"class":"gs_ri"}):  #for the whole class
        #for ele1 in ele.find_all("h3",{'class':"gs_rt"}):
        #    for a1 in ele1.find_all('a'):
        #        str1.append(a1.text)
        for ele2 in ele.find_all("div",{'class':'gs_a'}):
            for a2 in ele2.find_all('a'):
                str1.append("\"")
                str1.append(a2.text)
                str1.append("\"")
                str1.append(",")
    #str1.append(']}')
    var = ''.join(str1)
    file.write(var)
    file.close()



def make_directory():
    path = "./directory1"
    os.makedirs(path, exist_ok=True)
    print ("Path is created")

start()
