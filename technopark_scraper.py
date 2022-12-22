from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

driver = webdriver.Firefox()
driver.get("https://www.technopark.org/company-a-z-listing")
screen_height = driver.execute_script("return window.screen.height;")

i = 1
while True:
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(5)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    if (screen_height) * i > scroll_height:
        break

soup=BeautifulSoup(driver.page_source,features="lxml")
links = []
for j in soup.find_all("a"):
    link=j.get("href")
    if(link and link.startswith('/company/')):
        links.append(link)
        
csv_list=[]
for link in links:
    driver.get('https://www.technopark.org'+link)
    soup=BeautifulSoup(driver.page_source, features="lxml")
    list=soup.find("ul",{"class":"list-sx"})
    list=list.find_all("li")
    name=list[1].contents[2]
    name=' '.join(name.split())
    address=list[2].contents[2]
    address=' '.join(address.split())
    mail=list[5].find("a").contents[0]
    csv_list.append([name,address,mail])
    
header = ['NAME', 'ADDRESS', 'MAIL']
with open('technopark.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for csv in csv_list:
        writer.writerow(csv)
