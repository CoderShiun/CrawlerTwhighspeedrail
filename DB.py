import sqlite3
import datetime
systime = datetime.datetime.now()
date = systime + datetime.timedelta(days=1)
tomorrow = date.date().strftime("%Y/%m/%d")

def cretable():
    connection = sqlite3.connect("TwhispeedrailDb.sqlite")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE %s" % tomorrow + "(id PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, 車次 TEXT NOT NULL, \
    出發時間 TEXT NOT NULL, 抵達時間 TEXT NOT NULL, 備註 TEXT)")
    connection.commit()
    connection.close()