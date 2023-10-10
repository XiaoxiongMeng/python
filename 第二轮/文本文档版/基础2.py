import requests
import re
month = ['01','02','03','04','05','06','07','08','09','10','11','12']
maxd = 0
dm = ''
maxt = 0
tm = ''
maxl = 0
lm = ''
days = [31,29,31,30,31,30,31,31,30,31,30,31]
ua = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
for i in month:
    postUrl = 'https://baike.baidu.com/cms/home/eventsOnHistory/'+i+'.json?_=1668083268575'
    xx = requests.get(postUrl, headers=ua)
    xx.encoding = 'utf-8'
    t = xx.json()
    print(i+"月")
    for u in range(1,days[int(i)-1]+1):
        date = ''
        print(u,'日',type(i))
        if u<10 :
            date = i + '0' + str(u)
        else:
            date = i + str(u)
        todayHistory = t[i][date]
        txt = ''
        for m in todayHistory:
            # print (m['link'])
            m['title'] = re.sub("<(.|\n)*?>", '', m['title'])
            m['desc'] = re.sub("<(.|\n)*?>", '', m['desc'])
            m['title'] = m['title'].replace("'", "`")
            m['desc'] = m['desc'].replace("'", "`")
            m['desc'] = m['desc'] + '...'
            m['desc'] = re.sub("<(.|\n)*?\.", '', m['desc'])
            if len(m['desc'])>maxd:
                maxd = len(m['desc'])
                dm = m['desc']
            if len(m['title']) > maxt:
                maxt = len(m['title'])
                tm = m['title']
            if len(m['link'])>maxl:
                maxl = len(m['link'])
                lm = m['link']
            if m['type'] == 'birth':
                typet = '神人诞生\n'
            elif m['type'] == 'death':
                typet = '巨星陨落\n'
            else:
                typet = '其他类型\n'
            print(m['year']+"年的今天,"+m['title']+'。\n事件类型:'+typet+m['desc']+'...更多请移步百度百科.\n')
            txt += ('\n\n\n'+m['year']+"年的今天,"+m['title']+'。\n事件类型:'+typet+m['desc']+'...更多请移步百度百科:\n'+m['link']+'\n')
        with open('./历史上的今天'+date+'.txt', 'w', encoding='utf-8') as fp:
            fp.write(txt)

print(f"输出完成,并已写入运行目录下.\n最长内容:{maxd}\n{dm}\n最长标题:{maxt}\n{tm}\n最长链接:{maxl}\n{lm}\n")
