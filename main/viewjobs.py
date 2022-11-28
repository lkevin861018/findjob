from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from bs4 import BeautifulSoup
from django.shortcuts import render
from selenium.webdriver.chrome.options import Options
import os


def search104(request):
    if request.method == 'POST':
        while True:
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
            keyword.encode('utf-8').decode('latin1')
            num = request.POST['num']
            area = request.POST['area']
            url = "https://www.104.com.tw/jobs/search/?keyword=" + \
                keyword+"&indexpoc&ro=0&page="+num+'&area='+area
            chrome_options = Options()
            chrome_options.add_argument("--headless")
        # heroku上使用
            chrome_options.binary_location = os.environ.get(
                "GOOGLE_CHROME_BIN")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            browser = webdriver.Chrome(executable_path=os.environ.get(
                "CHROMEDRIVER_PATH"), chrome_options=chrome_options)
            # browser = webdriver.Chrome(options=chrome_options)
            browser.implicitly_wait(5)
            browser.get(url)
            urlsource = browser.page_source
            soup = BeautifulSoup(urlsource, 'html.parser')
            if soup != '':
                break
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
        res = render(request, 'search104.html', context={'FTjob': df})
        res.set_cookie('keyword', keyword)
        return res
    else:
        res = render(request, 'search104.html')
        res.set_cookie('keyword', '')
        return res


def parttime(request):
    def search(url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            WorkTitleList = soup.select('div.job_info h2.job-info-title')
            CompanyTitleList = soup.select(
                'div.job-info-company p.ellipsis-job-company')
            TimeList = soup.select('div.job-info-date span.date-time')
            hreflist = soup.select('ul.job-list a')
            SaleryList = soup.select('p.job_detail span.salary')
            AreaList = soup.select('p.job_detail span.place')
            PTjob = []
            for company, Time, title, href, Salery, Area in zip(CompanyTitleList, TimeList, WorkTitleList, hreflist, SaleryList, AreaList):
                PTjob.append([company.text.strip(), Time.text, title.text.strip(
                ), href.get('href'), Salery.text, Area.text])
        return PTjob

    if request.method == 'POST':
        url = 'https://www.chickpt.com.tw/?'
        keyword = request.POST['keyword']
        area = request.POST['area']
        if keyword != "":
            url += 'keyword=%s&' % keyword
        else:
            pass
        if area != "":
            url += 'area=%s&' % area
        else:
            pass
        PTjob = search(url)
        res = render(request, "parttime.html", {"PTjob": PTjob})
        res.set_cookie('keyword', keyword)
        return res
        # return HttpResponse(url)
    else:
        url = 'https://www.chickpt.com.tw/'
        PTjob = search(url)
        res = render(request, "parttime.html", {"PTjob": PTjob})
        res.set_cookie('keyword', '')
        return res


def fulltime(request):
    def search(url):
        Headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=Headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 職缺名稱串列
            TitleList = soup.select(
                'div.job-list-item div.card-body h5.card-title.title_6')
            # 公司名稱串列
            CompanyNameList = soup.select(
                'div.job-list-item div.card-body h6.job_item_company')
            # 工作地區串列
            WorkAreaList = soup.select(
                'div.job-list-item div.card-body a.job_item_detail_location')
            # 薪資串列
            SalaryList = soup.select(
                'div.job-list-item div.card-body div.job_item_detail_salary')
            # 上傳時間串列
            DateList = soup.select(
                'div.job-list-item div.card-body div.item_data div.job_item_data_mobile_show small.text-muted')
            # 應徵人數串列
            #PersonList=soup.select('div.job-list-item div.card-body div.item_data span.applicants_data')
            Hreflist = soup.select('div.job_item_info a')
            FTjob = []
            ##-----範例(請自行運用)--------------------------------------------------##
            for WorkArea, Date, Company, Title, Salary, Href in zip(WorkAreaList, DateList, CompanyNameList, TitleList, SalaryList, Hreflist):
                FTjob.append([WorkArea.text, Date.text, Company.text,
                             Title.text, Salary.text, Href.get('href')])
        return FTjob

    if request.method == 'POST':
        keyword = request.POST['keyword']
        num = request.POST['page']

        url = 'https://www.1111.com.tw/search/job?ks='+keyword+'&page='+num
        area = request.POST['area']
        if area != "":
            url += '&c0='+area
        FTjob = search(url)
        res = render(request, "fulltime.html", {"FTjob": FTjob})
        res.set_cookie('keyword', keyword)
        return res
    else:
        url = 'https://www.1111.com.tw/search/job?page=1'
        FTjob = search(url)
        res = render(request, "fulltime.html", {"FTjob": FTjob})
        res.set_cookie('keyword', '')
        return res
