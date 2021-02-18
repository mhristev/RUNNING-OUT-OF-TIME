from datetime import date
'''count = 0
today = None

def func():
    global today
    global count
    if count == 0:
        today = date.today()
        print(today)
        count += 1


func()
#print("Count: " + str(count))
#print("Today: " + str(today))
if today != date.today():
    print("Today's date:", today)
else:
    print("In else")
'''

today = date.today()

while(1):
    if today != date.today():
        #refresh tasks
        today = date.today()