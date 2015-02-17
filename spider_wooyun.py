Enter file contents here
import mysql.connector
import sys, os
import urllib.request
import re
import itertools
import base64

search_item='金融'
#以后只需要修改search_item就可以了
#转成bytes string
bytesString = search_item.encode(encoding="utf-8")
encodestr = base64.b64encode(bytesString)
#base64 编码

user = 'root'
pwd  = ''
host = '127.0.0.1'
db   = 'test'
data_file = 'wooyun.dat'
create_table_sql = "CREATE TABLE IF NOT EXISTS mytable ( serial_number_sql varchar(100), title_sql varchar(100), \
    loophole_type_sql varchar(100) , industry_sql varchar(100) , author_sql varchar(100) , yield_time_sql varchar(100), \
    loophole_mood_sql varchar(100), hazard_rating_sql varchar(100), reveal_mood_sql varchar(200),\
    detail_sql varchar(5000), repair_sql varchar(2000), path_sql varchar(50))\
    CHARACTER SET utf8"

insert_sql = "INSERT INTO mytable (serial_number_sql, title_sql, loophole_type_sql, industry_sql, \
    author_sql, yield_time_sql, loophole_mood_sql, hazard_rating_sql, reveal_mood_sql, \
    detail_sql, repair_sql, path_sql) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

query_num_sql="select count(serial_number_sql) from mytable"

remove_duplicated_sql="delete from mytable where serial_number_sql in (select serial_number_sql from \
(select  serial_number_sql  from  mytable  group  by  serial_number_sql  having  count(serial_number_sql) > 1)as total)"

cnx = mysql.connector.connect(user=user, password=pwd, host=host, database=db)
cursor = cnx.cursor()

def create_table_sql_api(a):
    try:
        cursor.execute(a)
    except mysql.connector.Error as err:
        print("create table 'mytable' failed.")
        print("Error: {}".format(err.msg))
        sys.exit()

def insert_sql_api(a,b):
    try:
        cursor.execute(a,b)
    except mysql.connector.Error as err:
        print("insert table 'mytable' failed.")
        print("Error: {}".format(err.msg))
        sys.exit()

create_table_sql_api(create_table_sql)
#mysql数据库

starturl="http://www.wooyun.org/searchbug.php?q="+encodestr.decode()
loophole=[]
nextpage=[]
result=[]
#定义页面跳转相关变量

def get_html_response(url):
    html_response = urllib.request.urlopen(url).read().decode('utf-8')
    return html_response

def geturl(starturl):
    a=get_html_response(starturl)
    childurl=(re.findall(r'/bugs/wooyun-\w*-\w*\b',a))
    return childurl

def get_nextpage(starturl):
    d=get_html_response(starturl)
    num_p=0
    num=re.findall(r'\d*\s页',d)
    for i in num:
        i=re.sub(r'\s页','',i)
        num_p=i
    for x in range(1,int(num_p)):
        x='searchbug.php?q='+encodestr.decode()+'&pNO='+str(x)
        nextpage.append(x)
    return nextpage

def download_img(url):
    img_name=re.sub(r'http://wooyun.org/upload/\d*/','',url)
    download_img=urllib.request.urlretrieve(url,'D:\wooyun\%s'%img_name)

def download_html(i,title):
    html_path='D:\\wooyun_html\\'+title+'.html'
    download_html=open(html_path,'w+',encoding='utf-8')
    download_html.write(i)
    download_html.close()
    return('wooyun_html\\'+title+'.html')

for i in get_nextpage(starturl):
    result+=geturl('http://wooyun.org/'+i)
    #扫描各种漏洞的url地址放入result中
result=set(result)#去除result中重复的地址

serial_number_p=''
title_p=''
refered_industry_p=''
author_p=''
yield_time_p=''
loophole_type_p=''
loophole_mood_p=''
hazard_rating_p=''
reveal_mood_p=[]
detail_p=[]
repair_p=''
final=[]
if_updated=False
updated_serial_num=[]
#定义漏洞相关变量

cursor.execute(query_num_sql)
num_t=list(cursor.fetchall())
num_t=list(num_t[0])
num=int(num_t[0])

for i in result:
    k=get_html_response('http://wooyun.org/'+re.sub(search_item,encodestr,i))#下载页面到k

    #基础信息提取
    serial_number=re.findall(r'">WooYun-\w{4}-\w*',k)
    title=re.findall(r'漏洞标题：.*.</h3>',k)
    refered_industry=re.findall(r'相关厂商：.*.',k)
    author=re.findall(r'<a href="http://www.wooyun.org/whitehats/\S*">',k)
    yield_time=re.findall(r'提交时间：.*.',k)
    loophole_type=re.findall(r'漏洞类型：.*.',k)
    hazard_rating=re.findall(r'危害等级：.*.</h3>',k)
    loophole_mood=re.findall(r'漏洞状态：\s*\S*\s*</h3>',k)
    #详细信息提取
    reveal_mood=re.findall(r'\d*-\d*-\d*：\s*\S*<br/>',k)
    detail=re.findall(r'<p class="detail">.*.</p>',k)
    repair=re.findall(r'修复方案：</h3>\s*<p class="detail">.*.\s*</p>',k)
    #基础信息处理
    for j in serial_number:
        j=re.sub(r'">','',j)
        serial_number_p=j

    for j in title:
        j=re.sub('漏洞标题：\t\t','',j)
        j=re.sub(r'\s</h3>','',j)
        title_p=j

    for j in refered_industry:
        j=re.sub(r'相关厂商：\t\t<a href="http://www.wooyun.org/corps/','',j)
        j=re.sub(r'">\r','',j)
        refered_industry_p=j
    
    for j in author:
        j=re.sub(r'<a href="http://www.wooyun.org/whitehats/','',j)
        j=re.sub(r'">','',j)
        author_p=j

    for j in yield_time:
        j=re.sub(r'提交时间：\t\t','',j)
        j=re.sub(r'</h3>\r','',j)
        yield_time_p=j

    for j in loophole_type:
        j=re.sub(r'漏洞类型：\t\t','',j)
        j=re.sub(r'</h3>\r','',j)
        loophole_type_p=j

    for j in hazard_rating:
        j=re.sub(r'危害等级：\t\t','',j)
        j=re.sub(r'</h3>','',j)
        hazard_rating_p=j

    for j in loophole_mood:
        j=re.sub(r'漏洞状态：\s*','',j)
        j=re.sub(r'\s*</h3>','',j)
        loophole_mood_p=j
    #详细信息处理
    for j in reveal_mood:
        j=re.sub('<br/>','',j)
        reveal_mood_p.append(j)
    
    for j in detail:#处理详情
        j=re.sub(r'：\s',':',j)
        j=re.sub(r'<p class="detail">','',j)
        j=re.sub(r'</p>','',j)
        j=re.sub(r'"\starget="_blank"><img\ssrc="/upload/.*.width="600"/></a>',',',j)
        j=re.sub(r'<a href="',' http://wooyun.org',j)
        j=re.sub(r'对本漏洞信息进行评价，.*.备学习价值','',j)
        detail_p.append(j)
    
    for j in repair:#处理回复方法
        j=re.sub(r'</br>','',j)
        j=re.sub(r'</p>','',j)
        j=re.sub(r'修复方案：</h3>','',j)
        j=re.sub(r'<p\sclass="detail">','',j)
        j=re.sub(r'：',':',j)
        j=j.split()
        repair_p=j
    
    serial_number_str= "".join(itertools.chain(*serial_number_p))
    title_str="".join(itertools.chain(*title_p))
    loophole_type_str="".join(itertools.chain(*loophole_type_p))
    refered_industry_str="".join(itertools.chain(*refered_industry_p))
    author_str="".join(itertools.chain(*author_p))
    yield_time_str="".join(itertools.chain(*yield_time_p))
    loophole_mood_str="".join(itertools.chain(*loophole_mood_p))
    hazard_rating_str="".join(itertools.chain(*hazard_rating_p))
    detail_str="".join(itertools.chain(*detail_p))  
    reveal_mood_str="".join(itertools.chain(*reveal_mood_p))
    repair_str="".join(itertools.chain(*repair_p))

    img=re.findall(r'http://wooyun.org/upload/\d*/\w*\.\w{3}',detail_str)
    for j in img:
        download_img(j)
    path=download_html(k,serial_number_str)
    #将str加入final列表并转化为元组保存进sql
    final.append(serial_number_str)
    final.append(title_str)
    final.append(loophole_type_str)
    final.append(refered_industry_str)
    final.append(author_str)
    final.append(yield_time_str)
    final.append(loophole_mood_str)
    final.append(hazard_rating_str)
    final.append(reveal_mood_str)
    final.append(detail_str)
    final.append(repair_str)
    final.append(path)
    query_update_sql="select * from mytable where serial_number_sql = '%s'"%serial_number_str
    cursor.execute(query_update_sql)
    if final==list(cursor.fetchall()):
        pass
    else:
        if_updated=True
        updated_serial_num.append(serial_number_str)
    insert_sql_api(insert_sql,tuple(final))
    detail_p.clear()
    reveal_mood_p.clear()
    final.clear()

cursor.execute(remove_duplicated_sql)#去除重复项
cursor.execute(query_num_sql)
num_t=list(cursor.fetchall())
num_t=list(num_t[0])
num2=int(num_t[0])

#邮件模块
if(num2>num or if_updated):
    import smtplib
    import email.mime.multipart
    import email.mime.text

    msg=email.mime.multipart.MIMEMultipart()
    msg['from']=''
    msg['to']=''
    msg['subject']='告警邮件'
    content='您好，您的漏洞库新增%d'%(num2-num)+'条漏洞，请速去查看。'
    if num2>num:
        content+='从第%d条开始为新增的漏洞。'%num
    if if_updated:
        content+='以下乌云漏洞状态有更新：\n'
        for i in updated_serial_num:
            content+=i
            content+=','
    txt=email.mime.text.MIMEText(content)
    msg.attach(txt)

    smtp=smtplib
    smtp=smtplib.SMTP()
    smtp.connect('','25')
    #example:address of smtp server
    smtp.login('','')
    #sender and keyword 
    smtp.sendmail('','',str(msg))
    #sender & acceptor
    smtp.quit()



cnx.commit()
cursor.close()
cnx.close()
