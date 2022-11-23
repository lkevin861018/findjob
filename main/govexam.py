from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
import requests
from bs4 import BeautifulSoup

def govresource(request):
    if request.method == 'POST':
        keyword = request.POST['category']
        url='https://www.tqc.org.tw/TQCNet/Certificate.aspx'
        response=requests.get(url)
        if response.status_code==200:
            soup=BeautifulSoup(response.text,'html.parser')
        categorylist=soup.find_all(class_="CertPanel CertPanel-%s" % keyword) 
        examlist=[]
        for  category in categorylist:
            cate = category.find(class_="CertPanel-heading").text
            title = category.find('h4').text
            small = category.find('small').text
            href = category.find_parent().attrs['href'].replace(' ','%20')
            suburl = "https://www.tqc.org.tw/TQCNet/" + href
            response=requests.get(suburl)
            if response.status_code==200:
                soup=BeautifulSoup(response.text,'html.parser')
                img = soup.select('div.Book-item img')[-1].attrs['src']
                bookname = soup.select('div.Book-item h3')[-1].text.split("(")[0]
                if bookname ==  "MySQL 5實力養成暨評量":
                    bookname = "MySQL 5"
                
                examlist.append([cate,title+small,suburl,bookname,img])
        return render(request,"govexam.html",{"examlist":examlist})
    else:
        return render(request,"govexam.html")