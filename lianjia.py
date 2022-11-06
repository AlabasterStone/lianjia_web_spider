from bs4 import *
import requests
from lxml import etree
import json
from rich.console import Console

houseInfoList = list()
city = input()
district = input()

rConsole = Console()

for pg in range(1, 3):
    rConsole.log(f'starting search list{pg}...')

    url = f"https://{city}.lianjia.com/ershoufang/{district}/pg{pg}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    sellList = soup.find('ul', class_='sellListContent')
    houseList = []

    rConsole.log('done.')

    for sell in sellList.children:
        houseList.append(sell.a['href'])

    rConsole.log('starting collect house info...')
    for house in houseList:
        houseInfo = dict()
        houseRes = requests.get(house)
        soup = BeautifulSoup(houseRes.text, 'lxml')
        tree = etree.HTML(houseRes.text)
        houseInfo['ROOM'] = tree.xpath(
            "/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[1]/text()")[0][0]
        houseInfo['FLOR'] = tree.xpath(
            "/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[2]/text()")[0]
        if houseInfo['FLOR'][0: 2] == '低楼层':
            houseInfo['FLOR'] = 0
        elif houseInfo['FLOR'][0: 2] == '中楼层':
            houseInfo['FLOR'] = 1
        else:
            houseInfo['FLOR'] = 2

        houseInfo['AREA'] = tree.xpath(
            "/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[3]/text()")[0]
        houseInfo['STRT'] = tree.xpath(
            "/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[4]/text()")[0]
        if houseInfo['STRT'] == '平层':
            houseInfo['STRT'] = 0
        else:
            houseInfo['STRT'] = 1
        houseInfo['TYPE'] = tree.xpath(
            "/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[6]/text()")[0]
        if houseInfo['TYPE'] == '塔楼':
            houseInfo['TYPE'] = 0
        elif houseInfo['TYPE'] == '板塔结合':
            houseInfo['TYPE'] = 1
        else:
            houseInfo['TYPE'] = 2
        houseInfo['FACE'] = tree.xpath(
            "/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[7]/text()")[0]
        houseInfo['FITM'] = tree.xpath(
            "/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[9]/text()")[0]
        if houseInfo['FITM'] == '毛坯':
            houseInfo['FITM'] = 0
        else:
            houseInfo['FITM'] = 1
        houseInfo['WARM'] = tree.xpath(
            "/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[11]/text()")[0]
        if houseInfo['WARM'] == '集中供暖':
            houseInfo['WARM'] = 0
        else:
            houseInfo['WARM'] = 1
        houseInfo['EVAL'] = tree.xpath(
            "/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[12]/text()")[0]
        if houseInfo['EVAL'] == '无':
            houseInfo['EVAL'] = 0
        else:
            houseInfo['EVAL'] = 1
        houseInfo['INTRO'] = tree.xpath(
            "/html/body/div[7]/div[1]/div[2]/div/div[3]/div[2]/text()")
        houseInfo['ROUND'] = tree.xpath(
            "/html/body/div[7]/div[1]/div[2]/div/div[5]/div[2]/text()")

        houseInfoList.append(houseInfo)
    
    rConsole.log('done.')

with open(f'data/{district}.json', "w", encoding='utf-8') as f:
    f.write(json.dumps(houseInfoList, ensure_ascii=False))

#import pandas as pd
#data = pd.DataFrame(houseInfoList)
#data.to_excel('xicheng.xlsx', index=None)
