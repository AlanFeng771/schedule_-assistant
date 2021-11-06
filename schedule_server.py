import socket
import pymysql
import json
from crontab import CronTab

ip_addr = '0.0.0.0'  # allow any ip connect
port = 8080

sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.bind((ip_addr, port))
sk.listen()

allow_msg = 'allow_input'
hello_msg = 'hello'
exit_msg = 'exit'
schedule_msg = 'schedule'
show_schedule_msg = 'show'

while True: 
    print('listen') 
    conn, addr = sk.accept() 
    print(f'welcome client {addr}~~~') 
    conn.sendall(allow_msg.encode()) 
    while True:
        clientMessage = str(conn.recv(1024), encoding='utf-8')
        keyword = clientMessage.split('-')
        if keyword[0][-1] == ' ':    # avoid " " behind the keyword
            keyword[0] = keyword[0][:-1]

        parameter = dict()
        for item in keyword[1:]:
            item = item.split(' ', 1)
            parameter.update({item[0] : item[1]}) 

        print(f'Client : {keyword}')
        print(f'parameter : {parameter}')

        if keyword[0] == 'exit': # end connection
            conn.sendall(exit_msg.encode())
            conn.sendall(allow_msg.encode())
            conn.close()
            break

        if keyword[0] == 'hello': # say hello
            conn.sendall(hello_msg.encode())
            conn.sendall(allow_msg.encode())

        if keyword[0] == 'schedule':
            # schedule use crontab
            month = int(parameter['d'].split('/')[0])
            day = int(parameter['d'].split('/')[1])
            hour = int(parameter['t'].split(':')[0])
            minute = int(parameter['t'].split(':')[1])
            print(f'm : {month}, d : {day}, h : {hour}, m : {minute}')
            with CronTab(user=True) as cron:
                job = cron.new(command='/usr/bin/python3.8 /home/azureuser/python_workspace/mid_project/schedule_notify.py')
                job.setall(minute, hour, day, month, None)
            print('job was just executed')

            # save data in sql
            db = pymysql.connect(host='localhost', user='user1', password='Aa123', database='mysql')
            cursor = db.cursor()
            sql = """INSERT INTO schedule(date, time, info) VALUES ("%s", "%s", "%s")"""
            values = (parameter['d'], parameter['t'], parameter['m'])
            cursor.execute(sql, values)
            db.commit()
            db.close()
            conn.sendall(schedule_msg.encode())
            conn.sendall(allow_msg.encode())

        if keyword[0] == 'show':
            db = pymysql.connect(host='localhost', user='user1', password='Aa123', database='mysql')
            cursor = db.cursor()
            sql = """SELECT * FROM schedule;"""
            cursor.execute(sql)
            results = cursor.fetchall()
            results = json.dumps(results)
            print(results)
            db.close()
            conn.sendall(show_schedule_msg.encode())
            conn.send(bytes(results, encoding='utf-8'))
            # conn.sendall(allow_msg.encode())


    break
