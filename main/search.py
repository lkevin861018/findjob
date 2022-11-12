from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from urllib import response
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from selenium.webdriver.chrome.options import Options
import os


def search104(request):
    if request.method == 'POST':
        #-----準備空串列資料以利在使用Django時可套用此參數-----------------------------##
        tempTitleListData = []
        tempCompanyListData = []
        tempAreaListData = []
        tempExperienceListData = []
        tempEducationListData = []
        tempSalaryListData = []
        tempHrefListData = []
        #---------------------------------------------------------------------------##

        keyword = request.POST['keyword']
        num = request.POST['num']
        area = request.POST['area']
        url = "https://www.104.com.tw/jobs/search/?keyword=" + \
            keyword+"&indexpoc&ro=0&page="+num+'&area='+area
        chrome_options = Options()
        chrome_options.add_argument("--headless")
    # heroku上使用
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        browser = webdriver.Chrome(executable_path=os.environ.get(
            "CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        # browser = webdriver.Chrome(options=chrome_options)
        browser.implicitly_wait(5)
        browser.get(url)
        urlsource = browser.page_source
        soup = BeautifulSoup(urlsource, 'html.parser')
        #---------------------------------------------------------------------------##

        #-----職缺名稱---------------------------------------------------------------##
        TitleList = soup.select(
            'div#js-job-content div.b-block__left a.js-job-link')
        #-----公司名稱---------------------------------------------------------------##
        CompanyNameList = soup.select(
            'div#js-job-content div.b-block__left ul.b-list-inline a')
        #-----相關資料01(工作地點、相關經驗、學歷)-------------------------------------##
        Datalist = soup.select(
            'div#js-job-content div.b-block__left ul.job-list-intro')
        #-----相關資料02(薪水待遇)----------------------------------------------------##
        ContentList = soup.select(
            'div#js-job-content div.b-block__left div.job-list-tag')
        #-----職缺連結網址-----------------------------------------------------------##
        hreflinkList = soup.select(
            'div#js-job-content div.b-block__left h2.b-tit a')
        #---------------------------------------------------------------------------##

        for Title, CompanyName, Data, Content, href in zip(TitleList, CompanyNameList, Datalist, ContentList, hreflinkList):
            ##-----01.職缺名稱串列---------------------------------------------------##
            tmepTitle = Title.text.strip()
            tempTitleListData.append(tmepTitle)
            ##-----02.公司名稱串列---------------------------------------------------##
            tempCompanyName = CompanyName.text.strip()
            tempCompanyListData.append(tempCompanyName)
            ##-----03.工作地點串列---------------------------------------------------##
            tempArea = Data.text.strip().replace('\n', ',').replace(
                ',,', ',').replace(' ,', ',').split(',')[0]
            tempAreaListData.append(tempArea)
            ##-----04.相關經驗串列---------------------------------------------------##
            tempExperience = Data.text.strip().replace('\n', ',').replace(
                ',,', ',').replace(' ,', ',').split(',')[1]
            tempExperienceListData.append(tempExperience)
            ##-----05.學歷串列-------------------------------------------------------##
            tempEducation = Data.text.strip().replace('\n', ',').replace(
                ',,', ',').replace(' ,', ',').split(',')[2]
            tempEducationListData.append(tempEducation)
            ##-----06.薪水待遇串列---------------------------------------------------##
            tmepSalary = Content.text.strip().split(' ')[0].replace('月薪', '').replace(
                '元以上', '').replace('元', '').replace(',', '').replace('年薪', '')
            tempSalaryListData.append(tmepSalary)
            ##-----07.職缺連結網址串列-----------------------------------------------##
            tempHref = 'https:'+href.get('href')
            tempHrefListData.append(tempHref)
        df = []
        for i in range(len(tempTitleListData)):
            df.append([tempTitleListData[i],
                       tempCompanyListData[i],
                       tempAreaListData[i],
                       tempExperienceListData[i],
                       tempEducationListData[i],
                       tempSalaryListData[i],
                       tempHrefListData[i]])

        return render(request, 'search104.html', context={'FTjob': df})
    else:
        return render(request, 'search104.html')


def search_hahow(request):
    if request.method == 'POST':
        titleListdata = []
        nameListdata = []
        priceListdata = []
        page = request.POST['page']
        keyword = request.POST['keyword']
        if '' in [keyword]:
            url = 'https://hahow.in/courses?page=%s' % page
            way = 1
        else:
            url = 'https://hahow.in/search/courses?query=%s&page=%s' % (
                keyword, page)
            way = 2
        chrome_options = Options()
        chrome_options.add_argument("--headless")
    # heroku上使用
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        browser = webdriver.Chrome(executable_path=os.environ.get(
            "CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        # browser = webdriver.Chrome(options=chrome_options)
        browser.implicitly_wait(10)
        browser.get(url)
        browser.set_window_size(800, 800)
        urlsource = browser.page_source
        # browser.set_page_load_timeout(5)

        soup = BeautifulSoup(urlsource, 'html.parser')
        if way == 1:
            titleList = soup.select('div.list-container a h4.txt-bold')
            nameList = soup.select('div.list-container div.course-meta p')
            priceList = soup.select('div.list-container div.course-status-bar')
        elif way == 2:
            titleList = soup.select('div.list-container a h4.txt-bold')
            nameList = soup.select('div.list-container div.course-meta p')
            priceList = soup.select('div.list-container div.course-status-bar')

        for title, name, price in zip(titleList, nameList, priceList):
            temptitle = title.text
            tempName = name.text.replace('．', '')
            tempprice = 'NT'+price.text.replace('|', '').strip().split('NT')[1]

            titleListdata.append(temptitle)
            nameListdata.append(tempName)
            priceListdata.append(tempprice)
        df = []
        for i in range(len(titleListdata)):
            df.append([titleListdata[i],
                       nameListdata[i],
                       priceListdata[i]])
        return render(request, 'search_hahow.html', context={'Fclass': df})
    else:
        return render(request, 'search_hahow.html')
