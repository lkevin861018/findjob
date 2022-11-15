from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# Create your views here.

def parttime(request):
    def search(url):
        response=requests.get(url)
        if response.status_code==200:
            soup=BeautifulSoup(response.text,'html.parser')
            WorkTitleList=soup.select('div.job_info h2.job-info-title')
            CompanyTitleList=soup.select('div.job-info-company p.ellipsis-job-company')
            TimeList=soup.select('div.job-info-date span.date-time')
            hreflist=soup.select('ul.job-list a') 
            SaleryList=soup.select('p.job_detail span.salary')
            AreaList=soup.select('p.job_detail span.place')
            PTjob=[]           
            for company,Time,title,href,Salery,Area in zip(CompanyTitleList,TimeList,WorkTitleList,hreflist,SaleryList,AreaList):
                PTjob.append([company.text.strip(),Time.text,title.text.strip(),href.get('href'),Salery.text,Area.text])
        return PTjob

    if request.method == 'POST':
        url='https://www.chickpt.com.tw/?'
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
        return render(request,"parttime.html",{"PTjob":PTjob})
        #return HttpResponse(url)
    else:
        url='https://www.chickpt.com.tw/'
        PTjob = search(url)
        return render(request,"parttime.html",{"PTjob":PTjob})
    
def fulltime(request):
    def search(url):
        Headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
        response=requests.get(url,headers=Headers)
        if response.status_code==200:
            soup=BeautifulSoup(response.text,'html.parser')
            # 職缺名稱串列
            TitleList=soup.select('div.job-list-item div.card-body h5.card-title.title_6')
            # 公司名稱串列
            CompanyNameList=soup.select('div.job-list-item div.card-body h6.job_item_company')
            # 工作地區串列
            WorkAreaList=soup.select('div.job-list-item div.card-body a.job_item_detail_location')
            # 薪資串列
            SalaryList=soup.select('div.job-list-item div.card-body div.job_item_detail_salary')
            # 上傳時間串列
            DateList=soup.select('div.job-list-item div.card-body div.item_data div.job_item_data_mobile_show small.text-muted')
            # 應徵人數串列
            #PersonList=soup.select('div.job-list-item div.card-body div.item_data span.applicants_data')
            Hreflist=soup.select('div.job_item_info a') 
            FTjob=[]    
            ##-----範例(請自行運用)--------------------------------------------------##
            for WorkArea,Date,Company,Title,Salary,Href in zip(WorkAreaList,DateList,CompanyNameList,TitleList,SalaryList,Hreflist):
                FTjob.append([ WorkArea.text , Date.text , Company.text , Title.text , Salary.text , Href.get('href')])
        return FTjob
    
    if request.method == 'POST':
        keyword=request.POST['keyword']
        num=request.POST['page']
        
        url='https://www.1111.com.tw/search/job?ks='+keyword+'&page='+num
        area=request.POST['area']
        if area != "":
            url += '&c0='+area
        FTjob = search(url)
        return render(request,"fulltime.html",{"FTjob":FTjob})
    else:
        url='https://www.1111.com.tw/search/job?page=1'
        FTjob = search(url)
        return render(request,"fulltime.html",{"FTjob":FTjob})