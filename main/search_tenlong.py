import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

def search_tenlong(request):
    def search(url):
        Response=requests.get(url)
        Soup=BeautifulSoup(Response.text,'html.parser')
        Titlelist = Soup.select('div.search-result-list  div.book-data strong')
        Datalist = Soup.select('div.search-result-list div.book-data span.publish-date')
        Pricelist = Soup.select('div.search-result-list div.book-data span.price')
        Imglist = Soup.select('div.search-result-list img')
        Booklist = []
        for Title,Price,Data,Img in zip(Titlelist,Pricelist,Datalist,Imglist):
            bookdata = []
            bookdata.append(Title.text.replace("\n","").split("(")[0])
            bookdata.append(Price.text.replace(" ","").replace("\n",""))
            bookdata.append(Data.text)
            bookdata.append(Img.attrs["src"])
            Booklist.append(bookdata)
        return Booklist
    if request.method == 'POST':
        keyword = request.POST['keyword']
        url='https://www.tenlong.com.tw/search?keyword=%s' %keyword
        Booklist = search(url)
        return render(request,"search_book.html",{"Booklist":Booklist,"keyword":keyword})        
    else:
        try:
            keyword = request.GET['keyword']
        except:
            keyword="熱門"
        url='https://www.tenlong.com.tw/search?keyword=%s' %keyword
        Booklist = search(url)
        return render(request,"search_book.html",{"Booklist":Booklist,"keyword":keyword})