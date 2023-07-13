# test
import pymysql
import requests
import jsontest
import time
import random
import datetime
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='mysql', charset='utf8')
cur = conn.cursor()
session=requests.Session()
cur.execute("USE baidu")
for num in range(3339153721,3339153723):
	randomnnum=random.randint(1,10000)
	#randomnnum=0
	#ranum=randomnnum+num
	if randomnnum%6==1:
		logid='MTQ4NTM1NTg0MTY2NTAuNzA0ODA0MTM3NDM0MDgyMQ'
	elif randomnnum%6==2:
		logid='MTQ4NTC1NTg0MTY2NAAuQzA0ODV0MTS3NDM0MDgyMZ'
	elif randomnnum%6==3:
		logid='MTQ4NTQ1ADgyMjUzMjAuMTg0dDIwMzkxODkxMzM0NzU'
	elif randomnnum%6==4:
		logid='MTQ4NTQ1AAgyMMzuMjjUATg0dDIkxOwMzDkxMzMzU0N'
	else:
		logid='MTQ4NTQ1AAgyMMzuQzAUATg0dDIkxOwMz0MDMzMzU0N'
	headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36","Accept":"application/json, text/javascript, */*; q=0.01","X-Requested-With":"XMLHttpRequest","Referer":"http://pan.baidu.com/share/home?uk=%d"%(num)}
	url="http://pan.baidu.com/pcloud/feed/getsharelist?t=%s&category=0&auth_type=1&request_location=share_home&start=0&limit=60&query_uk=%d"%(time.mktime(datetime.datetime.now().timetuple()),num)+"&channel=chunlei&clienttype=0&web=1&logid=%s==&bdstoken=33136d882b09290e80b3aa990b965091"%(logid)
	try:
		req=session.get(url,headers=headers)
	except Exception as e:
		print(e)
	else:
		time.sleep(6)
		data=req.text
		#print(data)
		data=json.loads(req.text)
		#time.sleep(6)#经测试最低为6，不会因为请求过快被中断
		if(data['errno']==0):
			limit=1;
			datalist=data['records']
			for x in range(len(datalist)):
				if(datalist[x]['feed_type']!='album'):
					#print("INSERT INTO data VALUES (null,'http://pan.baidu.com/s/%s','%s','%s',%s);"%(datalist[x]['uk'],datalist[x]['shorturl'],datalist[x]['title'],datalist[x]['category']))
					cur.execute("INSERT INTO data VALUES (null,'%s','http://pan.baidu.com/s/%s','%s',%s);"%(datalist[x]['uk'],datalist[x]['shorturl'],datalist[x]['title'].replace("'", "\\'"),datalist[x]['category']))
					cur.connection.commit()
				else:
					cur.execute("INSERT INTO data VALUES (null,'%s','http://pan.baidu.com/pcloud/album/info?uk=%s&album_id=%s','%s',%s);"%(datalist[x]['uk'],datalist[x]['uk'],datalist[x]['album_id'],datalist[x]['title'].replace("'", "\\'"),datalist[x]['category']))
					cur.connection.commit()
			while (len(datalist)==60):
				randomnnum=random.randint(1,6)
				if randomnnum%6==1:
					logid='MTQ4NTM1NTg0MTY2NTAuNzA0ODA0MTM3NDM0MDgyMQ'
				elif randomnnum%6==2:
					logid='MTQ4NTC1NTg0MTY2NAAuQzA0ODV0MTS3NDM0MDgyMZ'
				elif randomnnum%6==3:
					logid='MTQ4NTQ1ADgyMjUzMjAuMTg0dDIwMzkxODkxMzM0NzU'
				elif randomnnum%6==4:
					logid='MTQ4NTQ1AAgyMMzuMjjUATg0dDIkxOwMzDkxMzMzU0N'
				else:
					logid='MTQ4NTQ1AAgyMMzuQzAUATg0dDIkxOwMz0MDMzMzU0N'
				headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36","Accept":"application/json, text/javascript, */*; q=0.01","X-Requested-With":"XMLHttpRequest","Referer":"http://pan.baidu.com/share/home?uk=%d"%(num)}
				url="http://pan.baidu.com/pcloud/feed/getsharelist?t=%s&category=0&auth_type=1&request_location=share_home&start=%d&limit=60&query_uk=%d"%(time.mktime(datetime.datetime.now().timetuple()),limit*60,num)+"&channel=chunlei&clienttype=0&web=1&logid=%s==&bdstoken=33136d882b09290e80b3aa990b965091"%(logid)
				try:
					req=session.get(url,headers=headers)
				except Exception as e:
					print(e)
				else:
					time.sleep(6)
					data=req.text
					data=json.loads(data)
				datalist=data['records']
				for x in range(len(datalist)):
					if(datalist[x]['feed_type']!='album'):
						#print("INSERT INTO data VALUES (null,'http://pan.baidu.com/s/%s','%s','%s',%s);"%(datalist[x]['uk'],datalist[x]['shorturl'],datalist[x]['title'],datalist[x]['category']))
						cur.execute("INSERT INTO data VALUES (null,'%s','http://pan.baidu.com/s/%s','%s',%s);"%(datalist[x]['uk'],datalist[x]['shorturl'],datalist[x]['title'].replace("'", "\\'"),datalist[x]['category']))
						cur.connection.commit()
					else:
						cur.execute("INSERT INTO data VALUES (null,'%s','http://pan.baidu.com/pcloud/album/info?uk=%s&album_id=%s','%s',%s);"%(datalist[x]['uk'],datalist[x]['uk'],datalist[x]['album_id'],datalist[x]['title'].replace("'", "\\'"),datalist[x]['category']))
						cur.connection.commit()
				limit=limit+1
		elif(data['errno']==-55):
			print('请求失败，请求速度太快被暂时禁止请求，遍历值减一,重新遍历uk值,并且休息两分钟')
			num=num-1
			time.sleep(120)
		else:
			print('请求失败，原因未知,休息两分钟，重新请求')
			num=num-1
			time.sleep(120)

	print(num)

cur.close
conn.close



