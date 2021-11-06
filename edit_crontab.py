from crontab import CronTab

with CronTab(user=True) as cron:
    job = cron.new(command='/usr/bin/python3.8 /home/azureuser/python_workspace/mid_project/schedule_notify.py')
    job.setall(1, 2, 3, 4, None)
    iter = cron.find_command('/usr/bin/python3.8')
    for job in iter:
       cron.remove(job)

print('cron.write() was just executed')

