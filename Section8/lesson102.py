import datetime

now = datetime.datetime.now()
print(now)
print(now.isoformat())
print(now.strftime("%d/%m/%y-%H%M%S%f"))

today = datetime.date.today()
print(today)

#d= datetime.timedelta(weeks=1)
d = datetime.timedelta(days=365)
print(now - d)