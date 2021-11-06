import requests
import pymysql
from datetime import datetime
from crontab import CronTab
today = datetime.today()
msg = ''   # notify msg
db = pymysql.connect(host='localhost', user='user1', password='Aa123', database='mysql')
cursor = db.cursor()
sql = """SELECT * FROM schedule;"""
cursor.execute(sql)
results = cursor.fetchall()
for item in results:
    month = int(item[0].replace('\'', '').split('/')[0])
    day = int(item[0].replace('\'', '').split('/')[1])
    hour = int(item[1].replace('\'', '').split(':')[0])
    minute = int(item[1].replace('\'', '').split(':')[1])
    dat = datetime(year=2021, month=month, day=day, hour=hour, minute=minute)
    if today > dat:
        msg = item[2]
        #  delete this schedule record from mysql
        sql = """DELETE FROM schedule WHERE date=%s AND time=%s AND info=%s"""
        index = (item[0], item[1], item[2])
        cursor.execute(sql, index)
        db.commit()

        #  remove this job form crontab
        with CronTab(user=True) as cron:
           i = 0
           iter = cron.find_command('/usr/bin/python3.8')
           for job in iter:
               if i==0:
                   cron.remove(job)
                   print(job)
                   break

        break


print(f'msg : {msg}')
headers = {
    "Authorization": "Bearer " + "4CYT40v4ZkYNPCNmZpSkYZCnoBbuWFSfqWirhrTxaTt",
    "Content-Type": "application/x-www-form-urlencoded"
} 
params = {'message': msg}
 
r = requests.post("https://notify-api.line.me/api/notify",
                       headers=headers, params=params)
print(r.status_code)  #200
