from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
import requests
from bs4 import BeautifulSoup

def govresource(request):
    url='https://www.tqc.org.tw/TQCNet/Certificate.aspx'
    response=requests.get(url)
    response=requests.get(url)
    if response.status_code==200:
        soup=BeautifulSoup(response.text,'html.parser')
        #類別串列
        categorylist = soup.select('div.col-xs-12 div.CertPanel-heading')
        #名稱串列
        titlelist = soup.select('div.col-xs-12 h4') 
        smalllist = soup.select('div.col-xs-12 small')
        #網址串列
        hreflist = soup.select('div.col-xs-12 a')
        
        examlist=[]
        for category,title,small,hrefpath in zip(categorylist,titlelist,smalllist,hreflist):
            href = "https://www.tqc.org.tw/TQCNet/" + hrefpath.attrs["href"].replace(" ","%20")
            response=requests.get(href)
            if response.status_code==200:
                soup=BeautifulSoup(response.text,'html.parser')
                bookname = soup.select('div.Book-middle h3')[-1].text.split("(")[0]
                if bookname ==  "雲端練功坊輔考專用線上練習系統":
                    bookname = "python3 程式設計"
                elif bookname ==  "MySQL 5實力養成暨評量":
                    bookname = "MySQL 5"
            examlist.append([category.text,title.text+small.text,href,bookname])

    if request.method == 'POST':
        return render(request,"govexam.html",{"examlist":examlist})
        #return HttpResponse(url)
    else:
        return render(request,"govexam.html",{"examlist":examlist})