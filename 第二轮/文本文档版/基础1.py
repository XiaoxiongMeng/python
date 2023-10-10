import sys
import requests
import re
import datetime
starttime = datetime.datetime.now()
group = []
title = []
sum = 0
net = []
txt = ''
page = ''


def getlist(url):
    global group, title, net, page, txt, sum
    returns = requests.get(url)  # 发送一个请求
    returns.encoding = 'utf-8'  # 防止出现乱码
    txt = returns.text  # 取出其中的文本
    groups = re.findall("\u3010.*?\u3011", txt)  # 获取各个文章来自的部门
    titles_first = re.findall(".htm\" target=\"_blank\" title=\".*?\"", txt)  # 使用正则表达式对文本进行第一次过滤
    titles_second = ''  # 初始化一个字符串变量用来存储第二遍过滤的文本
    for temp in titles_first:  # 进行第二次过滤
        titles_second += re.findall("title=\".*?\"", temp)[0]
    titles = re.findall("\".*?\"", titles_second)  # 最后一次过滤
    nets_first = re.findall("<a href=\".*info/..../.*?htm\"", txt)  # 获取详细网址链接并过滤
    nets_second = ''
    for temp in nets_first:
        nets_second += re.findall("\".*?\"", temp)[0]
    nets = re.findall("\".*?\"", nets_second)
    for temp in range(0, len(groups)):  # 去除作者组中的冗余括号
        groups[temp] = groups[temp].strip('【')
        groups[temp] = groups[temp].strip('】')
    for temp in range(0, len(titles)):  # 去除标题中冗余的引号
        titles[temp] = titles[temp].strip('"')
    for temp in range(0, len(nets)):  # 去除网址中冗余的引号
        nets[temp] = nets[temp].strip('"')
        nets[temp] = 'https://jwch.fzu.edu.cn/' + nets[temp].strip('../')
    group += groups
    title += titles
    net += nets
    sum += len(nets)


def getinfo(url):
    detailsAll = requests.get(url)
    detailsAll.encoding = 'utf-8'
    detailsText = detailsAll.text
    with open("./福州大学教务处通知概览集合.txt", 'a', encoding='utf-8') as fp:
        fp.write(re.findall("发布时间：....-..-..", detailsText)[0]+'\n')
    with open("./福州大学教务处通知概览集合.txt", 'a', encoding='utf-8') as fp:
        fp.write('详情链接:' + url + '\n')
    if len(re.findall('\u5df2\u4e0b\u8f7d', detailsText)) == 0:
        with open("./福州大学教务处通知概览集合.txt", 'a', encoding='utf-8') as fp:
            fp.write('无附件'+'\n')
        return
    filename = re.findall("\">.*?</a>】已下载", detailsText)
    ajaxUrls = re.findall("\([0-9]{7,8}", detailsText)
    downloadnet = re.findall("【<a href=\".*?\"", detailsText)
    numbers = len(ajaxUrls)
    for i in range(0, numbers):
        ajaxUrls[i] = ajaxUrls[i].strip('(')
        dlt = requests.get(
            'https://jwch.fzu.edu.cn/system/resource/code/news/click/clicktimes.jsp?wbnewsid=' + ajaxUrls[
                i] + '&owner=1744984858&type=wbnewsfile&randomid=nattach')
        times = dlt.text
        downloadTimes = ''
        for u in range(15, 19):
            downloadTimes += times[u]
        downloadTimes = (downloadTimes.strip("\"")).strip(",")
        downloadnet[i] = downloadnet[i].strip("【<a href=\"")
        downloadnet[i] = downloadnet[i].strip("\"")
        downloadnet[i] = 'https://jwch.fzu.edu.cn' + downloadnet[i]
        downloadTimes = downloadTimes.strip(",")
        filename[i] = filename[i].strip("\">附件：")
        filename[i] = filename[i].strip("</a>】已下载")
        filename[i] = filename[i].strip("1：")
        filename[i] = filename[i].strip("2：")
        filename[i] = filename[i].strip("3：")
        filename[i] = filename[i].strip("4：")
        filename[i] = filename[i].strip("5：")
        with open("./福州大学教务处通知概览集合.txt", 'a', encoding='utf-8') as fp:
            fp.write('附件' + str(i + 1) + ':  ' + filename[i] + '  下载次数:' + downloadTimes + '\n')
            fp.write("下载链接:" + downloadnet[i] + '\n')


getlist('https://jwch.fzu.edu.cn/jxtz.htm')
with open("./福州大学教务处通知概览集合.txt",'w',encoding='utf-8')as fp:
    fp.write('')
pages = re.findall("...\.htm\">2", txt)  # 从这里开始4行取页码总数
for i in range(0, 3):
    page += pages[0][i]
page = int(page) + 1
print('总页数为', page)
with open("./福州大学教务处通知概览集合.txt",'a',encoding='utf-8')as fp:
    fp.write('总页数为' + str(page))
for i in range(1, page):  # 循环获取前100个
    getlist('https://jwch.fzu.edu.cn/jxtz/' + str(int(page) - i) + '.htm')
    print("\r", end="")
    print("获取信息进度: {}%: ".format(int(((i + 1) / page) * 100)), "▓" * (int(((i + 1) / page) * 100) // 2), end="")
    sys.stdout.flush()
print('')
for i in range(0, sum):
    with open("./福州大学教务处通知概览集合.txt", 'a', encoding='utf-8') as fp:
        fp.write('*****************************' + str(i + 1)+ '************************************\n')
        fp.write('通知标题:' + title[i] + '\n文章来源:' + group[i]+'\n')
    getinfo(net[i])  # 详情链接50 标题100 附件链接120
    print("\r", end="")
    print("存储到文本文档进度: {}% ".format(int(((i + 1) / sum) * 100)), "▓" * int((((i + 1) / sum) * 100) // 2),
          end="")
    sys.stdout.flush()
endtime = datetime.datetime.now()
print(f'\n已经全部存储完成,耗时{endtime-starttime}')