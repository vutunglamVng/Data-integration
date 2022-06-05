from logging import exception
import requests
from bs4 import BeautifulSoup
import csv

root = './'

def crawData():
    url = "https://www.nguyenkim.com/dien-thoai-di-dong/page-{}/"
    listUrl = []
    for i in range(1, 8):
        response = requests.get(url.format(i))
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.findAll('div', class_='item nk-fgp-items nk-new-layout-product-grid') 
        for link in links:
            listUrl.append(link.find('a').attrs["href"])   

    count = 0
    data = []
    for url in listUrl: 
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.find('h1', class_='product_info_name').text
        price = soup.find('span', class_='nk-price-final').text

        body = soup.find('table', class_='productSpecification_table')
        table = body.findChildren('tr')

        model = producer = origin = year = hdh = chip = ram = ''
        for row in table:
            label = row.find('td', class_='title').text
            value = row.find('td', class_='value').text
            if label == 'Model:':
                model = value
            elif label == 'Nhà sản xuất:':
                producer = value
            elif label == 'Xuất xứ:':
                origin = value
            elif label == 'Năm ra mắt :':
                year = value
            elif label == 'Hệ điều hành:':
                hdh = value
            elif label == 'Chipset:':
                chip = value
            elif label == 'RAM:':
                ram = value

        data.append([url, title, price, model, producer, origin, year, hdh, chip, ram])
        print(count)
        count += 1

    with open(root+'NguyenKim.csv', mode='a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['url', 'title', 'price', 'model', 'producer', 'origin', 'year', 'hdh', 'chip', 'ram'])
        for row in data:
            writer.writerow(row)

def crawlData2():
    listType = ['apple', 'samsung', 'xiaomi', 'oppo', 'nokia', 'realme', 'vsmart', 'asus', 'vivo']
    data = []
    count = 0
    for type in listType:
        url = "https://cellphones.com.vn/mobile/"+type+".html"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.findAll('div', class_='item-product') 
        for link in links:
            url = link.find('a').attrs["href"]
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            count += 1
            print(count)
            try:
                title = soup.find('div', class_='box-name__box-product-name').find('h1').text
                price = soup.find('div', class_='box-info__box-price').find('p', class_='special-price').text
            except:
                print(url)
                break

            body = soup.find('table', id='tskt')
            table = body.findChildren('tr')

            producer = type
            size = pin = weight = hdh = chip = ram = memory = ''
            for row in table:
                label = row.findChildren('th')[0].text
                value = row.findChildren('th')[1].text
                if label == 'Kích thước màn hình':
                    size = value
                elif label == 'Pin':
                    pin = value
                elif label == 'Trọng lượng':
                    weight = value
                elif label == 'Hệ điều hành':
                    hdh = value
                elif label == 'Chipset':
                    chip = value
                elif label == 'Dung lượng RAM':
                    ram = value
                elif label == 'Bộ nhớ trong':
                    memory = value

            data.append([url, title, price, producer, size, pin, weight, hdh, chip, ram, memory])

    with open(root+'CellPhones.csv', mode='a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['url', 'title', 'price', 'producer', 'size', 'pin', 'weight', 'hdh', 'chip', 'ram', 'memory'])
            for row in data:
                writer.writerow(row)

def crawlData3():
    listType = ['iphone', 'samsung', 'xiaomi', 'oppo', 'tecno', 'realme-1', 'vsmart']
    data = []
    count = 0
    for type in listType:
        baseUrl = "https://didongthongminh.vn/"+type
        response = requests.get(baseUrl)
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.findAll('div', class_='col-sm-5ths') 
        for link in links:
            count += 1
            print(count)
            try:
                url = link.find('a').attrs["href"]
            except:
                print("============")
                break

            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            title = soup.find('h1', class_='pull-left').text
            price = soup.find('div', class_='details_top').find('span', class_='_price').text

            body = soup.find('table', class_='charactestic_table')
            try:
                table = body.findChildren('tr')
            except:
                print(url)
                break

            producer = type
            size = pin = chip = ram = memory = ''
            for row in table:
                label = row.find('td', class_='title_charactestic').text
                value = row.find('td', class_='content_charactestic').text
                if label.find('Màn hình rộng') != -1:
                    size = value
                elif label.find('Dung lượng pin') != -1:
                    pin = value
                elif label.find('Chip xử lý') != -1:
                    chip = value
                elif label.find('RAM') != -1:
                    ram = value
                elif label.find('Bộ nhớ trong') != -1:
                    memory = value

            data.append([url, title, price, producer, size, pin, chip, ram, memory])

    with open(root+'Didongthongminh.csv', mode='a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['url', 'title', 'price', 'producer', 'size', 'pin', 'chip', 'ram', 'memory'])
            for row in data:
                writer.writerow(row)

crawlData3()

