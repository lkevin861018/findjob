import re
import time
from django.http import HttpResponse
from selenium import webdriver
from bs4 import BeautifulSoup
from django.shortcuts import redirect, render
from selenium.webdriver.chrome.options import Options
import os
import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from pandas import DataFrame
from main.models import Dreamreal, shop, companyacc


def govresource(request):
    if request.method == 'POST':
        keyword = request.POST['category']
        url = 'https://www.tqc.org.tw/TQCNet/Certificate.aspx'
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
        categorylist = soup.find_all(class_="CertPanel CertPanel-%s" % keyword)
        examlist = []
        for category in categorylist:
            cate = category.find(class_="CertPanel-heading").text
            title = category.find('h4').text
            small = category.find('small').text
            href = category.find_parent().attrs['href'].replace(' ', '%20')
            suburl = "https://www.tqc.org.tw/TQCNet/" + href
            response = requests.get(suburl)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                img = soup.select('div.Book-item img')[-1].attrs['src']
                bookname = soup.select(
                    'div.Book-item h3')[-1].text.split("(")[0]
                if bookname == "MySQL 5實力養成暨評量":
                    bookname = "MySQL 5"

                examlist.append([cate, title+small, suburl, bookname, img])
        return render(request, "govexam.html", {"examlist": examlist})
    else:
        return render(request, "govexam.html")


def search_tenlong(request):
    def search(url):
        Response = requests.get(url)
        Soup = BeautifulSoup(Response.text, 'html.parser')
        Titlelist = Soup.select('div.search-result-list  div.book-data strong')
        Datalist = Soup.select(
            'div.search-result-list div.book-data span.publish-date')
        Pricelist = Soup.select(
            'div.search-result-list div.book-data span.price')
        Imglist = Soup.select('div.search-result-list img')
        Booklist = []
        for Title, Price, Data, Img in zip(Titlelist, Pricelist, Datalist, Imglist):
            bookdata = []
            bookdata.append(Title.text.replace("\n", "").split("(")[0])
            bookdata.append(Price.text.replace(" ", "").replace("\n", ""))
            bookdata.append(Data.text)
            bookdata.append(Img.attrs["src"])
            Booklist.append(bookdata)
        return Booklist
    if 'keyword' in request.COOKIES:
        keyword = request.COOKIES['keyword']
        url = 'https://www.tenlong.com.tw/search?keyword=%s' % keyword
        Booklist = search(url)
        del request.COOKIES['keyword']
        return render(request, "search_book.html", {"Booklist": Booklist, "keyword": keyword})

    if request.method == 'POST':
        keyword = request.POST['keyword']
        if keyword == "":
            keyword = "熱門"
        url = 'https://www.tenlong.com.tw/search?keyword=%s' % keyword
        Booklist = search(url)
        return render(request, "search_book.html", {"Booklist": Booklist, "keyword": keyword})
    else:
        try:
            keyword = request.GET['keyword']
        except:
            keyword = "熱門"
        url = 'https://www.tenlong.com.tw/search?keyword=%s' % keyword
        Booklist = search(url)
        return render(request, "search_book.html", {"Booklist": Booklist, "keyword": keyword})


def search_hahow(request):
    if request.method == 'POST':
        titleListdata = []
        nameListdata = []
        priceListdata = []
        imgListdata = []
        page = request.POST['page']
        keyword = request.POST['keyword']
        if '' in [keyword]:
            keyword = '熱門'

        url = 'https://hahow.in/search/courses?query=%s&page=%s' % (
            keyword, page)

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
        browser.set_window_size(900, 900)
        urlsource = browser.page_source
        # browser.set_page_load_timeout(5)
        soup = BeautifulSoup(urlsource, 'html.parser')
        time.sleep(3)

        titleList = soup.select('div.sc-18817me-0 h4')
        nameList = soup.select('div.sc-18817me-0 p')
        priceList = soup.select(
            'div.sc-18817me-0 div.course-status-bar div span.text-secondary')
        imgList = soup.select('div.sc-18817me-0 div.relative img')

        for title, name, price, img in zip(titleList, nameList, priceList, imgList):
            temptitle = title.text
            tempName = name.text.replace('．', '')
            tempimg = img.attrs["src"]
            try:
                tempprice = 'NT' + \
                    price.text.replace('|', '').strip().split('NT')[1]
                priceListdata.append(tempprice)
            except:
                pattern = "NT.+"
                price = re.findall(pattern, price.text)
                for p in price:
                    if p != []:
                        priceListdata.append(p)

            titleListdata.append(temptitle)
            nameListdata.append(tempName)
            imgListdata.append(tempimg)

        df = []
        for i in range(len(titleListdata)):
            df.append([titleListdata[i],
                       nameListdata[i],
                       priceListdata[i],
                       imgListdata[i]])
        return render(request, 'search_hahow.html', context={'Fclass': df})
    else:
        return render(request, 'search_hahow.html')


item = ''
urltype = ''


def shoppingr(request):
    global urltype, item
    try:
        try:
            item = request.GET['item']
            urltype = request.GET['type']
        except:
            urltype = request.GET['type']
            if 'c' == urltype:
                return redirect('search_hahow')
            elif 'b' == urltype:
                return redirect('search_book')
    except:
        messages.add_message(
            request, messages.INFO, '非預期錯誤!')
        return redirect('index')
    return render(request, 'shopping.html', context={'item': item})


def shopping(request):
    if request.method == 'POST':
        try:
            account = request.session['account']
        except:
            messages.add_message(
                request, messages.INFO, '請先登入!')
            return redirect('login')
        try:
            try:
                try:
                    user = Dreamreal.objects.get(pid=account)
                except:
                    user = Dreamreal.objects.get(email=account)
                name = user.firstname+user.lastname
                pid = user.pid
            except:
                try:
                    user = companyacc.objects.get(pid=account)
                except:
                    user = companyacc.objects.get(email=account)
                name = user.companyname
                pid = user.pid
        except:
            messages.add_message(
                request, messages.INFO, '請進行登入!')
            return redirect('index')

        try:
            q = int(request.POST['quanty'])
        except:
            messages.add_message(
                request, messages.INFO, '數量錯誤，請填阿拉伯數字!')
            global urltype, item
            return redirect('https://findjob2022project.herokuapp.com/main/shoppingr?type=%s&itme=%s' % (urltype, item))
            # return redirect('http://127.0.0.1:8000/main/shoppingr?type=%s&itme=%s' % (urltype, item))

        Shop = shop(
            name=name,
            itemname=item,
            quanty=q,
            pid=pid
        )

        Shop.save()
        messages.add_message(
            request, messages.INFO, '購買成功!')
        if 'c' == urltype:
            return redirect('search_hahow')
        elif 'b' == urltype:
            return redirect('search_book')

    return redirect('index')


def shoplist(request):
    account = request.session['account']
    try:
        try:
            try:
                user = Dreamreal.objects.get(pid=account)
            except:
                user = Dreamreal.objects.get(email=account)
            upid = user.pid
        except:
            try:
                user = companyacc.objects.get(pid=account)
            except:
                user = companyacc.objects.get(email=account)
            upid = user.pid
    except:
        messages.add_message(
            request, messages.INFO, '請進行登入!')
        return redirect('index')

    try:
        shophist = shop.objects.filter(pid=upid)
        itemnamelist = []
        quantylist = []
        for i in range(len(shophist)):
            buyer = shophist[i].name
            itemnameh = shophist[i].itemname
            quantyh = shophist[i].quanty
            itemnamelist.append(itemnameh)
            quantylist.append(quantyh)
        data = {'buyer': buyer,
                'itemname': itemnamelist,
                'qunaty': quantylist
                }
        frame = DataFrame(data)
        frame.index += 1
    except:
        messages.add_message(
            request, messages.INFO, '查無購買紀錄!')
        return redirect('index')

    framehtml = frame.to_html()
    framehtml += r'<br><a href="/main/index"><button>返回首頁</button> </a>'
    return HttpResponse(framehtml)
